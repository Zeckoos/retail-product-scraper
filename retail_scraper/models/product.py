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

    # Country of Origin (CoOL)
    country_of_origin: Optional[str]  # Human-readable label (AltText)
    origin_country: Optional[str]  # Country name
    origin_percentage: Optional[str]  # Ingredient percentage
    origin_png: Optional[str]  # PNG badge URL
    origin_svg: Optional[str]  # SVG badge URL

    allergen_contains: Optional[str]
    allergen_may_be_present: Optional[str]

    nutritional_raw: Optional[Dict[str, Any]]