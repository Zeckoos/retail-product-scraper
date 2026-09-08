import logging
from scraper_factory import ScraperFactory

logging.basicConfig(level=logging.INFO)

def print_product(p):
    print(f"{p.display_name} | (Stockcode: {p.stock_code})")
    print(f"Brand: {p.brand}")
    print(f"Price: ${p.price} | {p.cup_string}")
    print(f"Ingredients: {p.ingredients}")
    print(f"Country of origin: {p.origin_country}")
    print(f"Origin country: {p.origin_country}")
    print(f"Origin percentage: {p.origin_percentage}")
    print(f"Origin PNG: {p.origin_png}")
    print(f"Origin SVG: {p.origin_svg}")
    print(f"Allergen contains: {p.allergen_contains}")
    print(f"Allergen may be present: {p.allergen_may_be_present}")
    print(f"Has nutritional info: {p.nutritional_raw is not None}")
    print("-----")

def main():
    scraper = ScraperFactory.woolworths()
    products = scraper.search("La gina extra virgin", with_detail=True)

    for p in products:
        print_product(p)

if __name__ == "__main__":
    main()