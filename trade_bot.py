import logging
import json
import time
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from typing import Dict, List, Optional, Any
import argparse
import sys
import os


logger= logging.getLogger(__name__)

class TradeBot:
    def __init__(self, api_key: str, api_secret: str, testnet):
        self.api_key= api_key
        self.api_secret= api_secret
        self.testnet= testnet

        try:
            self.client= Client(
                api_key= api_key,
                api_secret= api_secret,
                
            )
            if testnet:
                self.client.API_URL='https://testnet.binance.vision/api'
            self.client.ping()
            logger.info("Successfully connected to Binance Spot API")

            account_info= self.client.get_account()
            logger.info(f"Account info retrieved successfully: {account_info}")

        except Exception as e:
            logger.error(f"Failed to initialize Binance client:{e}")
            raise

    def get_account_info(self) -> Dict:

        try:
            account_info=self.client.get_account()
            logger.info("Retrieved account information")
            return account_info
        except BinanceAPIException as e:
            logger.error(f"API retrival failed: {e}")
            raise

    def get_current_price(self, symbol:str)-> float:
        try:

            ticker= self.client.get_symbol_ticker(symbol= symbol)
            price= float(ticker['price'])
            logger.info(f"current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"API error getting current proce for {symbol}: {e}")
            raise

    def place_market_order(self, symbol:str, side:str, quantity:float) ->Dict:

        try:
            logger.info(f"Placing market order: {side}, {quantity}, {symbol}")
            
            order= self.client.create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )

            logger.info(f"Market order placed successfully:{order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error placing market order: {e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"API error placing market order:{e}")
            raise

    def place_limit_order(self, symbol:str, side:str, quantity:float,
                          price:float, time_in_force:str='GTC')-> Dict:
        try:
            logger.info(f"Placing limit order:{side},{quantity},{symbol}")
            order= self.client.create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price, #f"{price:.8f}",  # Ensure price is formatted correctly
                timeInForce=time_in_force,

            )  
            logger.info(f"Limit order placed successfully: {order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error placing limit order:{e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"API error placing limit order:{e}")
            raise

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float,
                               price: float, stop_price: float, time_in_force='GTC') -> Dict:
        # type: ignore
        try:
            logger.info(f"Placing stop-limit order: {side}, {quantity}, {symbol}, {price}, {stop_price}")
            order = self.client.create_order(
                symbol=symbol,
                side=side,
                type='STOP_LOSS_LIMIT',
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            logger.info(f"Stop-limit order placed successfully: {order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error placing stop-limit order: {e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"API error placing stop-limit order: {e}")
            raise

    def place_oco_order(self, symbol: str, side: str, quantity: float,
                        price: float, stop_price: float, 
                        stop_limit_price: float, time_in_force: str = 'GTC') -> Dict:
        try:
            logger.info(f"Placing OCO order: {side}, {quantity}, {symbol}, limit: {price}, stop: {stop_price}, stop_limit: {stop_limit_price}")
            order = self.client.create_oco_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                stopLimitPrice=stop_limit_price,
                stopLimitTimeInForce=time_in_force
            )
            logger.info(f"OCO order placed successfully: {order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error placing OCO order: {e}")
            raise   
        except BinanceAPIException as e:
            logger.error(f"API error placing OCO order: {e}")
            raise

    def  cancel_order(self, symbol: str, order_id:int) -> Dict:
        try:
            logger.info(f"Cancelling order: {order_id} for {symbol}")

            order= self.client.cancel_order(
                symbol=symbol,
                orderId=order_id    
            )  

            logger.info(f"Order cancelled successfully: {order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error cancelling order: {e}")
            raise
        except BinanceAPIException as e:
            logger.error(f"API error cancelling order: {e}")
            raise

    def get_order_status(self, symbol:str, order_id:int) ->Dict:

        try:

            order= self.client.get_order(
                symbol=symbol,
                orderId=order_id
            )     
            logger.info(f"Order status retrieved successfully: {order}")
            return order
        except BinanceOrderException as e:
            logger.error(f"Order error getting order status: {e}")
            raise   
        except BinanceAPIException as e:
            logger.error(f"API error getting order status: {e}")
            raise

    def get_open_orders(self, symbol:str = None) -> List[Dict]: 
        try:

            order= self.client.get_open_orders(
                symbol=symbol
            ) 
            logger.info(f"Retrieved {len(order)} open orders")
            return order
        except BinanceAPIException as e:    
            logger.error(f"API error getting open orders: {e}")
            raise
