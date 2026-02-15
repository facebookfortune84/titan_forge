import shopify
from app.core.config import settings


class ShopifyTool:
    def __init__(self):
        self.name = "shopify_manager"
        self.description = (
            "Interacts with a Shopify store. Current action: get_product_list."
        )
        self._setup_session()

    def _setup_session(self):
        if not all(
            [
                settings.SHOPIFY_SHOP_URL,
                settings.SHOPIFY_API_VERSION,
                settings.SHOPIFY_ADMIN_API_TOKEN,
            ]
        ):
            print("WARNING: Shopify settings not fully configured.")
            return

        try:
            api_session = shopify.Session(
                settings.SHOPIFY_SHOP_URL,
                settings.SHOPIFY_API_VERSION,
                settings.SHOPIFY_ADMIN_API_TOKEN,
            )
            shopify.ShopifyResource.activate_session(api_session)
            print("Shopify session activated.")
        except Exception as e:
            print(f"Failed to activate Shopify session: {e}")

    def get_product_list(self) -> str:
        try:
            products = shopify.Product.find()
            product_list = [f"- {p.title} (ID: {p.id})" for p in products]
            return "Product List:\n" + "\n".join(product_list)
        except Exception as e:
            return f"Error fetching Shopify products: {e}"

    def execute(self, action: str) -> str:
        if action == "get_product_list":
            return self.get_product_list()
        else:
            return f"Error: Shopify action '{action}' not supported."
