# CLI reference

Break-Time exposes a command-line interface, not an HTTP API. Install from a checkout with Python 3.10 or newer, or run the script directly from the repository root.

~~~sh
python -m pip install .
break-time [--stat] [--commit --message MESSAGE] [--push]
~~~

Without installation, invoke the same interface with python python/daily_activity.py.

## Options

| Option | Description |
| --- | --- |
| No options | Print repository status and staged paths without changing the repository. |
| --stat | Show Git's staged insertion and deletion summary after paths pass safety checks. Can be combined with --commit. |
| --commit | Create one commit from already-staged files that pass path checks. Requires --message. |
| --message MESSAGE | Set the commit message. It is only valid with --commit and cannot be empty. |
| --push | Push the new commit to the current branch's origin remote. Requires --commit. |

The helper never stages files. Use Git to select the exact changes before invoking --commit. SAFE_PATHS controls allowed paths, and PROTECTED_PATHS always blocks a matching path.

## Exit status

- 0: preview succeeded, no staged changes were found, or the requested operation completed.
- 1: Git is unavailable, a Git command failed, or a command timed out.
- 2: command-line arguments are invalid, staged paths violate path policy, or the checkout is detached.

The Python functions in daily_activity.py are implementation details. The command-line options above are the supported interface.
