# TitanForge Demo Navigation Guide

**Quick access guide for 5 PM demo presentation**

---

## 🎯 For Sales Presentation

### Customer-Facing Materials Location
```
F:\TitanForge\docs\sales\
```

**Key Files to Show:**
- `QUICK_START_5MIN.md` - Fast onboarding demo
- `MARKETING_PLAYBOOK.md` - Product positioning
- `SALES_QUICK_REFERENCE.md` - Feature overview

---

## 🏢 For Operations Discussion

### Operational Documentation Location
```
F:\TitanForge\docs\operations\
```

**Key Files to Show:**
- `BUILD_AND_RUN.md` - System deployment
- `STRIPE_SETUP.md` - Payment integration
- `GO_LIVE_CHECKLIST.md` - Launch readiness
- `ARCHITECTURE_PLAN.md` - System design

---

## 📋 For Legal/Compliance

### Legal Documentation Location
```
F:\TitanForge\docs\legal\
```

**Files Available:**
- Privacy Policy
- Terms of Service
- Data Sale Agreement
- Affiliate Disclaimer

---

## 🧪 For Technical Demo

### Test Suites Location
```
F:\TitanForge\tests\
```

**Run Endpoint Tests:**
```bash
cd F:\TitanForge
pytest tests/endpoints/
```

**Run Integration Tests:**
```bash
pytest tests/integration/
```

**Run All Tests:**
```bash
pytest tests/
```

---

## 🚀 For Deployment Demo

### Startup Scripts Location
```
F:\TitanForge\scripts\deployment\
```

**Start Application:**
```powershell
.\scripts\deployment\start_titanforge.ps1
```

**Verify Production Ready:**
```powershell
.\scripts\deployment\VERIFY_PRODUCTION_READY.ps1
```

---

## 📊 Project Organization Overview

```
📁 F:\TitanForge
├── 📁 docs/ ................... All documentation
│   ├── 📁 sales/ .............. Sales materials (4 files)
│   ├── 📁 operations/ ......... Operational guides (12 files)
│   ├── 📁 legal/ .............. Legal docs (4 files)
│   └── PROJECT_STRUCTURE.md ... Master reference
├── 📁 tests/ .................. All test suites (8 files)
│   ├── endpoints/ ............. API tests (3 files)
│   ├── integration/ ........... E2E tests (4 files)
│   └── frontend/ .............. UI tests (1 file)
├── 📁 scripts/ ................ Automation scripts (5 files)
│   ├── setup/ ................. Setup scripts (2 files)
│   └── deployment/ ............ Launch scripts (3 files)
├── README.md .................. Main documentation
└── [Core config files] ........ Docker, package.json, .env
```

---

## ⚡ Demo Flow Recommendations

### 5-Minute Walkthrough
1. Show organized folder structure (40 sec)
2. Navigate to `/docs/sales/` and show marketing materials (1 min)
3. Show `/tests/` with runnable test suites (1 min)
4. Demonstrate deployment scripts in `/scripts/deployment/` (1 min)
5. Show PROJECT_STRUCTURE.md for completeness (1 min)

### 10-Minute Technical Demo
1. Show project organization (1 min)
2. Run endpoint tests: `pytest tests/endpoints/` (2 min)
3. Show updated import paths and robustness (1 min)
4. Demonstrate startup script: `.\scripts\deployment\start_titanforge.ps1` (2 min)
5. Show verification script: `.\scripts\deployment\VERIFY_PRODUCTION_READY.ps1` (2 min)
6. Q&A and discussion (2 min)

---

## 📞 Key Talking Points

### Organization
- ✅ 32 files reorganized into 3 main categories
- ✅ Documentation logically grouped by audience
- ✅ Tests organized by testing scope
- ✅ Scripts clearly separated by purpose

### Quality Assurance
- ✅ All import paths verified and updated
- ✅ No breaking changes - only reorganization
- ✅ All functionality preserved
- ✅ Professional structure demonstrates maturity

### Scalability
- ✅ Reserved directories for future expansion
- ✅ Clear naming conventions for easy navigation
- ✅ Modular organization supports team growth

---

## 🔗 Quick Links to Key Documents

| Purpose | File | Location |
|---------|------|----------|
| Overview | PROJECT_STRUCTURE.md | docs/ |
| Summary Report | REORGANIZATION_REPORT.md | docs/ |
| This Guide | DEMO_NAVIGATION_GUIDE.md | docs/ |
| Main README | README.md | root |
| Product Info | PRODUCT_CATALOG.md | root |

---

## 💡 Pro Tips for Demo

1. **Before presenting:** Run `pytest tests/endpoints/` to verify all tests pass
2. **Use file explorer:** Open root directory to show clean, organized structure
3. **Highlight modularity:** Point out reserved directories for future features
4. **Show documentation:** Open `/docs/` in VSCode explorer for visual organization
5. **Mention improvements:** Reference REORGANIZATION_REPORT.md for detailed changes

---

**Ready to impress! All materials organized and tested.** ✅
