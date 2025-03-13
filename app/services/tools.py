import requests
from app.config import config

def fetch_crypto_price(coin: str) -> str:
    """Fetches cryptocurrency price from an external API."""
    try:
        params = {"ids": coin, "vs_currencies": "usd"}
        response = requests.get(config.CRYPTO_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return str(data.get(coin, {}).get("usd", "Price unavailable"))
    except requests.exceptions.RequestException:
        return "Error fetching crypto price."

def translate(text: str, language: str) -> str:
    """Dummy translation function – Extend with a real API if needed."""
    return f"(Translated to {language}): {text}"
