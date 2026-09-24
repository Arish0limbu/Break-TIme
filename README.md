# Break-Time

Break-Time is a small Python command-line helper for reviewing and committing real Git changes that you have already staged.

## Behavior

- Running the tool without options is a read-only preview.
- The tool never edits files or stages changes for you.
- It creates one commit only when you pass --commit and a non-empty --message.
- It pushes only when you also pass --push.
- It uses your existing Git author identity and does not set a bot identity.
- Safe-path rules allow expected project files and block secrets and generated files.

There is no scheduler or automatic file generator.

## Requirements

- Python 3.10 or newer
- Git installed and available on PATH

## Install

From a checkout of this repository, install the command in your active Python environment:

~~~sh
python -m pip install .
break-time --help
~~~

You can also run the script directly without installing the package.

## Quick start

From the repository root, stage actual work and preview the staged files and summary:

~~~sh
git add README.md
break-time --stat
~~~

After reviewing the preview, create one commit with a clear message:

~~~sh
break-time --commit --message "docs: clarify usage"
~~~

To push the new commit to the current branch's origin remote, opt in explicitly with --push.

The tool refuses to continue if any staged path is outside SAFE_PATHS or matches PROTECTED_PATHS. Unstaged and untracked files remain untouched.

## Configuration

Edit python/config.py to change the allowlist, protected paths, or log level. PROTECTED_PATHS always takes precedence over SAFE_PATHS. Logging goes to the console and does not create a log file.

MIN_COMMITS and MAX_COMMITS remain temporarily for compatibility with older readers; the current helper ignores them.

## Design notes

- Git commands are run as argument lists without a shell.
- The helper does not stage files, configure an author, rewrite history, or force-push.
- A detached HEAD cannot be committed through the helper.
- GitHub Actions is not required; use your normal local Git workflow.
