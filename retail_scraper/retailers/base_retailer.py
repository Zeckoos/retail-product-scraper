from abc import ABC, abstractmethod
from typing import List
from models.product import Product

class BaseRetailer(ABC):
    """
    Abstract base class for all retailer scrapers.

    Implement this interface for new retailers (Coles, Aldi, etc.).
    """

    @abstractmethod
    def search(self, term: str, with_detail: bool = True) -> List[Product]:
        """
        Search for products by term.

        :param term: Search query string.
        :param with_detail: If True, fetch detail for each product.
        """
        pass