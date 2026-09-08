def extract_barcode(detail):
    """
    Woolworths stores barcodes inconsistently across fields.
    This function normalises all possible locations.
    """
    fields = ["Barcode", "Gtin", "GTIN", "EAN"]

    for f in fields:
        if f in detail and detail[f]:
            return detail[f]

    # Fallback: some products hide barcode in AdditionalAttributes
    attrs = detail.get("AdditionalAttributes", {})
    return attrs.get("Barcode")