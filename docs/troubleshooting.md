# Troubleshooting

## The preview says there are no staged changes

Stage the files you intend to include, then run the preview again:

~~~sh
git status --short
git add path/to/changed-file
python python/daily_activity.py
~~~

Unstaged and untracked files are left untouched.

## A staged path is refused

The helper commits only paths in SAFE_PATHS. A path matching PROTECTED_PATHS is always refused. Review python/config.py and adjust the policy only when the path is appropriate for this repository. Remove secrets and generated files from the Git index before retrying.

## Git cannot find a repository

Run the command from inside a Git checkout. The helper searches upward from the current directory for the repository root.

## Git is unavailable

Install Git and confirm the executable is available on PATH. Python 3.10 or newer is also required.

## The commit is rejected

The helper uses your local Git author identity and commits only the staged index. Check git status, branch protection, hooks, and your repository's commit policy. It does not change your Git identity.

## A push fails

A push is attempted only with --push. The commit remains in your local branch if the push fails. Check that origin exists, you have access, and the branch permits direct pushes; then push manually or use your normal pull request process.

## The checkout is detached

Switch to a named branch before asking the helper to create a commit.
