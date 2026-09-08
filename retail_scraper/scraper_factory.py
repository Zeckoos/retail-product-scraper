from retailers.woolworths.ww_scraper import WoolworthsScraper
from retailers.base_retailer import BaseRetailer


class ScraperFactory:
    """
    Factory for creating retailer scrapers.

    Forkers:
    - Register new retailers here (Coles, Aldi, etc.).
    """

    @staticmethod
    def woolworths(location: str = "96064") -> BaseRetailer:
        return WoolworthsScraper(location)