from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Product:
    stock_code: int
    name: str
    display_name: str
    brand: Optional[str]
    package_size: Optional[str]
    price: Optional[float]
    cup_string: Optional[str]

    ingredients: Optional[str]
    country_of_origin: Optional[str]
    origin_png: Optional[str]
    origin_svg: Optional[str]
    origin_percentage: Optional[str]
    origin_country: Optional[str]
    allergen_contains: Optional[str]
    allergen_may_be_present: Optional[str]

    nutritional_raw: Optional[Dict[str, Any]]