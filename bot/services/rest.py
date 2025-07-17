from binance.spot import Spot
import os

# Support both Railway.app and local environment variable names
api_key = os.getenv("BINANCE_API_KEY") or os.getenv("API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET") or os.getenv("API_SECRET")
base_url = os.getenv("BASE_URL", "https://testnet.binance.vision")

client = Spot(api_key=api_key,
              api_secret=api_secret,
              base_url=base_url)