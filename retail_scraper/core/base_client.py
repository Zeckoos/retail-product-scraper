import time
import random
import logging
import tls_client

logger = logging.getLogger(__name__)

class BaseClient:
    """
    Browser‑accurate HTTP client using TLS fingerprinting.

    This client is reusable across retailers. Retailer modules
    should not hard‑code headers; instead, they can override or
    extend these defaults if needed.
    """

    BASE_URL = "https://www.woolworths.com.au" # Replace with retailer site

    def __init__(self, min_delay=0.7, max_delay=1.4):
        self.min_delay = min_delay
        self.max_delay = max_delay

        # Chrome 124 TLS fingerprint (real browser handshake)
        self.session = tls_client.Session(
            client_identifier="chrome_120",
            random_tls_extension_order=True
        )

        # Warm-up request to obtain cookies and CSRF token
        self.session.get(f"{self.BASE_URL}/shop/search/products")
        logging.info("Initialising Woolworths session…")

    def _sleep(self):
        """Random delay to mimic human browsing."""
        time.sleep(random.uniform(self.min_delay, self.max_delay))

    def _browser_headers(self):
        csrf = self.session.cookies.get("wow.csrf", "")

        """Realistic browser headers Woolworths expects."""
        return {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-AU,en;q=0.9",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": self.BASE_URL,
            "Referer": f"{self.BASE_URL}/shop/search/products",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-User": "?1",
            "Connection": "keep-alive",
            "x-wow-csrf": csrf,

            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),

            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
        }

    def get(self, path: str):
        """GET request for product detail."""
        self._sleep()

        url = f"{self.BASE_URL}{path}"
        headers = self._browser_headers()

        logger.info(f"GET → {url}")
        resp = self.session.get(url, headers=headers)

        if not resp.text:
            logger.warning(f"Empty GET response for {url}")
            return None

        try:
            return resp.json()
        except Exception:
            logger.error("Failed to decode JSON response", exc_info=True)
            return None

    def post(self, path: str, json=None):
        """POST for search only."""
        self._sleep()
        url = f"{self.BASE_URL}{path}"
        headers = self._browser_headers()

        logger.info(f"POST → {url}")
        resp = self.session.post(url, json=json, headers=headers)

        if not resp.text:
            logger.warning(f"Empty POST response for {url}")
            return None

        try:
            return resp.json()
        except Exception:
            logger.error("Failed to decode JSON response", exc_info=True)
            return None