# TitanForge Project Structure

## Overview
This document describes the reorganized folder structure of the TitanForge project. All documentation, tests, and scripts have been categorized and organized into logical subdirectories for better discoverability and maintainability.

**Reorganization Date:** Current Session  
**Total Files Organized:** 32 files across 3 categories

---

## Directory Structure

### 📁 `/docs` - Documentation (19 files)

All project documentation is organized by functional category:

#### `/docs/sales` (4 files)
Customer-facing and sales team documentation
- `QUICK_START_5MIN.md` - Quick start guide for new users
- `SALES_QUICK_REFERENCE.md` - Quick reference for sales team
- `SALES_TEAM_STARTUP_GUIDE.md` - Onboarding guide for sales
- `MARKETING_PLAYBOOK.md` - Marketing strategy and tactics

#### `/docs/operations` (11 files)
Operational documentation for deployment, setup, and management
- `ANALYTICS_SETUP.md` - Analytics configuration
- `ARCHITECTURE_PLAN.md` - System architecture overview
- `BUILD_AND_RUN.md` - Build and deployment instructions
- `GO_LIVE_CHECKLIST.md` - Pre-launch checklist
- `STRIPE_SETUP.md` - Stripe payment system setup
- `MONETIZATION_AUDIT.md` - Monetization audit report
- `MONETIZATION_REPORT.md` - Monetization strategy report
- `SCALABILITY_BLUEPRINT.md` - System scalability guidelines
- `how_to_get_jwt_token.md` - JWT token retrieval guide
- `seed_product_db_commands.md` - Database seeding commands
- `seed_product_db_powershell_commands.md` - PowerShell database seeding
- `user_instruction_for_stripe_products.md` - Stripe product setup guide

#### `/docs/legal` (4 files)
Legal and compliance documentation
- `AFFILIATE_DISCLAIMER.md` - Affiliate program disclaimer
- `DATA_SALE_AGREEMENT.md` - Data sale agreement template
- `PRIVACY_POLICY.md` - Privacy policy
- `TERMS_OF_SERVICE.md` - Terms of service

#### `/docs/agents` (0 files - reserved)
Reserved for future agent-related documentation

---

### 🧪 `/tests` - Test Suites (8 files)

All test files are organized by testing scope:

#### `/tests/endpoints` (3 files)
API endpoint and backend functionality tests
- `test_all_endpoints.py` - Comprehensive endpoint testing
- `test_backend.py` - Backend initialization and core tests
- `test_phase2_endpoints.py` - Phase 2 endpoint validation

#### `/tests/integration` (4 files)
End-to-end and integration tests
- `test_complete_journey.py` - Full user journey testing
- `test_comprehensive_integration.py` - Comprehensive system integration
- `test_comprehensive_phases.py` - Multi-phase integration testing
- `test_launch_components.py` - Launch component validation

#### `/tests/frontend` (1 file)
Frontend integration testing
- `test_frontend_integration.py` - Frontend API integration tests

#### `/tests/auth` (0 files - reserved)
Reserved for authentication-specific tests

#### `/tests/agents` (0 files - reserved)
Reserved for agent-related tests

---

### 🛠️ `/scripts` - Automation Scripts (5 files)

All utility and deployment scripts organized by purpose:

#### `/scripts/setup` (2 files)
Setup and configuration scripts
- `setup_stripe_products.py` - Stripe product catalog setup
- `STEPS_5_TO_10_IMPLEMENTATION.py` - Implementation workflow automation

#### `/scripts/deployment` (3 files)
Deployment and management scripts
- `LAUNCH_COMPONENTS_REPORT.ps1` - Launch component status report
- `VERIFY_PRODUCTION_READY.ps1` - Production readiness verification
- `start_titanforge.ps1` - Application startup script

#### `/scripts/utilities` (0 files - reserved)
Reserved for future utility scripts

---

## Root Directory (/TitanForge)

### Configuration Files
- `.env` - Environment variables
- `.env.example` - Example environment configuration
- `.gitignore` - Git ignore patterns
- `.dockerignore` - Docker ignore patterns
- `docker-compose.yml` - Docker composition configuration
- `package.json` - Node.js dependencies
- `package-lock.json` - Locked Node.js dependencies

### Core Documentation (Kept in Root)
- `README.md` - Main project README
- `PRODUCT_CATALOG.md` - Product reference information
- `SECRETS_VAULT.md` - Secrets management reference

### Project Files
- `FINAL_TEST_REPORT.txt` - Final test results
- `LAUNCH_COMPLETION_REPORT.txt` - Launch completion report
- `migration-report.json` - Database migration report
- `test_results_endpoints.json` - Endpoint test results
- `test_results_phase3_9.json` - Phase 3-9 test results

### Existing Application Directories
- `/frontend/` - Frontend application code
- `/titanforge_backend/` - Backend application code
- `/data/` - Data storage and fixtures
- `/agent_files_workspace/` - Agent file management
- `/memory/` - Memory storage
- `/swarm/` - Swarm management
- `/node_modules/` - Node.js packages

---

## Import Path Updates

The following test files were updated to reflect the new directory structure:

### Updated Files
1. **tests/endpoints/test_backend.py**
   - Changed sys.path to: `os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend')`

2. **tests/frontend/test_frontend_integration.py**
   - Changed sys.path to: `os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend')`

3. **tests/integration/test_comprehensive_integration.py**
   - Added sys.path initialization pointing to: `os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend')`

### Import Pattern
All moved test files now use:
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'titanforge_backend'))
```

---

## Reorganization Summary

| Category | Files Moved | Subdirectories |
|----------|-------------|-----------------|
| Documentation | 19 | sales, operations, legal, agents |
| Tests | 8 | endpoints, integration, frontend, auth, agents |
| Scripts | 5 | setup, deployment, utilities |
| **Total** | **32** | **12** |

---

## Files Kept in Root (Not Moved)

- **Core configs:** `.env`, `docker-compose.yml`, `package.json`
- **Core documentation:** `README.md`, `PRODUCT_CATALOG.md`, `SECRETS_VAULT.md`
- **System files:** `.gitignore`, `.dockerignore`
- **Test/Migration reports:** JSON and TXT output files

These files remain in the root because they are frequently referenced during development and deployment.

---

## Usage Guidelines

### Finding Documentation
- **Sales/Demo material:** `/docs/sales/`
- **Operational procedures:** `/docs/operations/`
- **Legal compliance:** `/docs/legal/`

### Running Tests
- **API endpoint tests:** `pytest tests/endpoints/`
- **Integration tests:** `pytest tests/integration/`
- **Frontend tests:** `pytest tests/frontend/`

### Running Setup Scripts
- **Setup Stripe:** `python scripts/setup/setup_stripe_products.py`
- **Run implementation:** `python scripts/setup/STEPS_5_TO_10_IMPLEMENTATION.py`

### Running Deployment Scripts
- **Start application:** `.\scripts\deployment\start_titanforge.ps1`
- **Verify production:** `.\scripts\deployment\VERIFY_PRODUCTION_READY.ps1`
- **Launch report:** `.\scripts\deployment\LAUNCH_COMPONENTS_REPORT.ps1`

---

## Future Considerations

The following directories are reserved for future use:
- `/docs/agents/` - Agent-specific documentation
- `/tests/auth/` - Authentication test suite
- `/tests/agents/` - Agent testing
- `/scripts/utilities/` - Utility scripts

---

**Last Updated:** Reorganization Complete  
**Next Review:** After initial demo feedback
