# How to Push Nigiri to a New GitHub Repository

This guide shows you how to push the nigiri Python bindings to a new repository.

## Current Status

✅ **Done:**
- Nigiri is initialized as a separate git repository
- All files are committed (262 files)
- Nigiri is excluded from the goat repository (added to .gitignore)
- Build artifacts are ignored (.gitignore configured)

📍 **Location:** `/app/packages/cpp/nigiri/`

## Step 1: Create a New GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., `nigiri-python-wheel`)
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Copy the repository URL (e.g., `https://github.com/YOUR_USERNAME/nigiri-python-wheel.git`)

## Step 2: Add Remote and Push

```bash
cd /app/packages/cpp/nigiri

# Add your new GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/nigiri-python-wheel.git

# Rename the default branch from 'master' to 'main' (optional but recommended)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Step 3: Verify on GitHub

Visit your repository on GitHub to confirm:
- All 262 files are present
- Build artifacts (build/, dist/, *.so) are NOT present (correctly ignored)
- README_REPO.md, BUILD_GUIDE.md, and other docs are visible

## What's Included in the Repository

### Source Files (tracked by git)
- All C++ source code (include/, src/)
- Python bindings (python/)
- Build configuration (CMakeLists.txt, setup.py, pyproject.toml)
- Build scripts (build_wheel.sh, test_wheel.sh)
- Documentation (README_REPO.md, BUILD_GUIDE.md, CHANGES.md)
- Python package (nigiri/__init__.py)
- Test scripts (test_import.py)

### Build Artifacts (ignored by git)
- build/ directory (~500MB)
- dist/ directory with wheel file (~2.3MB)
- nigiri.egg-info/
- *.so files (compiled extensions)
- .pkg, .pkg.lock, .pkg.mutex

## Alternative: Push to a Different Branch in Existing Repo

If you prefer to keep it in the same organization but separate branch:

```bash
cd /app/packages/cpp/nigiri

# Add the goat repo as remote with a different name
git remote add goat-repo https://github.com/plan4better/goat.git

# Create a new branch for nigiri
git checkout -b nigiri-python-bindings

# Push to a separate branch
git push -u goat-repo nigiri-python-bindings
```

Then you can access it at:
`https://github.com/plan4better/goat/tree/nigiri-python-bindings/packages/cpp/nigiri`

## Maintaining Both Repositories

### To update nigiri repository:
```bash
cd /app/packages/cpp/nigiri
# Make changes...
git add .
git commit -m "Your commit message"
git push
```

### Goat repository won't track nigiri anymore:
The `packages/cpp/nigiri/` directory is now in .gitignore, so the goat repo won't see any changes inside it.

## Repository README

The repository includes `README_REPO.md` as the main README. You may want to:
1. Rename it: `mv README_REPO.md README.md` (then commit)
2. Or keep both (README.md from original nigiri, README_REPO.md for wheel build)

## Next Steps

1. Create GitHub repository
2. Push using commands above
3. Add description and tags on GitHub
4. Consider adding:
   - GitHub Actions for automated wheel building
   - Release workflow for distributing wheels
   - Issue templates
   - Contributing guidelines

## Troubleshooting

### Authentication Error
Use a personal access token instead of password:
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/repo.git
```

### Already Have a Remote
```bash
git remote remove origin
git remote add origin NEW_URL
```

### Want to Review Before Pushing
```bash
git log --oneline
git diff HEAD~1 HEAD  # See what changed in last commit
git show HEAD         # See full details of last commit
```

## Additional Notes

- The original nigiri README.md is preserved
- BUILD_GUIDE.md has complete build instructions
- CHANGES.md documents all modifications made
- The .gitignore is configured to keep the repository clean

---

**Ready to push!** Just create your GitHub repo and run the commands in Step 2.
