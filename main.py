# main.py
import argparse
import json
import time
import logging
from trade_bot import TradeBot
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trade_bot_logs.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def validate_input(args):
    if not args.api_key or not args.api_secret:
        logger.error("API key and secret are required")
        return False

    # Skip the rest of validation if not placing an order
    if not args.order_type:
        return True

    if args.side not in ['BUY', 'SELL']:
        logger.error("Side must be either 'BUY' or 'SELL'")
        return False

    if args.order_type not in ['MARKET', 'LIMIT', 'STOP_LIMIT', 'OCO']:
        logger.error("Order type must be one of 'MARKET', 'LIMIT', 'STOP_LIMIT', or 'OCO'")
        return False

    if args.quantity is None or args.quantity <= 0:
        logger.error("Quantity must be greater than 0")
        return False

    if args.order_type in ['LIMIT', 'STOP_LIMIT', 'OCO'] and (args.price is None or args.price <= 0):
        logger.error("Price must be greater than 0 for LIMIT, STOP_LIMIT, and OCO orders")
        return False

    if args.order_type in ['STOP_LIMIT', 'OCO'] and (args.stop_price is None or args.stop_price <= 0):
        logger.error("Stop price must be greater than 0 for STOP_LIMIT and OCO orders")
        return False

    if args.order_type == 'OCO' and (args.stop_limit_price is None or args.stop_limit_price <= 0):
        logger.error("Stop-limit price must be greater than 0 for OCO orders")
        return False

    return True

def main():
    parser = argparse.ArgumentParser(description='Binance Trading Bot')
    
    # Authentication
    parser.add_argument('--api-key', required=True, help='Binance API key')
    parser.add_argument('--api-secret', required=True, help='Binance API secret')
    parser.add_argument('--testnet', action='store_true', default=True, 
                       help='Use testnet (default: True)')
    
    # Order parameters
    parser.add_argument('--symbol', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], 
                       help='Order side')
    parser.add_argument('--order-type',  choices=['MARKET', 'LIMIT', 'STOP_LIMIT', 'OCO'],
                       help='Order type')
    parser.add_argument('--quantity', type=float, 
                       help='Order quantity')
    parser.add_argument('--price', type=float, help='Limit price')
    parser.add_argument('--stop-price', type=float, help='Stop price')
    parser.add_argument('--stop-limit-price', type=float, 
                       help='Stop limit price (for OCO orders)')
    
    # Additional commands
    parser.add_argument('--account-info', action='store_true', 
                       help='Show account information')
    parser.add_argument('--open-orders', action='store_true', 
                       help='Show open orders')
    parser.add_argument('--cancel-order', type=int, help='Cancel order by ID')
    parser.add_argument('--current-price', action='store_true',
                       help='Get current price of the symbol')
    parser.add_argument('--order-status', type=int, 
                       help='Get status of an order by ID')
    
    args = parser.parse_args()
    
    # Validate inputs
    if not validate_input(args):
        return 1
    
    try:
        # Initialize bot
        bot = TradeBot(
            api_key=args.api_key,
            api_secret=args.api_secret,
            testnet=args.testnet
        )
        
        # Handle information requests
        if args.account_info:
            account_info = bot.get_account_info()
            print(json.dumps(account_info, indent=2))
            return 0
        if args.current_price:
            if not args.symbol:
                logger.error("Symbol is required to get current price")
            else:
                price=bot.get_current_price(args.symbol)
                print(f"Current price for {args.symbol}: {price}")
            return 0    
        
        if args.open_orders:
            orders = bot.get_open_orders(args.symbol)
            print(json.dumps(orders, indent=2))
            return 0
        
        if args.cancel_order:
            result = bot.cancel_order(args.symbol, args.cancel_order)
            print(json.dumps(result, indent=2))
            return 0
        if args.order_status:
            status = bot.get_order_status(args.symbol, args.order_status)
            print(json.dumps(status, indent=2))
            return 0
        
        # Place orders
        if args.order_type == 'MARKET':
            order = bot.place_market_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
            )
        
        elif args.order_type == 'LIMIT':
            order = bot.place_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
            )
        
        elif args.order_type == 'STOP_LIMIT':
            order = bot.place_stop_limit_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
                stop_price=args.stop_price,
            )
        
        elif args.order_type == 'OCO':
            if not args.stop_limit_price:
                logger.error("Stop limit price required for OCO orders")
                return 1
            
            order = bot.place_oco_order(
                symbol=args.symbol,
                side=args.side,
                quantity=args.quantity,
                price=args.price,
                stop_price=args.stop_price,
                stop_limit_price=args.stop_limit_price
            )
        
        # Display order details
        print("\n=== ORDER PLACED SUCCESSFULLY ===")
        print(json.dumps(order, indent=2))
        
        return 0
        
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())