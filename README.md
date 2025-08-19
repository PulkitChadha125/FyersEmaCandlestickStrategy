# Fyers EMA with Candle - Automated Trading System

A Python-based automated trading system that implements an Exponential Moving Average (EMA) strategy with candle analysis using the Fyers API for Indian stock markets.

## 🚀 Features

- **Automated Trading**: Execute trades based on EMA crossover signals
- **Multi-Symbol Support**: Trade multiple stocks simultaneously
- **Real-time Data**: Live market data streaming via Fyers WebSocket
- **Risk Management**: Configurable stop-loss and position sizing
- **Time-based Trading**: Trade only during specified market hours
- **Comprehensive Logging**: Detailed order and trade logs

## 📋 Prerequisites

- Python 3.7 or higher
- Fyers trading account with API access
- Valid Fyers API credentials
- Internet connection for real-time data

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Fyers credentials:**
   - Edit `FyersCredentials.csv` with your API details
   - Ensure you have the correct client ID, secret key, and TOTP key

4. **Configure trading parameters:**
   - Edit `TradeSettings.csv` to specify:
     - Stock symbols to trade
     - Quantity per trade
     - Timeframe (e.g., 5 minutes)
     - EMA period (e.g., 21)
     - Trading start/stop times
     - Risk amount per trade

## ⚙️ Configuration

### FyersCredentials.csv
Contains your Fyers API authentication details:
- Client ID
- Secret Key
- FY ID
- TOTP Key
- PIN
- Redirect URI

### TradeSettings.csv
Configure your trading strategy parameters:
- **Symbol**: Stock symbol (e.g., RELIANCE, TCS)
- **Quantity**: Number of shares per trade
- **FyersTf**: Timeframe in minutes (e.g., 5 for 5-minute candles)
- **MA1**: EMA period (e.g., 21 for 21-period EMA)
- **StartTime**: Market opening time for trading
- **Stoptime**: Market closing time for trading
- **RiskAmount**: Maximum risk per trade

## 🚀 Usage

### Running the Application

1. **Start the main application:**
   ```bash
   python main.py
   ```

2. **For executable version:**
   ```bash
   ./main.exe
   ```

### Trading Strategy

The system implements an EMA crossover strategy:
- **Entry Signal**: When price crosses above the EMA
- **Exit Signal**: When price crosses below the EMA or stop-loss is hit
- **Time-based**: Only trades during configured market hours
- **Risk Management**: Automatic stop-loss based on timeframe

## 📊 Key Components

### Main Files

- **`main.py`**: Main application logic and trading engine
- **`FyresIntegration.py`**: Fyers API integration and authentication
- **`Fyres activation.py`**: API activation and token management

### Data Files

- **`FyersCredentials.csv`**: API credentials
- **`TradeSettings.csv`**: Trading configuration
- **`OrderLog.txt`**: Trade execution logs

### Log Files

- **`fyersApi.log`**: API interaction logs
- **`fyersDataSocket.log`**: WebSocket data logs
- **`fyersRequests.log`**: HTTP request logs

## 🔧 Dependencies

- **`pandas`**: Data manipulation and analysis
- **`polars`**: Fast DataFrame operations
- **`polars-talib`**: Technical analysis indicators
- **`fyers-apiv3`**: Fyers trading API
- **`pyotp`**: Time-based one-time password generation
- **`requests`**: HTTP requests
- **`pytz`**: Timezone handling
- **`pyarrow`**: Data serialization

## ⚠️ Important Notes

- **Paper Trading**: Test thoroughly with paper trading before live trading
- **Risk Management**: Never risk more than you can afford to lose
- **Market Hours**: System only trades during NSE market hours (9:15 AM - 3:30 PM IST)
- **API Limits**: Be aware of Fyers API rate limits and usage policies
- **Backup**: Keep regular backups of your configuration files

## 📝 Logging

The system maintains comprehensive logs:
- **Order Execution**: All buy/sell orders with timestamps
- **API Interactions**: Authentication and data requests
- **WebSocket Data**: Real-time market data streaming
- **Error Handling**: Detailed error logs for debugging

## 🚨 Disclaimer

This software is for educational and informational purposes only. Trading involves substantial risk of loss and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a qualified financial advisor before making investment decisions.

## 🤝 Support

For issues or questions:
1. Check the log files for error details
2. Verify your Fyers API credentials
3. Ensure all dependencies are properly installed
4. Check your internet connection for real-time data

## 📄 License

This project is provided as-is for educational purposes. Use at your own risk.

---

**Note**: This is an automated trading system. Please ensure you understand the risks involved and test thoroughly before using with real money.
