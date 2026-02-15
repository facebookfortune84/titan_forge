ACTION PROPOSAL [36]: Generate the "Go Live Checklist" for activating monetization.

Rationale: This checklist provides a clear, actionable guide for the human operator to transition the TitanForge AI platform from development to a fully operational, revenue-generating system, ensuring all critical steps are covered.

---
# TitanForge AI - Go Live Checklist

This checklist outlines the essential steps required to fully activate monetization and make the TitanForge AI platform live. Please perform these actions carefully.

## REQUIRED BEFORE LIVE

*   **1. Stripe Account Setup:**
    *   Ensure your Stripe account is fully set up, verified, and ready to accept live payments.
*   **2. Live Stripe API Keys:**
    *   Update your `.env` file with your **live Stripe Secret Key** (`STRIPE_API_KEY` starting with `sk_live_`) and your **live Stripe Publishable Key** (to be used by the frontend, ensure this is securely handled and passed to the frontend).
*   **3. Live Webhook Secret:**
    *   Create a **live webhook endpoint** in your Stripe Dashboard (`https://dashboard.stripe.com/webhooks`) pointing to your production backend URL (e.g., `https://your-production-domain.com/api/v1/stripe-webhook`).
    *   Configure it to listen for all necessary events (`checkout.session.completed`, `customer.subscription.created`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_succeeded`, `invoice.payment_failed`).
    *   Copy the **live signing secret** (starts with `whsec_live_`) and set it as `STRIPE_WEBHOOK_SECRET` in your `.env` file.
*   **4. Create Live Stripe Products & Prices:**
    *   Manually create all the products and prices defined in your `PRODUCT_CATALOG.md` within your **live Stripe Dashboard**.
    *   Ensure the `Price ID`s match the expected billing intervals (monthly/yearly) and amounts.
*   **5. Seed Production Database with Live Product IDs:**
    *   Run a script or use an administrative tool to populate your **production database's `products` table** with entries corresponding to your live Stripe Products.
    *   Crucially, map the `stripe_price_id` and `stripe_product_id` from your live Stripe account to your internal `db_models.Product` entries.
*   **6. Configure Live Email (SMTP):**
    *   Ensure your `SMTP_USER`, `SMTP_PASS`, `SMTP_SERVER`, `SMTP_PORT` in `.env` are configured for a live, reliable email sending service (e.g., SendGrid, Mailgun, or a dedicated Gmail business account with an app password) to ensure transactional emails (welcome, payment confirmations) are delivered.
*   **7. Deploy Backend & Frontend to Production:**
    *   Deploy your backend application (FastAPI) and frontend application (React) to your chosen production hosting environment (e.g., Render, Vercel, AWS, GCP).
    *   Ensure all `.env` variables are correctly configured in the production environment.
*   **8. Create Superuser Account:**
    *   Ensure at least one user account has `is_superuser=True` in the database to access the `AnalyticsDashboard`. This might require direct database modification or a special admin registration route (if implemented).
*   **9. Test Live Checkout Flow:**
    *   Perform a small, legitimate purchase (e.g., a Starter plan) using real payment details in the live environment.
    *   Verify that:
        *   The checkout process completes successfully.
        *   Your Stripe Dashboard shows the new customer and subscription.
        *   The `BillingAgent` processes the webhooks (check backend logs).
        *   Your internal database (`users`, `subscriptions`, `stripe_transactions`) is correctly updated.
        *   You receive the welcome and payment confirmation emails.
        *   Your access to features is correctly provisioned.
*   **10. Test Analytics Reporting:**
    *   Verify that the `AnalyticsDashboard` (accessible by a superuser) correctly displays updated metrics after live user activity.

## RECOMMENDED OPTIMIZATION

*   **11. Detailed `PricingPage.tsx` Content:**
    *   Add compelling copy, feature comparisons, and clear call-to-actions to the pricing page.
*   **12. Compelling `AgentLandingPage.tsx` Content:**
    *   Develop high-quality marketing copy, visuals, and testimonials for the main landing page to attract and convert visitors.
*   **13. Implement Google Analytics / SEO Tools:**
    *   Integrate Google Analytics or other preferred SEO/traffic tracking tools into the frontend for more comprehensive visitor insights.
*   **14. Setup Monitoring & Alerts:**
    *   Configure monitoring for backend services, database health, Redis, and agent queues to proactively detect and resolve issues.
    *   Set up alerts for critical system failures or payment processing errors.
*   **15. Automated Product Seeding:**
    *   Develop an internal admin endpoint or script to automate the synchronization of products between your internal database and Stripe.
*   **16. Enhance Customer Support:**
    *   Integrate the `Notification Agent` with a dedicated customer support platform or build out a basic support ticketing system.
*   **17. Basic Marketing Automation:**
    *   Configure the `Notification Agent` to send welcome, nurture, and upgrade email sequences.

## FINAL STATUS: Ready for Deployment & Activation

All necessary architectural changes, core monetization logic, and foundational UI components are in place. The system is designed for automated operation with human oversight. This checklist enables a confident transition to a revenue-generating platform.
