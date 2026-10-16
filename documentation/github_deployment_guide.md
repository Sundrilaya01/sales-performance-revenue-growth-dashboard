# GitHub Deployment & Version Control Guide

**Project:** Sales Performance & Revenue Growth Dashboard  
**Phase:** Phase 8 — Publishing Guidance and Portfolio Preparation  
**Role:** Senior BI Delivery Engineer & Technical Documentation Specialist  
**Governance Standard:** Zero Secret Leakage & Controlled Public Release  

---

## 1. Overview & Policy Warning

> [!WARNING]
> **Authorization Policy:** In accordance with Phase 8 operational constraints, the local Git repository must not be pushed to GitHub or made public without explicit authorization from the Technical Project Manager. Follow the instructions below only when authorized to stage, commit, and link to a remote repository.

---

## 2. Step-by-Step GitHub Deployment Procedure

### Step 1: Verify Pre-Staging Cleanliness & `.gitignore`
Before initializing or staging files, ensure that the project root contains the approved [`.gitignore`](file:///d:/Power%20BI/Sales%20Performance%20&%20Revenue%20Growth%20Dashboard/.gitignore) to exclude:
- Bytecode / cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`.venv/`, `env/`)
- Local secrets, tokens, or credential JSONs (`*.env`, `credentials.json`)
- Power BI local recovery caches (`*.tmp`, `*.pbi.cache`)
- Operating system files (`Thumbs.db`, `.DS_Store`)

Run the following PowerShell command from the project root:
```powershell
# Check that .gitignore exists and verify tracked file boundaries
Get-Content -Path ".gitignore" -TotalCount 15
```

---

### Step 2: Initialize Git Repository
From the project root (`D:\Power BI\Sales Performance & Revenue Growth Dashboard`):

```powershell
# 1. Initialize local Git repository (if not already initialized)
git init

# 2. Configure default branch to main
git branch -M main

# 3. Verify user name and email are configured
git config user.name "Your Name"
git config user.email "your.email@domain.com"
```

---

### Step 3: Review Working-Tree Status
Inspect all untracked and modified files before staging:

```powershell
git status
```
*Verify that only approved project files appear in untracked files:*
- `README.md`
- `.gitignore`
- `data/` (`data/raw/sales_performance_dataset.csv`, `data/processed/*.csv`)
- `scripts/` (`*.py`, `*.m`, `*.dax`, `*.json`)
- `docs/` (`*.md`)
- `documentation/` (`business_case/*.md`, `publishing_guide.md`, `github_deployment_guide.md`)
- `screenshots/` (mockups / visual assets)

---

### Step 4: Stage Approved Files
Stage files cleanly into the index:

```powershell
# Stage all approved project files
git add .

# Confirm staged items
git status
```

---

### Step 5: Create Initial Production Commit
Create a descriptive, professional commit message:

```powershell
git commit -m "feat: complete initial release of Sales Performance & Revenue Growth Dashboard

- Preprocessed and normalized raw sales data into Star Schema
- Engineered 11 verified DAX measures and continuous calendar table
- Formulated executive 16:9 dashboard layout specification and theme JSON
- Built Holt-Winters ETS time-series forecasting engine with H1 2026 projections
- Documented business case, claim validation register, technical architecture, and ROI framework
- Added automated validation test suites for 100% mathematical parity"
```

---

### Step 6: Link to Remote GitHub Repository (Requires User Authorization)
Once an empty repository has been created on GitHub under your account (e.g. `https://github.com/<your-username>/sales-performance-dashboard.git`):

```powershell
# Link remote origin
git remote add origin https://github.com/<your-username>/sales-performance-dashboard.git

# Verify remote configuration
git remote -v
```

---

### Step 7: Push Approved Branch
Push your validated `main` branch to the remote repository:

```powershell
# Push to GitHub
git push -u origin main
```

---

### Step 8: Post-Push Verification Checklist
After pushing:
1. Open the repository URL in your web browser.
2. Confirm the root `README.md` renders cleanly with active markdown links.
3. Verify that zero private credentials, `.env` files, or temporary cache files were pushed.
4. Confirm dataset files (`data/raw/` and `data/processed/`) display properly.
5. Verify commit history displays clean, atomic messages.
