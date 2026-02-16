# 🔧 CRITICAL ACTION PLAN - TitanForge Emergency Fixes

**Generated:** February 16, 2026  
**Deadline:** 2.5 Hours  
**Priority:** CRITICAL

---

## PHASE 1: CRITICAL FIXES (45 Minutes)

### ✅ FIX #1: Test Payload Format Mismatch
**Problem:** Tests using `json=` for OAuth2PasswordRequestForm (expects form-encoded data)  
**File:** `titanforge_backend/tests/test_new_endpoints.py` (line 195-200)  
**Root Cause:** Login endpoint uses `OAuth2PasswordRequestForm` which expects form data, not JSON

```python
# WRONG - Current test (line 195)
response = client.post(
    "/api/v1/auth/login",
    json={                          # ❌ WRONG FORMAT
        "username": email,
        "password": password
    }
)

# CORRECT - Should be:
response = client.post(
    "/api/v1/auth/login",
    data={                          # ✓ CORRECT FORMAT (form-encoded)
        "username": email,
        "password": password
    }
)
```

**Files to Fix:**
- test_new_endpoints.py:195-199 (test_login_success)
- test_new_endpoints.py:220-225 (test_refresh_token prerequisites)
- test_new_endpoints.py:247-252 (test_logout prerequisites)

---

### ✅ FIX #2: Database State Between Tests
**Problem:** Tests failing due to database state pollution (duplicate emails persist)  
**Solution:** Implement pytest fixtures with database cleanup

**Code to Add at top of test_new_endpoints.py:**

```python
import tempfile
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(autouse=True)
def setup_test_db():
    """Setup test database before each test"""
    # Clear database before test
    yield
    # Cleanup after test (optional - can delete test.db)
```

**Files to Update:**
- test_new_endpoints.py (add fixtures and conftest.py)

---

### ✅ FIX #3: Lead Endpoint Routing Issue
**Problem:** Tests fail when accessing leads - routing might not be properly registered  
**Current Status:** GET endpoints already exist in leads.py (lines 99-124) ✓

**Verification Needed:**
- Check if router is properly included in main.py
- Verify prefix is correct: `app.include_router(leads_router, prefix="/api/v1")`

**Current Status in main.py (line 92):**
```python
app.include_router(leads_router, prefix="/api/v1")  # ✓ Correct
```

**Action:** Tests should work once database fixtures are fixed

---

### ✅ FIX #4: Test Execution Order
**Problem:** Tests depend on specific execution order (create before read)  
**Solution:** Add test isolation and use fixtures

**Changes:**
- Each test should be independent
- Use unique email addresses (add UUID to email)
- Clear database state before each test

---

## PHASE 2: COMPONENT CREATION (25 Minutes)

### Component #1: CookieBanner.tsx
**Location:** `frontend/src/components/CookieBanner.tsx`  
**Purpose:** Cookie consent banner (GDPR compliant)  
**Estimated Time:** 5 minutes

```typescript
import React, { useState, useEffect } from 'react';

interface CookieBannerProps {
  onAccept?: () => void;
  onDecline?: () => void;
}

const CookieBanner: React.FC<CookieBannerProps> = ({ onAccept, onDecline }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const cookieAccepted = localStorage.getItem('cookies_accepted');
    if (!cookieAccepted) {
      setIsVisible(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('cookies_accepted', 'true');
    setIsVisible(false);
    onAccept?.();
  };

  const handleDecline = () => {
    localStorage.setItem('cookies_accepted', 'false');
    setIsVisible(false);
    onDecline?.();
  };

  if (!isVisible) return null;

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      backgroundColor: '#1a1a1a',
      color: 'white',
      padding: '20px',
      zIndex: 1000,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center'
    }}>
      <p>We use cookies to improve your experience.</p>
      <div style={{ display: 'flex', gap: '10px' }}>
        <button onClick={handleDecline} style={{
          padding: '10px 20px',
          backgroundColor: 'transparent',
          border: '1px solid white',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px'
        }}>
          Decline
        </button>
        <button onClick={handleAccept} style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          border: 'none',
          color: 'white',
          cursor: 'pointer',
          borderRadius: '4px'
        }}>
          Accept
        </button>
      </div>
    </div>
  );
};

export default CookieBanner;
```

### Component #2: ROICalculatorComponent.tsx
**Location:** `frontend/src/components/ROICalculatorComponent.tsx`  
**Purpose:** Display ROI calculations visually  
**Estimated Time:** 10 minutes

---

### Component #3: LiveDemo.tsx
**Location:** `frontend/src/LiveDemo.tsx`  
**Purpose:** Interactive demo showcase page  
**Estimated Time:** 10 minutes

---

## PHASE 3: TEST FIXES (20 Minutes)

