# Quant Algo Trading Workspace - Groww API

This workspace is set up to develop, test, and run automated trading strategies using the Groww Trading API.

## Directory Structure
- `requirements.txt`: Python package dependencies.
- `.env.template`: Copy to `.env` and fill with credentials.
- `guide.md`: Core guide for daily workflow and algo trading basics.
- `src/groww_helper.py`: Setup wrapper for Groww API clients.
- `notebooks/`:
  - `01_authentication.ipynb`: Test authentication.
  - `02_market_data.ipynb`: Test fetching of stock info, prices, and historical candles.
  - `03_trading_orders.ipynb`: Test order management and portfolio updates.

## Getting Started
1. **Configure Environment Variables:**
   - Copy `.env.template` to `.env`.
   - Update it with your Groww API Key/Secret or TOTP credentials.
2. **Start Jupyter Lab/Notebook:**
   - Launch Jupyter using the virtual environment kernel.
   - Open and run the notebooks in sequence.
