# Setup

Break-Time runs as a local Python command-line tool. It has no third-party runtime dependencies and does not require a GitHub Actions workflow.

## Requirements

- Python 3.10 or newer
- Git installed and available on PATH
- A Git checkout with the intended project changes staged

## Run from a checkout

Clone the repository and move to its root:

~~~sh
git clone https://github.com/Arish0limbu/Break-TIme.git
cd Break-TIme
~~~

Stage only real changes, then preview the staged file list:

~~~sh
git add README.md
python python/daily_activity.py
~~~

The preview is read-only. To create one commit after reviewing the staged files, pass a message explicitly:

~~~sh
python python/daily_activity.py --commit --message "docs: clarify setup"
~~~

Add --push only when you want the helper to push that new commit to origin.

## Configuration

Edit python/config.py to update SAFE_PATHS and PROTECTED_PATHS. Protected patterns always take precedence. The helper preserves the identity configured in your local Git settings; inspect it with:

~~~sh
git config user.name
git config user.email
~~~

No token, workflow permission, or log directory is needed.
