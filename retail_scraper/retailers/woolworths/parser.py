import json
from typing import Dict, Any, Optional

from models.product import Product


class WoolworthsParser:
    """
    Transforms Woolworths JSON into our internal Product model.
    """

    @staticmethod
    def _get_additional_attr(raw: Dict[str, Any], key: str) -> Optional[str]:
        return (raw.get("AdditionalAttributes") or {}).get(key)

    @staticmethod
    def _parse_nutritional(raw: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        nutri = (raw.get("AdditionalAttributes") or {}).get("nutritionalinformation")
        if not nutri:
            return None
        try:
            return json.loads(nutri)
        except Exception:
            return None

    @staticmethod
    def _parse_country_of_origin(raw: Dict[str, Any]) -> Dict[str, Optional[str]]:
        """
            Parse CountryOfOriginLabel from top-level detail JSON.

            Fallback rules:
            - Prefer AltText (full human-readable label)
            - If CountryOfOrigin is empty, still return AltText
            - If both are empty, return None for all fields
            """
        label = raw.get("CountryOfOriginLabel")
        if not isinstance(label, dict):
            return {
                "text": None,
                "country": None,
                "percentage": None,
                "png": None,
                "svg": None,
            }

        alt = label.get("AltText")
        country = label.get("CountryOfOrigin")

        # Fallback: if country is empty but AltText exists, use AltText
        if not country and alt:
            country = alt

        return {
            "text": alt,
            "country": country,
            "percentage": label.get("IngredientPercentage"),
            "png": label.get("PngImageFile"),
            "svg": label.get("SvgImageFile"),
        }

    @classmethod
    def from_search_result(cls, raw: Dict[str, Any]) -> Product:
        """
        Build a Product from a search result item.
        Search already includes a lot of metadata.
        """
        return Product(
            stock_code=raw.get("Stockcode"),
            name=raw.get("Name"),
            display_name=raw.get("DisplayName"),
            brand=raw.get("Brand") or cls._get_additional_attr(raw, "brand"),
            package_size=raw.get("PackageSize"),
            price=raw.get("Price"),
            cup_string=raw.get("CupString"),

            ingredients=cls._get_additional_attr(raw, "ingredients"),
            country_of_origin=None,
            origin_png=None,
            origin_svg=None,
            origin_percentage=None,
            origin_country=None,
            allergen_contains=cls._get_additional_attr(raw, "allergencontains"),
            allergen_may_be_present=cls._get_additional_attr(raw, "allergenmaybepresent"),

            nutritional_raw=cls._parse_nutritional(raw),
        )

    @classmethod
    def enrich_with_detail(cls, product: Product, detail_raw: Dict[str, Any]) -> Product:
        """
        Merge detail response into an existing Product.
        """
        if not isinstance(detail_raw, dict):
            return product

        product.ingredients = (
                cls._get_additional_attr(detail_raw, "ingredients")
                or product.ingredients)

        origin = cls._parse_country_of_origin(detail_raw)
        product.country_of_origin = origin["text"]
        product.origin_country = origin["country"]
        product.origin_percentage = origin["percentage"]
        product.origin_png = origin["png"]
        product.origin_svg = origin["svg"]

        product.allergen_contains = (
                cls._get_additional_attr(detail_raw, "allergencontains")
                or product.allergen_contains
        )

        product.allergen_may_be_present = (
                cls._get_additional_attr(detail_raw, "allergenmaybepresent")
                or product.allergen_may_be_present
        )

        product.nutritional_raw = (
                cls._parse_nutritional(detail_raw)
                or product.nutritional_raw
        )

        return product