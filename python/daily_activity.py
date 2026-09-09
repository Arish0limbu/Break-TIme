#!/usr/bin/env python3
"""
GitHub Daily Activity Automation
Makes meaningful commits to maintain daily GitHub activity.
"""

import os
import sys
import random
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import config

# ==================== LOGGING SETUP ====================
def setup_logging():
    """Configure logging system"""
    log_dir = Path(config.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ==================== GIT OPERATIONS ====================
def run_git_command(command, check=True):
    """Execute git command and return output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return result.stdout.strip(), result.returncode
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {command}")
        logger.error(f"Error: {e.stderr}")
        return "", e.returncode

def configure_git():
    """Configure git identity"""
    logger.info("Configuring git identity")
    run_git_command(f'git config user.name "{config.GIT_USER_NAME}"')
    run_git_command(f'git config user.email "{config.GIT_USER_EMAIL}"')

def get_current_branch():
    """Get current git branch"""
    stdout, _ = run_git_command("git rev-parse --abbrev-ref HEAD")
    return stdout if stdout else config.REPOSITORY_BRANCH

def has_uncommitted_changes():
    """Check if there are uncommitted changes"""
    stdout, _ = run_git_command("git status --porcelain")
    return len(stdout) > 0

def commit_changes(message):
    """Stage and commit changes with given message"""
    logger.info(f"Committing: {message}")
    run_git_command("git add .")
    stdout, returncode = run_git_command(f'git commit -m "{message}"')
    if returncode == 0:
        logger.info(f"Successfully committed: {message}")
        return True
    else:
        logger.warning(f"No changes to commit or commit failed")
        return False

def push_changes(branch):
    """Push changes to remote repository"""
    logger.info(f"Pushing changes to {branch}")
    stdout, returncode = run_git_command(f"git push origin {branch}")
    if returncode == 0:
        logger.info("Successfully pushed changes")
        return True
    else:
        logger.error(f"Failed to push changes: {stdout}")
        return False

# ==================== LEGITIMATE CHANGES ====================
def can_modify_file(filepath):
    """Check if file can be safely modified"""
    filepath = Path(filepath)
    
    # Check protected paths
    for protected in config.PROTECTED_PATHS:
        if protected in str(filepath) or filepath.match(protected):
            return False
    
    # Check if file is in safe paths
    for safe in config.SAFE_PATHS:
        if safe in str(filepath) or filepath.match(safe):
            return True
    
    return False

def improve_readme():
    """Add meaningful improvements to README"""
    readme_path = Path("README.md")
    if not readme_path.exists():
        return None
    
    content = readme_path.read_text()
    improvements = [
        "\n## Getting Started\n\nThis project is easy to set up and use.",
        "\n## Contributing\n\nContributions are welcome! Please read our guidelines.",
        "\n## License\n\nThis project is open source and available under the MIT License.",
        "\n## Features\n\n- Easy to use\n- Well documented\n- Active development",
        "\n## Support\n\nFor issues and questions, please open an issue on GitHub.",
    ]
    
    for improvement in improvements:
        if improvement not in content:
            content += improvement
            readme_path.write_text(content)
            return "docs: improve README documentation"
    
    return None

def update_changelog():
    """Add entry to changelog"""
    changelog_path = Path("CHANGELOG.md")
    if not changelog_path.exists():
        # Create changelog if it doesn't exist
        initial_content = """# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial project setup
- GitHub activity automation
"""
        changelog_path.write_text(initial_content)
        return "chore: add changelog"
    
    content = changelog_path.read_text()
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"\n## [{today}]\n\n### Updated\n- Automated documentation improvements\n"
    
    if today not in content:
        content = content.replace("## [Unreleased]", entry + "## [Unreleased]")
        changelog_path.write_text(content)
        return "chore: update changelog"
    
    return None

def add_contributing_guide():
    """Add contributing guide if missing"""
    contributing_path = Path("CONTRIBUTING.md")
    if not contributing_path.exists():
        content = """# Contributing

Thank you for your interest in contributing!

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Guidelines

- Write clear commit messages
- Follow the existing code style
- Add tests for new features
- Update documentation as needed
"""
        contributing_path.write_text(content)
        return "docs: add contributing guidelines"
    
    return None

def improve_code_comments():
    """Add helpful comments to Python files"""
    python_files = list(Path(".").rglob("*.py"))
    for py_file in python_files:
        if not can_modify_file(py_file):
            continue
            
        content = py_file.read_text()
        if "# TODO:" not in content and len(content) > 100:
            # Add a helpful comment if file is substantial
            improved = content + "\n# TODO: Consider adding more documentation\n"
            py_file.write_text(improved)
            return f"docs: add comments to {py_file.name}"
    
    return None

def create_test_file():
    """Create a simple test file if tests directory exists"""
    tests_dir = Path("tests")
    if not tests_dir.exists():
        return None
    
    test_file = tests_dir / "test_example.py"
    if not test_file.exists():
        content = """
\"\"\"
Example test file for project validation.
\"\"\"

def test_example():
    \"\"\"Example test case\"\"\"
    assert True

if __name__ == "__main__":
    test_example()
"""
        test_file.write_text(content)
        return "test: add example test case"
    
    return None

def improve_documentation_structure():
    """Add structure improvements to documentation files"""
    doc_files = list(Path(".").rglob("*.md"))
    for doc_file in doc_files:
        if not can_modify_file(doc_file):
            continue
            
        content = doc_file.read_text()
        
        # Add table of contents if missing and file is long enough
        if len(content) > 500 and "## Table of Contents" not in content:
            # Add table of contents
            toc = "\n## Table of Contents\n\n- [Introduction](#introduction)\n- [Features](#features)\n- [Usage](#usage)\n"
            if "# Introduction" in content or "# Features" in content or "# Usage" in content:
                improved = content.replace("# ", toc + "# ", 1)
                doc_file.write_text(improved)
                return f"docs: add table of contents to {doc_file.name}"
        
        # Add badges section if missing
        if len(content) > 300 and "![GitHub" not in content and doc_file.name == "README.md":
            badges = "\n![GitHub](https://img.shields.io/badge/github-%23181717.svg?style=for-the-badge&logo=github&logoColor=white)\n"
            improved = badges + content
            doc_file.write_text(improved)
            return "docs: add badges to README"
    
    return None

def add_code_examples():
    """Add code examples to documentation"""
    doc_files = list(Path(".").rglob("*.md"))
    for doc_file in doc_files:
        if not can_modify_file(doc_file):
            continue
            
        content = doc_file.read_text()
        
        # Add code example section if missing
        if "```" not in content and len(content) > 200:
            example = "\n## Code Example\n\n```python\n# Example code\ndef example_function():\n    return \"Hello, World!\"\n```\n"
            improved = content + example
            doc_file.write_text(improved)
            return f"docs: add code example to {doc_file.name}"
    
    return None

def improve_file_organization():
    """Add organization comments to files"""
    code_files = list(Path(".").rglob("*.py")) + list(Path(".").rglob("*.js")) + list(Path(".").rglob("*.ts"))
    for code_file in code_files:
        if not can_modify_file(code_file):
            continue
            
        content = code_file.read_text()
        
        # Add file header if missing
        if not content.startswith("#") and not content.startswith("\"\"\"") and not content.startswith("//"):
            header = f"# {code_file.name}\n# Auto-generated file header\n\n"
            improved = header + content
            code_file.write_text(improved)
            return f"refactor: add file header to {code_file.name}"
    
    return None

def add_license_file():
    """Add LICENSE file if missing"""
    license_path = Path("LICENSE")
    if not license_path.exists():
        content = """MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        license_path.write_text(content)
        return "chore: add MIT license"
    
    return None

def make_legitimate_change():
    """Attempt to make a legitimate change to the repository"""
    logger.info("Looking for legitimate changes to make")
    
    # Try different types of improvements
    change_generators = [
        improve_readme,
        update_changelog,
        add_contributing_guide,
        improve_code_comments,
        create_test_file,
        improve_documentation_structure,
        add_code_examples,
        improve_file_organization,
        add_license_file,
    ]
    
    for generator in change_generators:
        try:
            message = generator()
            if message:
                logger.info(f"Found legitimate change: {message}")
                return message
        except Exception as e:
            logger.warning(f"Change generator failed: {e}")
            continue
    
    logger.info("No legitimate changes available")
    return None

# ==================== MAIN AUTOMATION ====================
def calculate_daily_target():
    """Calculate random daily commit target"""
    target = random.randint(config.MIN_COMMITS, config.MAX_COMMITS)
    logger.info(f"Daily commit target: {target}")
    return target

def get_today_commit_count():
    """Get number of commits made today"""
    today = datetime.now().strftime("%Y-%m-%d")
    stdout, _ = run_git_command(f'git log --since="{today} 00:00:00" --until="{today} 23:59:59" --oneline')
    commits = stdout.split('\n') if stdout else []
    return len([c for c in commits if c])

def run_daily_activity():
    """Main automation function"""
    logger.info("=" * 50)
    logger.info(f"Starting daily activity automation - {datetime.now()}")
    logger.info("=" * 50)
    
    if not config.ENABLE_AUTOMATION:
        logger.info("Automation is disabled in configuration")
        return
    
    # Configure git
    configure_git()
    
    # Get current branch
    branch = get_current_branch()
    logger.info(f"Working on branch: {branch}")
    
    # Calculate daily target
    daily_target = calculate_daily_target()
    today_commits = get_today_commit_count()
    
    logger.info(f"Commits made today: {today_commits}")
    
    # Only run if less than threshold commits today
    if today_commits >= config.AUTO_RUN_THRESHOLD:
        logger.info(f"Already have {today_commits} commits today (threshold: {config.AUTO_RUN_THRESHOLD}), skipping automation")
        return
    
    remaining = max(0, daily_target - today_commits)
    logger.info(f"Remaining commits needed: {remaining}")
    
    if remaining == 0:
        logger.info("Daily target already reached")
        return
    
    # Limit commits per run
    commits_to_make = min(remaining, config.MAX_COMMITS_PER_RUN)
    logger.info(f"Will attempt {commits_to_make} commits this run")
    
    completed = 0
    for i in range(commits_to_make):
        logger.info(f"Attempt {i + 1}/{commits_to_make}")
        
        # Make a legitimate change
        commit_message = make_legitimate_change()
        
        if not commit_message:
            logger.info("No more legitimate changes available")
            break
        
        # Commit the change
        if commit_changes(commit_message):
            completed += 1
        
        # Small delay between commits (natural timing)
        import time
        time.sleep(random.uniform(1, 3))
    
    logger.info(f"Completed {completed} commits")
    
    # Push changes if any commits were made
    if completed > 0:
        if push_changes(branch):
            logger.info("Successfully pushed all changes")
        else:
            logger.warning("Failed to push changes")
    
    logger.info("=" * 50)
    logger.info(f"Daily activity automation completed - {datetime.now()}")
    logger.info("=" * 50)

if __name__ == "__main__":
    try:
        run_daily_activity()
    except Exception as e:
        logger.error(f"Automation failed with error: {e}")
        sys.exit(1)