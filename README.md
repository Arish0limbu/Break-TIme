# GitHub Daily Activity Automation

A professional automation system for maintaining meaningful daily GitHub activity through legitimate contributions to your repository.

## 🎯 Features

- **Smart Commit Targeting**: Generates 5-20 meaningful commits per day (configurable)
- **Real Work Only**: Each commit represents legitimate improvements to your codebase
- **Natural Timing**: Distributes commits throughout the day with randomized timing
- **Safety First**: Never modifies secrets, never creates fake commits
- **Professional Logging**: Tracks all activity with detailed logs
- **Easy Configuration**: Simple settings file for customization

## 📋 What This Automation Does

This system makes **only legitimate changes** to your repository:

- ✅ Updates documentation (README, CHANGELOG, etc.)
- ✅ Improves code structure and comments
- ✅ Adds test cases
- ✅ Updates project configuration
- ✅ Refactors existing code
- ✅ Adds contributing guidelines

**What it does NOT do:**
- ❌ Create fake/spam commits
- ❌ Modify the same file repeatedly just to generate commits
- ❌ Touch secrets, API keys, or `.env` files
- ❌ Make meaningless whitespace-only changes
- ❌ Rewrite git history or force-push

## 🚀 Quick Setup

### 1. Repository Setup

#### Option A: New Repository

```bash
# Initialize your repository
git init
git add .
git commit -m "Initial commit: Add GitHub activity automation"

# Create repository on GitHub, then add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

#### Option B: Existing Repository

Simply copy the automation files to your existing repository:

```bash
# Copy these files to your repository:
- .github/workflows/daily-activity.yml
- python/daily_activity.py
- python/config.py
- logs/ (directory)
```

### 2. GitHub Configuration

#### Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Under **Actions permissions**, select:
   - **"Allow all actions and reusable workflows"**
4. Click **Save**

#### Workflow Permissions

1. In **Settings** → **Actions** → **General**
2. Scroll to **Workflow permissions**
3. Select **"Read and write permissions"**
4. Check **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**

#### Branch Protection (Optional but Recommended)

1. Go to **Settings** → **Branches**
2. Add rule for your main branch
3. Enable:
   - **Require a pull request before merging**
   - **Require status checks to pass before merging**
   - **Require branches to be up to date before merging**

### 3. Customize Configuration

Edit `python/config.py` to customize settings:

```python
# Commit Settings
MIN_COMMITS = 5           # Minimum commits per day
MAX_COMMITS = 20          # Maximum commits per day
MAX_COMMITS_PER_RUN = 10  # Maximum commits per script execution

# Automation Control
ENABLE_AUTOMATION = True  # Set to False to disable

# Repository Settings
REPOSITORY_BRANCH = "main"  # Branch to commit to
GIT_USER_NAME = "GitHub Actions"
GIT_USER_EMAIL = "actions@github.com"

# Safe Paths (files automation can modify)
SAFE_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "docs/",
    "python/",
    "tests/",
    # Add your project-specific paths
]
```

### 4. Push to GitHub

```bash
git add .
git commit -m "Add GitHub activity automation"
git push origin main
```

## 🧪 Testing the Workflow

### Manual Testing

#### Test Locally

```bash
# Navigate to your repository
cd /path/to/your/repository

