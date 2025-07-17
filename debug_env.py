#!/usr/bin/env python3
"""
Quick environment variable debug script for Railway
"""
import os

print("🔍 ALL ENVIRONMENT VARIABLES:")
for key, value in sorted(os.environ.items()):
    if any(term in key.upper() for term in ['API', 'BASE', 'URL', 'BINANCE', 'DAILY', 'FDUSD', 'PORT']):
        # Hide sensitive values
        display_value = value[:10] + '...' if len(value) > 10 else value
        print(f"   {key} = {display_value}")

print("\n🎯 EXPECTED VARIABLES:")
expected = ['BINANCE_API_KEY', 'BINANCE_API_SECRET', 'BINANCE_BASE_URL', 'DAILY_TARGET', 'FDUSD_CAP']
for var in expected:
    value = os.getenv(var)
    status = '✅' if value else '❌'
    print(f"   {status} {var} = {value[:10] + '...' if value and len(value) > 10 else value}")
