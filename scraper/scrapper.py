import logging
from typing import List

from core.base_client import BaseClient
from retailers.woolworths.api import WoolworthsAPI
from retailers.woolworths.parser import WoolworthsParser
from models.product import Product

logger = logging.getLogger(__name__)


class WoolworthsScraper:
    """
    High-level scraper that:
    - searches products
    - normalises them
    - optionally enriches with detail
    """

    def __init__(self, location: str = "96064"):
        self.client = BaseClient()
        self.api = WoolworthsAPI(self.client, location=location)
        self.parser = WoolworthsParser()

    def search(self, term: str, with_detail: bool = True) -> List[Product]:
        raw_items = self.api.search_products(term)
        logger.info(f"Found {len(raw_items)} search results for term='{term}'")

        products: List[Product] = []
        for raw in raw_items:
            product = self.parser.from_search_result(raw)

            if with_detail and product.stock_code:
                try:
                    detail_raw = self.api.product_detail(product.stock_code)
                    product = self.parser.enrich_with_detail(product, detail_raw)
                except Exception:
                    logger.warning(
                        f"Failed to fetch detail for stockcode={product.stock_code}",
                        exc_info=True,
                    )

            products.append(product)

        return products