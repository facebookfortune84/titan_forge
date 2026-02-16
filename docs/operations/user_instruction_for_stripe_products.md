ACTION PROPOSAL [38.3]: Instruct the user to manually create products and prices in their Stripe Dashboard (test or live) and to then provide the Stripe Product and Price IDs in a structured JSON format.

Rationale: This is a critical, human-dependent step to populate the system's product catalog with Stripe integration details, enabling payment flows. It ensures the user understands their role in setting up the external Stripe configuration.

---

Okay, let's get you set up for live monetization! I'll guide you step-by-step.

### Step 1: Create Your Products in the Stripe Dashboard

This is a **manual step you need to perform in your Stripe account**. Please follow these instructions carefully:

1.  **Go to your Stripe Dashboard:** Open your web browser and go to `https://dashboard.stripe.com/`
    *   **Choose your Mode:** On the left sidebar, toggle between **"Test mode"** and **"Live mode"** based on whether you want to set up test products first or go directly to live. It's highly recommended to do this in **Test mode** first, following the guidance in `STRIPE_SETUP.md`.

2.  **Create Products & Prices:**
    *   In the Stripe Dashboard, navigate to **"Products"** (usually under "Billing" or "Payments").
    *   You need to create products and their associated prices for **ALL** the offerings defined in your `PRODUCT_CATALOG.md`.
    *   **For each product/price combination:**
        *   **For subscriptions (e.g., Starter AIaaS - Monthly):**
            *   Create a "Product" (e.g., "AIaaS Starter").
            *   Add a "Recurring price" to that product (e.g., "$19.00 USD per month").
        *   **For one-time services (e.g., Micro-Feature Development Package):**
            *   Create a "Product" (e.g., "Micro-Feature Development").
            *   Add a "One-time price" to that product (e.g., "$499.00 USD").

    *   **Refer to `PRODUCT_CATALOG.md` for the exact product names, descriptions, and pricing amounts.**
        *   **AIaaS Starter Tier:** $19/month, $199/year
        *   **AIaaS Pro Tier:** $99/month, $999/year
        *   **Micro-Feature Development Package:** $499 (example price)
        *   **Website Audit & Optimization Report:** $299 (example price)
        *   **Automated API Endpoint Creation:** $799 (example price)
        *(Remember, the Enterprise tier for AIaaS is custom pricing and doesn't require a Stripe Price ID for now.)*

3.  **Collect Stripe IDs:**
    *   **As you create each product and price, it's CRITICAL to copy two pieces of information:**
        *   **`Price ID`:** This typically starts with `price_` (e.g., `price_1P3z2g...`).
        *   **`Product ID`:** This typically starts with `prod_` (e.g., `prod_R9Yx0Q...`).
    *   Keep these IDs organized.

### Step 2: Provide the Collected Stripe IDs

Once you have created all the necessary products and prices in your Stripe Dashboard and have collected their respective `Price ID`s and `Product ID`s, please fill them into the template below.

**Copy this entire JSON block, replace all `YOUR_STRIPE_..._ID` placeholders with the actual IDs you collected, and then paste the complete, filled-out JSON back into our chat.**

```json
[
  {
    "name": "Starter AIaaS - Monthly",
    "description": "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month.",
    "type": "subscription",
    "stripe_price_id": "YOUR_STRIPE_STARTER_MONTHLY_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_STARTER_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 1900,
    "interval": "month"
  },
  {
    "name": "Starter AIaaS - Annually",
    "description": "Access to core agent swarm capabilities, 1 concurrent task, 1,000 API requests/month (annual discount).",
    "type": "subscription",
    "stripe_price_id": "YOUR_STRIPE_STARTER_ANNUAL_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_STARTER_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 19900,
    "interval": "year"
  },
  {
    "name": "Pro AIaaS - Monthly",
    "description": "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month.",
    "type": "subscription",
    "stripe_price_id": "YOUR_STRIPE_PRO_MONTHLY_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_PRO_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 9900,
    "interval": "month"
  },
  {
    "name": "Pro AIaaS - Annually",
    "description": "All Starter features + expanded concurrent tasks (5), 10,000 API requests/month (annual discount).",
    "type": "subscription",
    "stripe_price_id": "YOUR_STRIPE_PRO_ANNUAL_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_PRO_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 99900,
    "interval": "year"
  },
  {
    "name": "Micro-Feature Development Package",
    "description": "Delivery of a small, well-defined software feature.",
    "type": "one_time_purchase",
    "stripe_price_id": "YOUR_STRIPE_MICRO_FEATURE_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_MICRO_FEATURE_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 49900
  },
  {
    "name": "Website Audit & Optimization Report",
    "description": "Automated, agent-powered comprehensive audit of a target website.",
    "type": "one_time_purchase",
    "stripe_price_id": "YOUR_STRIPE_WEBSITE_AUDIT_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_WEBSITE_AUDIT_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 29900
  },
  {
    "name": "Automated API Endpoint Creation",
    "description": "Agent-driven development and testing of a single RESTful API endpoint.",
    "type": "one_time_purchase",
    "stripe_price_id": "YOUR_STRIPE_API_ENDPOINT_PRICE_ID",
    "stripe_product_id": "YOUR_STRIPE_API_ENDPOINT_PRODUCT_ID",
    "currency": "USD",
    "unit_amount": 79900
  }
]
```