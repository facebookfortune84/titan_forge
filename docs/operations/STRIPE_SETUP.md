ACTION PROPOSAL [21]: Create STRIPE_SETUP.md documentation.

Rationale: This document is crucial for guiding the human operator on setting up and managing Stripe integration, including environment variables, testing procedures, and deployment to live mode.

---
# Stripe Setup and Management

This document provides instructions for configuring and managing Stripe integration within the TitanForge project.

## 1. Required Environment Variables

Ensure the following environment variables are set in your `.env` file for the backend application.
**Do NOT commit actual secret keys to your repository.**

*   `STRIPE_API_KEY`: Your Stripe Secret Key. This typically starts with `sk_test_` for test mode or `sk_live_` for live mode.
*   `STRIPE_WEBHOOK_SECRET`: The secret key for signing webhooks, obtained from your Stripe Dashboard webhook settings.

**Example `.env` entries:**
```
STRIPE_API_KEY=sk_test_********************************
STRIPE_WEBHOOK_SECRET=whsec_***************************
```

## 2. Running in Test Mode (Recommended for Development)

For all development and initial testing, it is highly recommended to use Stripe's test mode. This allows you to simulate transactions without affecting real money.

### 2.1. Configure Test API Key
Set your `STRIPE_API_KEY` in the `.env` file to a **test secret key** (starts with `sk_test_`).

### 2.2. Configure Test Webhook Secret
Obtain a test webhook secret from your Stripe Dashboard:
1.  Go to the Stripe Dashboard: `https://dashboard.stripe.com/test/webhooks`
2.  Click "Add endpoint" or select an existing endpoint.
3.  Configure the URL to point to your development server's webhook endpoint (e.g., `http://localhost:8000/api/v1/stripe-webhook`).
4.  Select the events you want to receive (at a minimum: `checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_succeeded`, `invoice.payment_failed`).
5.  After creation, retrieve the signing secret (starts with `whsec_test_`) and set it as `STRIPE_WEBHOOK_SECRET` in your `.env` file.

### 2.3. Test Procedures

You can test the Stripe integration using the following steps (assuming your backend is running):

#### A. Initial Product Setup (Manual via Stripe Dashboard or API)
Before creating checkout sessions, you need to have Products and Prices defined in your Stripe account.
1.  Go to the Stripe Dashboard (Test Mode): `https://dashboard.stripe.com/test/products`
2.  Create the following products and associated recurring prices (for subscriptions) or one-time prices (for productized services) that match the `PRODUCT_CATALOG.md`:
    *   **AIaaS Starter Tier:**
        *   Product: `AIaaS Starter`
        *   Price: `$19.00 / month` (or `$199.00 / year`)
    *   **AIaaS Pro Tier:**
        *   Product: `AIaaS Pro`
        *   Price: `$99.00 / month` (or `$999.00 / year`)
    *   **Micro-Feature Development Package:**
        *   Product: `Micro-Feature Development`
        *   Price: `$499.00 / one-time` (or appropriate range)
3.  **Crucially:** Note down the `Price ID` for each product. You will use these Price IDs to seed your `db_models.Product` entries (via a script or API call).

#### B. Populate Internal Products in Database
You will need to manually (or via an admin endpoint you create) add entries to your `db_models.Product` table in your PostgreSQL database, mirroring the Stripe Products and Prices you created. Ensure you save the corresponding `stripe_price_id` and `stripe_product_id` from Stripe into your database records.

#### C. Simulate Checkout Flow (Frontend Interaction)
1.  **Register a User:** Use your frontend's registration page (`/register`) to create a new user.
2.  **Browse Products:** Access your frontend's pricing page (to be implemented, e.g., `/pricing`) which lists the products you seeded from your database.
3.  **Initiate Checkout:** When a user clicks "Subscribe" or "Buy," the frontend should call your backend's `/api/v1/create-checkout-session` endpoint with the `product_id` (your internal UUID), `success_url`, and `cancel_url`.
    *   **Example `curl` for testing `create-checkout-session` (replace with actual values):**
        ```bash
        curl -X POST "http://localhost:8000/api/v1/create-checkout-session" 
             -H "Authorization: Bearer YOUR_ACCESS_TOKEN" 
             -H "Content-Type: application/json" 
             -d '{
                   "product_id": "YOUR_INTERNAL_PRODUCT_UUID",
                   "success_url": "http://localhost:3000/success",
                   "cancel_url": "http://localhost:3000/cancel"
                 }'
        ```
4.  **Complete Payment (Stripe Test Cards):** The backend will return a `checkout_session.url`. Redirect your browser to this URL. On the Stripe Checkout page, use Stripe's test credit card numbers (e.g., `4242...4242` for Visa, any future expiry date, any CVC) to complete the payment.
5.  **Verify Webhook Processing:** After successful payment, Stripe will send a webhook event to your `/api/v1/stripe-webhook` endpoint. Verify in your backend logs that the `BillingAgent` receives and processes this event, updating your `users`, `subscriptions`, and `stripe_transactions` tables accordingly.
    *   Check your `users` table for `stripe_customer_id` and `current_subscription_id`.
    *   Check your `subscriptions` table for new active entries.
    *   Check your `stripe_transactions` table for `checkout.session.completed` and `invoice.payment_succeeded` events.

## 3. Switching to Live Mode

Once thoroughly tested in test mode, you can switch to live mode by:

1.  **Update API Key:** Change `STRIPE_API_KEY` in your `.env` file to your **live secret key** (starts with `sk_live_`).
2.  **Update Webhook Secret:** Obtain a live webhook secret from your Stripe Dashboard: `https://dashboard.stripe.com/webhooks`. Configure a live endpoint (e.g., `https://your-production-domain.com/api/v1/stripe-webhook`) and set the live `whsec_live_` secret as `STRIPE_WEBHOOK_SECRET` in your `.env` file.
3.  **Create Live Products/Prices:** Recreate your products and prices in the Stripe Dashboard's **live mode**, noting their live `Price ID`s.
4.  **Update Internal Products:** Update your `db_models.Product` entries in your production database with the live `stripe_price_id`s and `stripe_product_id`s.
5.  **Deploy:** Deploy your updated application with the live environment variables.

**Remember: Always test thoroughly in test mode before deploying to live. Any actions in live mode involve real money.**
