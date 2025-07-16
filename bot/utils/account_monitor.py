"""
Account monitoring utilities for DogeBot
"""
import os
import logging
from binance.spot import Spot
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class AccountMonitor:
    def __init__(self):
        load_dotenv()
        
        # Get environment variables
        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_SECRET')
        base_url = os.getenv('BASE_URL', 'https://testnet.binance.vision')
        
        print(f"🔧 Initializing with base_url: {base_url}")
        print(f"🔑 API Key present: {'Yes' if api_key else 'No'}")
        print(f"🔐 API Secret present: {'Yes' if api_secret else 'No'}")
        
        # Initialize authenticated client for account operations
        if api_key and api_secret:
            try:
                self.client = Spot(
                    api_key=api_key,
                    api_secret=api_secret,
                    base_url=base_url
                )
                print("✅ Authenticated client initialized")
            except Exception as e:
                print(f"❌ Failed to initialize authenticated client: {e}")
                self.client = None
        else:
            print("⚠️ No API credentials found - balance checking will not work")
            self.client = None
            
        # Public client for price data (no authentication needed)
        try:
            self.public_client = Spot(base_url='https://api.binance.com')
            print("✅ Public client initialized")
        except Exception as e:
            print(f"❌ Failed to initialize public client: {e}")
            self.public_client = None
    
    def get_account_balance(self):
        """Get account balances for relevant assets"""
        if not self.client:
            print("❌ No authenticated client available - check your API credentials")
            return {}
            
        try:
            account_info = self.client.account()
            balances = {}
            
            for balance in account_info['balances']:
                asset = balance['asset']
                free = float(balance['free'])
                locked = float(balance['locked'])
                total = free + locked
                
                # Only show assets with non-zero balance
                if total > 0.001:  # Small threshold to avoid dust
                    balances[asset] = {
                        'free': free,
                        'locked': locked,
                        'total': total
                    }
            
            return balances
            
        except Exception as e:
            logger.error(f"❌ Failed to get account balance: {e}")
            return {}
    
    def get_current_price(self, symbol="DOGEFDUSD"):
        """Get current price for a symbol"""
        try:
            ticker = self.client.ticker_price(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            logger.error(f"❌ Failed to get price for {symbol}: {e}")
            return None
    
    def get_dogefdusd_price(self):
        """Get current DOGEFDUSD price"""
        return self.get_current_price("DOGEFDUSD")
    
    def get_24h_ticker(self, symbol="DOGEFDUSD"):
        """Get 24h ticker statistics"""
        try:
            ticker = self.client.ticker_24hr(symbol=symbol)
            return {
                'symbol': ticker['symbol'],
                'price': float(ticker['lastPrice']),
                'change': float(ticker['priceChange']),
                'change_percent': float(ticker['priceChangePercent']),
                'high': float(ticker['highPrice']),
                'low': float(ticker['lowPrice']),
                'volume': float(ticker['volume'])
            }
        except Exception as e:
            logger.error(f"❌ Failed to get 24h ticker for {symbol}: {e}")
            return None
    
    def print_account_summary(self):
        """Print a formatted account summary"""
        print("🏦 Account Summary")
        print("=" * 50)
        
        # Get balances
        balances = self.get_account_balance()
        if balances:
            print("\n💰 Account Balances:")
            for asset, balance in balances.items():
                if balance['total'] > 0.001:  # Only show meaningful balances
                    print(f"  {asset:>8}: {balance['free']:>12.6f} (free) + {balance['locked']:>12.6f} (locked) = {balance['total']:>12.6f}")
        else:
            print("❌ Unable to fetch account balances")
        
        # Get DOGE prices
        print("\n📊 Current Prices:")
        
        doge_fdusd_price = self.get_current_price("DOGEFDUSD")
        if doge_fdusd_price:
            print(f"  DOGEFDUSD: ${doge_fdusd_price:.6f}")
        
        # Get 24h stats
        print("\n📈 24h Statistics (DOGEFDUSD):")
        ticker = self.get_24h_ticker("DOGEFDUSD")
        if ticker:
            change_emoji = "📈" if ticker['change'] >= 0 else "📉"
            print(f"  Price: ${ticker['price']:.6f}")
            print(f"  Change: {change_emoji} {ticker['change']:+.6f} ({ticker['change_percent']:+.2f}%)")
            print(f"  High: ${ticker['high']:.6f}")
            print(f"  Low: ${ticker['low']:.6f}")
            print(f"  Volume: {ticker['volume']:,.0f} DOGE")
        
        print(f"\n🕐 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)

# Create global monitor instance
monitor = AccountMonitor()
