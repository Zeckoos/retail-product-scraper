import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class WoolworthsAPI:
    """
    Wrapper around Woolworths' internal JSON endpoints.
    Keeps retailer logic separate from the shared BaseClient.
    """

    def __init__(self, client, location="96064"):
        self.client = client
        self.location = location  # Store ID for location-specific pricing

    def search_products(self, term: str, page=1, page_size=36) -> List[Dict[str, Any]]:
        """
        Search by keyword.
        Returns raw JSON from /apis/ui/Search/products.
        """
        payload = {
            "SearchTerm": term,
            "PageNumber": page,
            "PageSize": page_size,
            "Location": self.location,
        }
        data = self.client.post("/apis/ui/Search/products", json=payload)

        if not isinstance(data, dict):
            logger.warning("Search returned non-JSON")
            return []

        blocks = data.get("Products", [])
        if not blocks:
            return []

        return blocks[0].get("Products", []) or []

    def product_detail(self, stock_code: int):
        """GET detail endpoint — same as browser."""
        path = f"/apis/ui/product/detail/{stock_code}"
        data = self.client.get(path)

        if not isinstance(data, dict):
            logger.warning(f"Detail unavailable for stockcode={stock_code}")
            return None

        # Normalise shape
        # if "Product" in data:
        #     return data["Product"]
        #
        # if "Products" in data and isinstance(data["Products"], list):
        #     return data["Products"][0]

        return data