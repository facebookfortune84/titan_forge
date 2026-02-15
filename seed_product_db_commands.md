ACTION PROPOSAL [39]: Generate curl commands to seed the internal product database using the provided Stripe Product and Price IDs.

Rationale: This action will populate the db_models.Product table in the internal database with the actual Stripe product configurations, which is a critical step to enable payment processing and display product offerings on the frontend. This brings the system closer to live monetization.

---

Here are the `curl` commands to seed your internal product database with the Stripe Product and Price IDs you provided.

**Before you execute these commands:**

*   **Ensure your backend is running.**
*   **Obtain a valid JWT `access_token` for your superuser account.** (You can get this by logging in via the frontend and inspecting local storage, or using the `/token` endpoint as described in previous instructions).
*   **Replace `YOUR_SUPERUSER_JWT_TOKEN`** in each `curl` command with your actual token.

```bash
# Command 1: Starter AIaaS - Monthly
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Starter AIaaS - Monthly",
           "description": "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month.",
           "type": "subscription",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2M",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2M",
           "currency": "USD",
           "unit_amount": 1900,
           "interval": "month",
           "is_active": true
         }'

# Command 2: Starter AIaaS - Annually
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Starter AIaaS - Annually",
           "description": "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month (annual discount).",
           "type": "subscription",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2N",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2M",
           "currency": "USD",
           "unit_amount": 19900,
           "interval": "year",
           "is_active": true
         }'

# Command 3: Pro AIaaS - Monthly
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Pro AIaaS - Monthly",
           "description": "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month.",
           "type": "subscription",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2O",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2P",
           "currency": "USD",
           "unit_amount": 9900,
           "interval": "month",
           "is_active": true
         }'

# Command 4: Pro AIaaS - Annually
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Pro AIaaS - Annually",
           "description": "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month (annual discount).",
           "type": "subscription",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2Q",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2P",
           "currency": "USD",
           "unit_amount": 99900,
           "interval": "year",
           "is_active": true
         }'

# Command 5: Micro-Feature Development Package
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Micro-Feature Development Package",
           "description": "Delivery of a small, well-defined software feature.",
           "type": "one_time_purchase",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2R",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2S",
           "currency": "USD",
           "unit_amount": 49900,
           "is_active": true
         }'

# Command 6: Website Audit & Optimization Report
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Website Audit & Optimization Report",
           "description": "Automated, agent-powered comprehensive audit of a target website.",
           "type": "one_time_purchase",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2T",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2U",
           "currency": "USD",
           "unit_amount": 29900,
           "is_active": true
         }'

# Command 7: Automated API Endpoint Creation
curl -X POST "http://localhost:8000/api/v1/admin/products" 
     -H "Authorization: Bearer YOUR_SUPERUSER_JWT_TOKEN" 
     -H "Content-Type: application/json" 
     -d '{
           "name": "Automated API Endpoint Creation",
           "description": "Agent-driven development and testing of a single RESTful API endpoint.",
           "type": "one_time_purchase",
           "stripe_price_id": "price_1P9c4lR512b2aB4LqA2G2T2V",
           "stripe_product_id": "prod_P9c4lR512b2aB4LqA2G2T2W",
           "currency": "USD",
           "unit_amount": 79900,
           "is_active": true
         }'

```
**Please execute these commands in your terminal after replacing `YOUR_SUPERUSER_JWT_TOKEN` with your actual token.**

Once executed, you can verify that the products have been added by visiting `http://localhost:8000/docs` and using the `/api/v1/products` endpoint (after logging in with any user account).

Let me know when you have successfully seeded the products.
