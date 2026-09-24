# CLI reference

Break-Time exposes a command-line interface, not an HTTP API. Run it from anywhere inside a Git checkout with Python 3.10 or newer.

~~~sh
python python/daily_activity.py [--commit --message MESSAGE] [--push]
~~~

## Options

| Option | Description |
| --- | --- |
| No options | Print repository status and staged paths without changing the repository. |
| --commit | Create one commit from already-staged files that pass path checks. Requires --message. |
| --message MESSAGE | Set the commit message. It is only valid with --commit. |
| --push | Push the new commit to the current branch's origin remote. Requires --commit. |

The helper never stages files. Use Git to select the exact changes before invoking --commit. SAFE_PATHS controls allowed paths, and PROTECTED_PATHS always blocks a matching path.

## Exit status

- 0: preview succeeded, no staged changes were found, or the requested operation completed.
- 1: a Git command failed, Git is unavailable, or a command timed out.
- 2: staged files violate path policy or the current checkout is detached.

The Python functions in daily_activity.py are implementation details. The command-line flags above are the supported interface.
