from binance.spot import Spot
import os

# Support both Railway.app and local environment variable names
api_key = os.getenv("BINANCE_API_KEY") or os.getenv("API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET") or os.getenv("API_SECRET")
base_url = os.getenv("BASE_URL", "https://testnet.binance.vision")

# Safety check for BASE_URL
if not base_url or not base_url.startswith("http"):
    raise ValueError(f"❌ BASE_URL env var missing or wrong: '{base_url}' - should start with 'http'")

print(f"✅ REST API initialized with BASE_URL: {base_url}")

client = Spot(api_key=api_key,
              api_secret=api_secret,
              base_url=base_url)