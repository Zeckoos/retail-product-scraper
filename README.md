# Retail Products Scraper

A Python scraper that includes Woolworths product metadata.

Features:
- Product name, brand, price, package size
- Ingredients
- Allergens
- Nutrition (raw JSON)
- Country of Origin
- CoOL PNG/SVG badge URLs
- Ingredient percentage

Architecture:
- `BaseRetailer` abstraction for multi‑retailer support
- Woolworths implementation under `retail_scraper/retailers/woolworths/`
- Browser‑accurate HTTP client using `tls-client`

## Quick start

```bash
uv sync
python main.py