# Run the script manually
cd python
python daily_activity.py
```

#### Test via GitHub Actions

1. Go to your repository on GitHub
2. Click **Actions** tab
3. Select **Daily Activity Automation** workflow
4. Click **Run workflow** → **Run workflow**
5. Monitor the execution in real-time

### Check Logs

After running, check the activity log:

```bash
cat logs/activity.log
```

Or download from GitHub Actions:
1. Go to **Actions** tab
2. Click on the workflow run
3. Download the `activity-log` artifact

## 🔧 How It Works

### Daily Schedule

The workflow runs automatically on a schedule:
- **Frequency**: Daily
- **Time**: Random hour between 9 AM - 11 PM UTC
- **Trigger**: GitHub Actions cron schedule

### Commit Process

1. **Calculate Target**: Random number between MIN_COMMITS and MAX_COMMITS
2. **Check Progress**: Count today's existing commits
3. **Find Work**: Identify legitimate improvements needed
4. **Make Changes**: Apply meaningful updates
5. **Commit**: Create professional commit messages
6. **Push**: Sync changes to GitHub
7. **Log**: Record all activity

### Commit Message Examples

```
docs: improve project documentation
docs: update README
refactor: improve code structure
test: add validation cases
fix: correct input validation
chore: update project configuration
docs: add contributing guidelines
chore: update changelog
```

## 🛑 Disabling the Automation

### Temporary Disable

Edit `python/config.py`:

```python
ENABLE_AUTOMATION = False
```

Commit and push:

```bash
git add python/config.py
git commit -m "chore: temporarily disable automation"
git push origin main
```

### Permanent Disable

#### Option 1: Delete Workflow

```bash
git rm .github/workflows/daily-activity.yml
git commit -m "chore: remove daily activity automation"
git push origin main
```

#### Option 2: Disable in GitHub

1. Go to **Settings** → **Actions** → **General**
2. Select **"Disable all workflows"**
3. Or disable specific workflow in **Actions** tab

## 📊 Monitoring

### View Activity

1. Go to your repository on GitHub
2. Click **Actions** tab
3. View workflow runs and logs
4. Check contribution graph for green squares

### Log Format

```
2026-09-07 10:00:00 - INFO - ==================================================
2026-09-07 10:00:00 - INFO - Starting daily activity automation - 2026-09-07 10:00:00
2026-09-07 10:00:00 - INFO - ==================================================
2026-09-07 10:00:01 - INFO - Daily commit target: 12
2026-09-07 10:00:01 - INFO - Commits made today: 0
2026-09-07 10:00:01 - INFO - Remaining commits needed: 12
2026-09-07 10:00:01 - INFO - Will attempt 10 commits this run
2026-09-07 10:00:02 - INFO - Looking for legitimate changes to make
2026-09-07 10:00:03 - INFO - Found legitimate change: docs: improve README documentation
2026-09-07 10:00:04 - INFO - Committing: docs: improve README documentation
2026-09-07 10:00:05 - INFO - Successfully committed: docs: improve README documentation
...
```

## 🔒 Security Features

- ✅ Uses GitHub's built-in `GITHUB_TOKEN` (no personal tokens needed)
- ✅ Never commits `.env` files or secrets
- ✅ Protected paths prevent accidental modifications
- ✅ Read-only access to sensitive files
- ✅ No force-push or history rewriting
- ✅ Safe branch handling

## 📁 Project Structure

```
project/
├── .github/
│   └── workflows/
│       └── daily-activity.yml    # GitHub Actions workflow
├── python/
│   ├── daily_activity.py         # Main automation script
│   └── config.py                  # Configuration settings
├── logs/
│   └── activity.log              # Activity logs
└── README.md                     # This file
```

## 🤝 Contributing

This automation is designed to help you maintain legitimate GitHub activity. The system will:

- Add to your documentation
- Improve code quality
- Create helpful tests
- Update project metadata

Feel free to customize the change generators in `daily_activity.py` to match your project's needs.

## ⚠️ Important Notes

1. **Real Work Only**: This system only makes legitimate improvements. If no legitimate work is available, it stops rather than creating fake commits.

2. **GitHub Limits**: Be aware of GitHub's API rate limits and abuse policies. The default settings (5-20 commits/day) are well within safe limits.

3. **Branch Protection**: If you have branch protection rules, you may need to adjust them or the automation workflow accordingly.

4. **Team Repositories**: For team repositories, ensure team members are aware of this automation and that it aligns with your contribution guidelines.

## 📝 License

This automation system is provided as-is for maintaining legitimate GitHub activity. Use responsibly and in accordance with GitHub's terms of service.

## 🆘 Troubleshooting

### Workflow Not Running

- Check GitHub Actions are enabled in repository settings
- Verify workflow permissions allow read/write access
- Ensure the workflow file is in the correct location

### Commits Not Appearing

- Check the activity log for errors
- Verify git configuration is correct
- Ensure branch name matches your repository

### Permission Errors

- Verify workflow permissions in GitHub settings
- Check that `GITHUB_TOKEN` has sufficient permissions
- Ensure branch protection rules allow automation

### No Legitimate Changes Available

- Add more files to `SAFE_PATHS` in config
- Create more documentation to improve
- Add test cases or code comments that can be enhanced

---

**Generated with [Devin](https://devin.ai)**

**Remember**: This automation creates only legitimate, meaningful contributions. Use it to maintain a healthy, active repository while genuinely improving your project.