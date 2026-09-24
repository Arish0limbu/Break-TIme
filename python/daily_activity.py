#!/usr/bin/env python3
"""Safely review and optionally commit already-staged Git changes.

The default mode is read-only. This tool never edits files or stages changes.
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path, PurePosixPath

import config


LOGGER = logging.getLogger(__name__)


class GitCommandError(RuntimeError):
    """Raised when a Git command cannot be completed."""


def setup_logging() -> None:
    """Log to the console without creating files in the repository."""
    level_name = str(getattr(config, "LOG_LEVEL", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(levelname)s: %(message)s",
        stream=sys.stdout,
    )


def run_git_command(arguments: list[str], cwd: Path, timeout: int = 30) -> str:
    """Run Git without a shell and return stdout unchanged."""
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            capture_output=True,
            check=False,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise GitCommandError("Git is not installed or is not available on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        raise GitCommandError(f"Git command timed out after {timeout} seconds.") from exc

    if result.returncode != 0:
        detail = result.stderr.strip()
        command = " ".join(arguments)
        message = f"git {command} failed with exit code {result.returncode}"
        if detail:
            message = f"{message}: {detail}"
        raise GitCommandError(message)

    return result.stdout


def get_repository_root() -> Path:
    """Return the root of the Git repository containing the current directory."""
    output = run_git_command(["rev-parse", "--show-toplevel"], Path.cwd())
    return Path(output.strip()).resolve()


def get_current_branch(repository: Path) -> str:
    """Return the current branch name, or an empty string for a detached HEAD."""
    return run_git_command(["branch", "--show-current"], repository).strip()


def _matches_path(path: str, pattern: str) -> bool:
    """Match an allowlist or protected pattern against a repository-relative path."""
    normalized_path = path.replace("\\", "/").strip("/")
    normalized_pattern = pattern.replace("\\", "/").strip("/")

    if not normalized_path or not normalized_pattern:
        return False

    if pattern.endswith(("/", "\\")):
        return (
            normalized_path == normalized_pattern
            or normalized_path.startswith(normalized_pattern + "/")
        )

    candidate = PurePosixPath(normalized_path)
    if candidate.match(normalized_pattern):
        return True

    return any(PurePosixPath(part).match(normalized_pattern) for part in candidate.parts)


def can_modify_file(filepath: str) -> bool:
    """Return whether a staged path is allowed by the configured path policies."""
    normalized_path = filepath.replace("\\", "/").strip("/")
    protected_paths = getattr(config, "PROTECTED_PATHS", ())
    safe_paths = getattr(config, "SAFE_PATHS", ())

    if any(_matches_path(normalized_path, pattern) for pattern in protected_paths):
        return False

    return any(_matches_path(normalized_path, pattern) for pattern in safe_paths)


def get_staged_files(repository: Path) -> list[str]:
    """Return staged paths, preserving spaces and other valid filename characters."""
    output = run_git_command(
        ["diff", "--cached", "--name-only", "-z"],
        repository,
    )
    return [path for path in output.split("\0") if path]


def get_staged_diff_stat(repository: Path) -> str:
    """Return Git's summary of staged insertions and deletions."""
    return run_git_command(["diff", "--cached", "--stat"], repository).strip()


def get_worktree_status(repository: Path) -> str:
    """Return the short status for staged, unstaged, and untracked changes."""
    return run_git_command(
        ["status", "--short", "--untracked-files=all"],
        repository,
    ).strip()


def commit_changes(repository: Path, message: str) -> None:
    """Commit staged changes only; the caller is responsible for staging."""
    run_git_command(["commit", "-m", message], repository)


def push_changes(repository: Path, branch: str) -> None:
    """Push the current branch to origin when the caller explicitly requests it."""
    run_git_command(["push", "origin", branch], repository)


def run_daily_activity(argv: list[str] | None = None) -> int:
    """Review staged changes and optionally commit or push them."""
    setup_logging()

    parser = argparse.ArgumentParser(
        description=(
            "Review already-staged changes. The default run is read-only; "
            "files are never edited or staged automatically."
        )
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="create one commit from the staged, allowed files",
    )
    parser.add_argument(
        "-m",
        "--message",
        help="commit message; required with --commit",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="push the new commit to origin; requires --commit",
    )
    parser.add_argument(
        "--stat",
        action="store_true",
        help="show Git's staged insertion and deletion summary",
    )
    args = parser.parse_args(argv)

    if args.commit and not args.message:
        parser.error("--message is required with --commit")
    if args.message and not args.commit:
        parser.error("--message can only be used with --commit")
    if args.push and not args.commit:
        parser.error("--push requires --commit")
    if args.message is not None and not args.message.strip():
        parser.error("commit message cannot be empty")

    try:
        repository = get_repository_root()
        status = get_worktree_status(repository)
        staged_files = get_staged_files(repository)

        LOGGER.info("Repository: %s", repository)
        if status:
            LOGGER.info("Working tree status:\n%s", status)
        else:
            LOGGER.info("Working tree is clean.")

        if not staged_files:
            LOGGER.info("No staged changes; nothing to commit.")
            return 0

        LOGGER.info("Staged files:")
        for filepath in staged_files:
            LOGGER.info("  %s", filepath)

        blocked_files = [
            filepath for filepath in staged_files if not can_modify_file(filepath)
        ]
        if blocked_files:
            LOGGER.error(
                "Refusing to continue because these staged paths are protected "
                "or outside SAFE_PATHS: %s",
                ", ".join(blocked_files),
            )
            return 2

        if args.stat:
            diff_stat = get_staged_diff_stat(repository)
            if diff_stat:
                LOGGER.info("Staged change summary:\n%s", diff_stat)

        if not args.commit:
            LOGGER.info(
                "Read-only preview complete. Stage intended files, then use "
                "--commit --message to create a commit."
            )
            return 0

        branch = get_current_branch(repository)
        if not branch:
            LOGGER.error("Cannot commit from a detached HEAD.")
            return 2

        commit_changes(repository, args.message.strip())
        LOGGER.info("Created one commit on branch %s.", branch)

        if args.push:
            push_changes(repository, branch)
            LOGGER.info("Pushed branch %s to origin.", branch)

        return 0
    except GitCommandError as exc:
        LOGGER.error("%s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(run_daily_activity())
