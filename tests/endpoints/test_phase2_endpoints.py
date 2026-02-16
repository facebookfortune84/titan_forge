"""Test Phase 2: Verify all key endpoints are working."""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(method, path, data=None, headers=None):
    """Test a single endpoint."""
    url = f"{BASE_URL}{path}"
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            return None
        
        return {
            "path": path,
            "status": response.status_code,
            "success": response.status_code in [200, 201],
            "method": method
        }
    except Exception as e:
        return {"path": path, "status": 0, "success": False, "error": str(e), "method": method}

def main():
    print("=" * 60)
    print("PHASE 2: SYSTEM ENDPOINT VERIFICATION")
    print("=" * 60)
    
    tests = [
        # Health check
        ("GET", "/health"),
        
        # Pricing endpoints (new)
        ("GET", "/api/v1/pricing"),
        ("GET", "/api/v1/pricing/tiers"),
        ("GET", "/api/v1/pricing/basic"),
        ("GET", "/api/v1/pricing/pro"),
        
        # Lead capture endpoints
        ("GET", "/api/v1/leads"),
        
        # Blog endpoints
        ("GET", "/api/v1/blog"),
        
        # Agent endpoints
        ("GET", "/api/v1/agents"),
        ("GET", "/api/v1/agents/graph/nodes"),
        ("GET", "/api/v1/agents/graph/edges"),
        ("GET", "/api/v1/agents/departments"),
        
        # Auth endpoints (will require auth for some)
        ("GET", "/api/v1/auth/me"),  # Should return 401
    ]
    
    passed = 0
    failed = 0
    
    print("\nTesting endpoints:")
    print("-" * 60)
    
    for method, path in tests:
        result = test_endpoint(method, path)
        if result:
            status_str = "✅" if result["success"] else "⚠️ "
            print(f"{status_str} {method:4} {path:35} [{result['status']}]")
            if result["success"]:
                passed += 1
            else:
                failed += 1
    
    print("-" * 60)
    print(f"\nResults: {passed} passed, {failed} failed")
    
    # Test pricing data structure
    print("\n" + "=" * 60)
    print("Pricing Data Verification:")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/api/v1/pricing/basic")
    if response.status_code == 200:
        basic = response.json()
        print(f"✅ Basic Tier: {json.dumps(basic, indent=2)}")
    
    response = requests.get(f"{BASE_URL}/api/v1/pricing/pro")
    if response.status_code == 200:
        pro = response.json()
        print(f"✅ Pro Tier: {json.dumps(pro, indent=2)}")

if __name__ == "__main__":
    main()
