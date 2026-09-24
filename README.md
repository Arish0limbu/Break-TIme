# Break-Time

Break-Time is a small Python command-line helper for reviewing and committing real Git changes that you have already staged.

## Behavior

- Running the tool without options is a read-only preview.
- The tool never edits files or stages changes for you.
- It creates one commit only when you pass --commit and a non-empty --message.
- It pushes only when you also pass --push.
- It uses your existing Git author identity and does not set a bot identity.
- Safe-path rules allow expected project files and block secrets and generated files.

There is no commit target, scheduler, or automatic file generator.

## Requirements

- Python 3.10 or newer
- Git installed and available on PATH

## Quick start

From the repository root, stage files that contain your actual work and preview them:

~~~sh
git add README.md
python python/daily_activity.py
~~~

If the preview lists the intended files, create one commit with a clear message:

~~~sh
python python/daily_activity.py --commit --message "docs: clarify usage"
~~~

To push that commit to the current branch's origin remote, opt in explicitly:

~~~sh
python python/daily_activity.py --commit --message "docs: clarify usage" --push
~~~

The tool reports all staged paths. It refuses the operation if any staged path is outside SAFE_PATHS or matches PROTECTED_PATHS. Unstaged and untracked files remain untouched. You can stage files with Git yourself before running the helper.

## Configuration

Edit python/config.py to change the allowlist, protected paths, or log level.

- SAFE_PATHS defines repository-relative files and directories the helper may commit.
- PROTECTED_PATHS always takes precedence, even when a path also matches SAFE_PATHS.
- Logging goes to the console and does not create a log file in the repository.

MIN_COMMITS and MAX_COMMITS remain in the configuration temporarily for compatibility with older readers. The current helper ignores them.

## Design notes

- Git commands are run as argument lists without a shell.
- The helper does not stage all files, configure an author, rewrite history, or force-push.
- A detached HEAD cannot be committed through the helper.
- No GitHub Actions workflow is required; use your normal local Git workflow.
