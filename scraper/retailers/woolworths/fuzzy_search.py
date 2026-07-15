from rapidfuzz import fuzz

def score_product(product, query):
    """
    Weighted fuzzy scoring:
    - name is most important
    - brand helps disambiguate
    - size helps differentiate variants
    """
    name = product.get("Name", "")
    brand = product.get("Brand", "")
    size = product.get("PackageSize", "") or product.get("Size", "")

    name_score = fuzz.token_set_ratio(query, name)
    brand_score = fuzz.partial_ratio(query, brand)
    size_score = fuzz.partial_ratio(query, size)

    return name_score * 0.65 + brand_score * 0.25 + size_score * 0.10


def fuzzy_best_match(products, query):
    """Return the single best fuzzy match from a product list."""
    scored = [(score_product(p, query), p) for p in products]
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1]