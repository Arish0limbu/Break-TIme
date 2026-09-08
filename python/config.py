"""
Configuration for GitHub Daily Activity Automation
"""

# ==================== COMMIT SETTINGS ====================
MIN_COMMITS = 10          # Minimum commits per day
MAX_COMMITS = 20          # Maximum commits per day
MAX_COMMITS_PER_RUN = 10  # Maximum commits per script execution
AUTO_RUN_THRESHOLD = 9    # Only run automation if today's commits < this number

# ==================== AUTOMATION CONTROL ====================
ENABLE_AUTOMATION = True  # Set to False to disable automation

# ==================== REPOSITORY SETTINGS ====================
REPOSITORY_BRANCH = "main"  # Branch to commit to
GIT_USER_NAME = "GitHub Actions"  # Git user name for commits
GIT_USER_EMAIL = "actions@github.com"  # Git user email for commits

# ==================== SAFE PATHS ====================
# Files and directories that automation may modify
# Add your project-specific paths here
SAFE_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "docs/",
    "python/",
    "tests/",
    ".github/",
    "CONTRIBUTING.md",
    "LICENSE",
]

# ==================== PROTECTED PATHS ====================
# Files that automation should NEVER modify
PROTECTED_PATHS = [
    ".env",
    ".git",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "secrets/",
    "config.py",
]

# ==================== LOGGING ====================
LOG_FILE = "logs/activity.log"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL