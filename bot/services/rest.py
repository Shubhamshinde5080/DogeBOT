from binance.spot import Spot
import os
client = Spot(api_key=os.getenv("API_KEY"),
              api_secret=os.getenv("API_SECRET"),
              base_url=os.getenv("BASE_URL"))