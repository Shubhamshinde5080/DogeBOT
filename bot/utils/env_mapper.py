#!/usr/bin/env python3
"""
Environment Variable Mapper for Railway.app Deployment
======================================================
Maps Railway.app environment variables to internal bot variables
"""

import os

def setup_environment():
    """Set up environment variables for Railway.app compatibility"""
    
    # Map Railway.app variables to internal variables
    if os.getenv("BINANCE_API_KEY") and not os.getenv("API_KEY"):
        os.environ["API_KEY"] = os.getenv("BINANCE_API_KEY")
    
    if os.getenv("BINANCE_API_SECRET") and not os.getenv("API_SECRET"):
        os.environ["API_SECRET"] = os.getenv("BINANCE_API_SECRET")
    
    # Set default base URL if not provided
    if not os.getenv("BASE_URL"):
        os.environ["BASE_URL"] = "https://testnet.binance.vision"
    
    # Map FDUSD-specific variables
    if os.getenv("DOGEFDUSD_DAILY_TARGET_USD") and not os.getenv("DAILY_TARGET"):
        os.environ["DAILY_TARGET"] = os.getenv("DOGEFDUSD_DAILY_TARGET_USD")
    
    if os.getenv("DOGEFDUSD_MAX_FUND_USD") and not os.getenv("FDUSD_CAP"):
        os.environ["FDUSD_CAP"] = os.getenv("DOGEFDUSD_MAX_FUND_USD")
    
    # Log environment setup
    print("🔧 Environment variables mapped for Railway.app deployment")
    print(f"   API_KEY: {'✅' if os.getenv('API_KEY') else '❌'}")
    print(f"   API_SECRET: {'✅' if os.getenv('API_SECRET') else '❌'}")
    print(f"   BASE_URL: {os.getenv('BASE_URL')}")
    print(f"   DAILY_TARGET: {os.getenv('DAILY_TARGET', '6')}")
    print(f"   FDUSD_CAP: {os.getenv('FDUSD_CAP', '1100')}")

if __name__ == "__main__":
    setup_environment()