### Test Fix #1: Fix test_main.py
**Problem:** Root endpoint test expects specific JSON response  
**File:** `titanforge_backend/tests/test_main.py:9`

**Current Error:**
```
json.decoder.JSONDecodeError: Expecting value: line 1 column 1
```

**Action:** Check what root endpoint actually returns

---

### Test Fix #2: Add conftest.py
**Location:** `titanforge_backend/tests/conftest.py` (NEW FILE)

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Use in-memory SQLite for tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

---

### Test Fix #3: Update test_new_endpoints.py
**Changes Required:**

1. **Lines 195-199:** Change from `json=` to `data=` for login
2. **Lines 25-35:** Add unique email generation for test_create_lead_success
3. **Lines 59-66:** Add unique email generation
4. **Lines 88-95:** Add unique email generation
5. **Lines 111-119:** Add unique email generation

**Pattern to use:**
```python
import uuid
email = f"test_{uuid.uuid4().hex[:8]}@example.com"
```

---

## PHASE 4: VERIFICATION (30 Minutes)

### Verification Checklist

#### ✅ Database & Routing
- [ ] Root endpoint returns valid JSON
- [ ] Leads router properly registered
- [ ] Auth router properly registered
- [ ] All database tables created

#### ✅ Auth Flow
- [ ] Register endpoint accepts valid payload (201)
- [ ] Register rejects weak passwords (400)
- [ ] Register rejects duplicate emails (400)
- [ ] Register rejects invalid emails (422)
- [ ] Login endpoint accepts form data (200 with token)
- [ ] Login endpoint rejects invalid credentials (401)
- [ ] Get current user requires auth (401 without token)
- [ ] Token refresh works (200)
- [ ] Logout works (200)

#### ✅ Lead Flow
- [ ] Create lead with valid data (201)
- [ ] Create lead rejects invalid email (400/422)
- [ ] Create lead rejects duplicate email (409)
- [ ] List leads returns array (200)
- [ ] Get single lead returns lead (200)
- [ ] Get nonexistent lead returns 404

#### ✅ Test Suite
```bash
cd F:\TitanForge
pytest titanforge_backend/tests/ -v

# Expected: 19/19 tests PASSED or close to 100%
```

---

## IMPLEMENTATION ORDER

### Step 1: Fix Tests (20 minutes)
1. Create `conftest.py` with database fixtures
2. Update test payloads (json → data for login)
3. Add unique email generation
4. Run pytest and verify 15+ tests pass

### Step 2: Fix Root Endpoint (5 minutes)
1. Check main.py root endpoint
2. Fix response format if needed
3. Verify test passes

### Step 3: Create Components (20 minutes)
1. Create CookieBanner.tsx
2. Create ROICalculatorComponent.tsx
3. Create LiveDemo.tsx (optional if time permits)

### Step 4: Final Testing (10 minutes)
1. Run all tests
2. Build frontend
3. Smoke test endpoints
4. Verify routes work

---

## SUCCESS METRICS

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Test Pass Rate | 21% (4/19) | 90%+ (17/19) | ❌ WORKING |
| Auth Tests | 1/9 | 9/9 | ❌ CRITICAL |
| Lead Tests | 1/7 | 7/7 | ❌ CRITICAL |
| Component Tests | 0/3 | 3/3 | ⏳ PENDING |
| Route Availability | 11/11 | 11/11 | ✓ OK |

---

## RISKS & MITIGATION

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Database state pollution | HIGH | CRITICAL | ✓ Using conftest fixtures |
| Test payload format | HIGH | CRITICAL | ✓ Will fix in step 1 |
| Missing components | MEDIUM | HIGH | ✓ Quick to create |
| Time constraint | MEDIUM | HIGH | ✓ Parallel work possible |

---

## TIME ALLOCATION

```
Phase 1 - Critical Fixes:        45 min ████████████████
Phase 2 - Components:            25 min ██████████
Phase 3 - Verification:          30 min ███████████
Phase 4 - Buffer/Contingency:    10 min ████
────────────────────────────────────────
Total:                          110 min (30 min buffer available)
```

---

## NEXT IMMEDIATE ACTIONS

1. ⏱️ **RIGHT NOW (5 min):** Create conftest.py in tests/
2. ⏱️ **NEXT (10 min):** Update test_new_endpoints.py with fixes
3. ⏱️ **THEN (5 min):** Run pytest to verify 15+ tests pass
4. ⏱️ **AFTER (20 min):** Create missing components
5. ⏱️ **FINAL (10 min):** Full suite verification

**Estimated Total Time to 90% Ready:** 60 minutes  
**Estimated Total Time to 100% Ready:** 110 minutes

---

**Document Version:** 1.0  
**Last Updated:** February 16, 2026, 11:40 UTC  
**Status:** Ready to implement
