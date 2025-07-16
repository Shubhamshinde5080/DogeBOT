#!/usr/bin/env python3
"""
DogeBot Account & Price Monitor
Run this script to check current prices and account balances
"""

import sys
import os
sys.path.append('/app')

from bot.utils.account_monitor import AccountMonitor
import argparse

def main():
    parser = argparse.ArgumentParser(description='DogeBot Account & Price Monitor')
    parser.add_argument('--balance', '-b', action='store_true', help='Show account balance')
    parser.add_argument('--price', '-p', action='store_true', help='Show current prices')
    parser.add_argument('--all', '-a', action='store_true', help='Show everything')
    parser.add_argument('--symbol', '-s', default='DOGEFDUSD', help='Symbol to check (default: DOGEFDUSD)')
    
    args = parser.parse_args()
    
    monitor = AccountMonitor()
    
    if args.all or (not args.balance and not args.price):
        monitor.print_account_summary()
    else:
        if args.balance:
            print("💰 Account Balances:")
            balances = monitor.get_account_balance()
            for asset, balance in balances.items():
                if balance['total'] > 0.001:
                    print(f"  {asset:>8}: {balance['total']:>12.6f}")
        
        if args.price:
            print("📊 Current Prices:")
            
            doge_fdusd = monitor.get_current_price("DOGEFDUSD")
            if doge_fdusd:
                print(f"  DOGEFDUSD: ${doge_fdusd:.6f}")
            
            doge_fdusd = monitor.get_dogefdusd_price()
            if doge_fdusd:
                print(f"  DOGEFDUSD: ${doge_fdusd:.6f}")
            
            if args.symbol != "DOGEFDUSD":
                custom_price = monitor.get_current_price(args.symbol)
                if custom_price:
                    print(f"  {args.symbol}: ${custom_price:.6f}")

if __name__ == "__main__":
    main()
