"""Configuration for the staged-change Git helper."""

# Kept temporarily for compatibility with older config readers. The current CLI
# does not choose or enforce a commit count.
MIN_COMMITS = 1
MAX_COMMITS = 1

# Only staged changes under these paths can be committed by the helper.
SAFE_PATHS = (
    ".gitignore",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "docs/",
    "python/",
    "tests/",
    ".github/",
)

# Sensitive and generated paths are refused even if a future allowlist includes them.
PROTECTED_PATHS = (
    ".env",
    ".env.*",
    ".git/",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    "*.pem",
    "*.key",
    "*.log",
    ".DS_Store",
    "secrets/",
)

LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, or CRITICAL
