# Contributing

Thanks for taking the time to improve Break-Time.

## Development setup

- Python 3.10 or newer
- Git installed and available on PATH

Clone the repository, make a focused change, and review the result before committing it.

## Project guidelines

- Keep commits tied to real code, documentation, or maintenance work.
- Do not add scheduled commit targets or automated filler edits.
- Preserve the Git identity configured by the contributor.
- Keep the helper read-only by default and require explicit flags for commits and pushes.
- Update SAFE_PATHS or PROTECTED_PATHS only when the change requires it.
- Keep documentation consistent with the current CLI behavior.

## Review your staged changes

Stage only the files that belong to your change, then inspect the helper's read-only preview:

~~~sh
git add path/to/changed-file
python python/daily_activity.py
~~~

The helper refuses staged files that are outside SAFE_PATHS or match PROTECTED_PATHS. It never stages files itself.

## Commit and submit

Use a concise message that describes the change. Open a pull request for review when contributing from a fork or feature branch.
