import logging
from scrapper import WoolworthsScraper

logging.basicConfig(level=logging.INFO)

def print_product(p):
    print(f"{p.display_name} (Stockcode: {p.stock_code})")
    print(f"Brand: {p.brand}")
    print(f"Price: {p.price} | {p.cup_string}")
    print(f"Ingredients: {p.ingredients}")
    print(f"Country of origin: {p.origin_country}")
    print(f"Allergen contains: {p.allergen_contains}")
    print(f"Allergen may be present: {p.allergen_may_be_present}")
    print(f"Has nutritional info: {p.nutritional_raw is not None}")
    print("-----")

def main():
    scraper = WoolworthsScraper(location="96064")
    term = "san remo spaghetti"

    products = scraper.search(term, with_detail=True)

    for p in products:
        print_product(p)
        if p.nutritional_raw:
            print("Has nutritional info")

if __name__ == "__main__":
    main()