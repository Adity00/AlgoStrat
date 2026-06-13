Algo Trading Crash Course (Groww API SDK)
This guide provides a practical crash course on the essentials of using the Groww API SDK. It covers importing files from parent directories, authenticating, checking account details, fetching market data, and placing orders.

1. Setup & Resolving the ImportError
   When running Jupyter Notebooks inside the notebooks/ directory, Python's module search path (sys.path) defaults to the notebooks/ directory. Since the helper library src is in the root directory, you must add the parent directory to sys.path.

Here is the boilerplate initialization code you should place at the top of every notebook:

python

import sys
import os

# 1. Add the parent directory (project root) to sys.path

sys.path.append(os.path.abspath(os.path.join('..')))

# 2. Import packages

from src.groww_helper import GrowwHelper
from growwapi import GrowwAPI
import pandas as pd
print("Setup complete! Groww SDK and helpers successfully imported.") 2. Authentication & Client Initialization
To execute requests, you need to create an authenticated GrowwAPI client. The helper handles the environment configuration and generates a dynamic OTP token automatically:

python

# Initialize client

try:
groww = GrowwHelper.get_api_client()
print("Groww Client Authenticated Successfully!")
except Exception as e:
print(f"Failed to authenticate: {e}") 3. Retrieving Account, Holdings, & Positions
Once authenticated, use these methods to check your account status, funds, and portfolio details:

A. Check User Profile Details
Get information about your logged-in profile:

python

profile = groww.get_user_profile()
print("Account Profile Details:", profile)
B. Check Available Margin & Funds
Find out how much money is available in your account to place trades:

python

margin_info = groww.get_available_margin_details()
print("Available Margins:", margin_info)
C. Check User Holdings (Long-term Portfolio)
Fetch all equity holdings currently stored in your Demat account:

python

holdings = groww.get_holdings_for_user()
print("Current Holdings:", holdings)
D. Check Positions (Intraday & Active F&O Trades)
Fetch all active intraday or derivative positions:

python

positions = groww.get_positions_for_user()
print("Active Positions:", positions) 4. Fetching Market Data
Before trading, you need to verify instrument codes and fetch real-time or historical prices.

A. Fetch Live Price (LTP) or Market Quote
python

# Fetch Quote details for an instrument

quote = groww.get_quote(
exchange=groww.EXCHANGE_NSE,
segment=groww.SEGMENT_CASH,
trading_symbol="SBIN"
)
print(f"SBIN Quote: {quote}")
print(f"SBIN Last Traded Price (LTP): {quote.get('ltp')}")
B. Fetch Historical Candles (for Strategy Analysis)
python

# Fetch daily candles for the past month

candles = groww.get_historical_candles(
exchange=groww.EXCHANGE_NSE,
segment=groww.SEGMENT_CASH,
trading_symbol="SBIN",
interval=groww.CANDLE_INTERVAL_DAY,
from_date="2026-05-01",
to_date="2026-06-01"
)

# Convert to a Pandas DataFrame for easy analysis

df = pd.DataFrame(candles)
print(df.head()) 5. Execution: Placing, Modifying, & Cancelling Orders
Use these methods to submit trades. Be extremely cautious; orders sent here are processed live.

A. Place a Limit Buy Order
python

# Place a Limit order to buy 1 share of SBIN at 800.00

buy_order = groww.place_order(
exchange=groww.EXCHANGE_NSE,
segment=groww.SEGMENT_CASH,
transaction_type=groww.TRANSACTION_TYPE_BUY,
order_type=groww.ORDER_TYPE_LIMIT,
product=groww.PRODUCT_CNC, # CNC for Delivery, MIS for Intraday
trading_symbol="SBIN",
quantity=1,
price=800.00,
validity=groww.VALIDITY_DAY
)
print("Buy Order Result:", buy_order)
B. View Order Book & Order Details
python

# Fetch all orders placed today

orders = groww.get_order_list()
print("Today's Orders:", orders)

# Get specific order status

if buy_order:
order_id = buy_order.get("order_id")
order_status = groww.get_order_status(order_id)
print("Order Status:", order_status)
C. Modify an Open Order
python

# Modify order price to 795.00

if buy_order:
modified_order = groww.modify_order(
order_id=buy_order.get("order_id"),
price=795.00,
quantity=1,
order_type=groww.ORDER_TYPE_LIMIT
)
print("Modified Order Result:", modified_order)
D. Cancel an Open Order
python

# Cancel the order completely

if buy_order:
cancelled_order = groww.cancel_order(order_id=buy_order.get("order_id"))
print("Cancelled Order Result:", cancelled_order) 6. Algorithmic Trading Rules & Safety Best Practices
CAUTION

No Rate Limit Protection by Default: If you query APIs inside a while True: loop without time.sleep(), the SDK or exchange will throttle or block your key. Always add a pause (e.g., time.sleep(1)) inside polling loops.

WARNING

Use Limit Orders over Market Orders: Market orders in low-volume stocks can suffer from severe slippage, causing execution at unfavorable prices. Use limit orders whenever possible.

IMPORTANT

Implement a Kill Switch: Always wrap your live trading loops in a try-except block to gracefully handle exceptions and cancel all pending orders on keyboard interruption (Ctrl+C):

python

try:
while True: # your trading strategy logic
pass
except KeyboardInterrupt:
print("Kill switch activated! Cancelling all open orders...") # implement logic to fetch and cancel all open orders
