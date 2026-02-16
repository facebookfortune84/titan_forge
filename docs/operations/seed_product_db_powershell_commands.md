ACTION PROPOSAL [40]: Generate PowerShell equivalent commands for seeding the internal product database.

Rationale: Providing commands compatible with the user's environment is crucial for them to successfully complete the product seeding step, which is a prerequisite for live monetization.

---

My apologies for providing `curl` commands when you are using PowerShell. Here are the equivalent commands using `Invoke-RestMethod` for PowerShell.

**Before you execute these commands:**

*   **Ensure your backend is running.**
*   **Obtain a valid JWT `access_token` for your superuser account.** (You can get this by logging in via the frontend and inspecting local storage, or using the `/token` endpoint as described in previous instructions).
*   **Replace `YOUR_SUPERUSER_JWT_TOKEN`** in each command with your actual token.

```powershell
# Store your superuser JWT token in a variable
$jwtToken = "YOUR_SUPERUSER_JWT_TOKEN"

# Common headers for all requests
$headers = @{
    "Authorization" = "Bearer $($jwtToken)"
    "Content-Type"  = "application/json"
}

# Command 1: Starter AIaaS - Monthly
$body1 = @{
    name = "Starter AIaaS - Monthly"
    description = "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month."
    type = "subscription"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2M"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2M"
    currency = "USD"
    unit_amount = 1900
    interval = "month"
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body1

# Command 2: Starter AIaaS - Annually
$body2 = @{
    name = "Starter AIaaS - Annually"
    description = "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month (annual discount)."
    type = "subscription"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2N"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2M"
    currency = "USD"
    unit_amount = 19900
    interval = "year"
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body2

# Command 3: Pro AIaaS - Monthly
$body3 = @{
    name = "Pro AIaaS - Monthly"
    description = "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month."
    type = "subscription"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2O"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2P"
    currency = "USD"
    unit_amount = 9900
    interval = "month"
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body3

# Command 4: Pro AIaaS - Annually
$body4 = @{
    name = "Pro AIaaS - Annually"
    description = "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month (annual discount)."
    type = "subscription"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2Q"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2P"
    currency = "USD"
    unit_amount = 99900
    interval = "year"
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body4

# Command 5: Micro-Feature Development Package
$body5 = @{
    name = "Micro-Feature Development Package"
    description = "Delivery of a small, well-defined software feature."
    type = "one_time_purchase"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2R"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2S"
    currency = "USD"
    unit_amount = 49900
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body5

# Command 6: Website Audit & Optimization Report
$body6 = @{
    name = "Website Audit & Optimization Report"
    description = "Automated, agent-powered comprehensive audit of a target website."
    type = "one_time_purchase"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2T"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2U"
    currency = "USD"
    unit_amount = 29900
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body6

# Command 7: Automated API Endpoint Creation
$body7 = @{
    name = "Automated API Endpoint Creation"
    description = "Agent-driven development and testing of a single RESTful API endpoint."
    type = "one_time_purchase"
    stripe_price_id = "price_1P9c4lR512b2aB4LqA2G2T2V"
    stripe_product_id = "prod_P9c4lR512b2aB4LqA2G2T2W"
    currency = "USD"
    unit_amount = 79900
    is_active = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/admin/products" `
    -Method Post `
    -Headers $headers `
    -Body $body7

```
**Please execute these commands in your PowerShell terminal after replacing `YOUR_SUPERUSER_JWT_TOKEN` with your actual token.**

Once executed, you can verify that the products have been added by visiting `http://localhost:8000/docs` and using the `/api/v1/products` endpoint (after logging in with any user account).

Let me know when you have successfully seeded the products.
