import yfinance as yf


def get_nse_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol + ".NS")  # ".NS" for NSE stocks
        data = stock.history(period="1d")
        
        if not data.empty:
            return {
                'Exchange': 'NSE',
                'Current Price': round(stock.info.get('currentPrice', None), 2) if stock.info.get('currentPrice', None) else None,
                'Opening Price': round(data.iloc[0]['Open'], 2),
                'Closing Price': round(data.iloc[0]['Close'], 2),
                'High': round(data.iloc[0]['High'], 2),
                'Low': round(data.iloc[0]['Low'], 2)
            }
    except Exception as e:
        print(f"NSE Fetch Error: {e}")
    return None

def get_bse_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol + ".BO")  # ".BO" for BSE stocks
        data = stock.history(period="1d")
        
        if not data.empty:
            return {
                'Exchange': 'BSE',
                'Current Price': round(stock.info.get('currentPrice', None), 2) if stock.info.get('currentPrice', None) else None,
                'Opening Price': round(data.iloc[0]['Open'], 2),
                'Closing Price': round(data.iloc[0]['Close'], 2),
                'High': round(data.iloc[0]['High'], 2),
                'Low': round(data.iloc[0]['Low'], 2)
            }
    except Exception as e:
        print(f"BSE Fetch Error: {e}")
    return None

def get_other_exchange_stock_price(symbol):
    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")
        
        if not data.empty:
            return {
                'Exchange': stock.info.get('exchange', 'Other'),
                'Current Price': round(stock.info.get('currentPrice', None), 2) if stock.info.get('currentPrice', None) else None,
                'Opening Price': round(data.iloc[0]['Open'], 2),
                'Closing Price': round(data.iloc[0]['Close'], 2),
                'High': round(data.iloc[0]['High'], 2),
                'Low': round(data.iloc[0]['Low'], 2)
            }
    except Exception as e:
        print(f"Other Exchange Fetch Error: {e}")
    return None

def get_stock_price(symbol):
    stock_data = get_nse_stock_price(symbol)
    if not stock_data:
        stock_data = get_bse_stock_price(symbol)
    if not stock_data:
        stock_data = get_other_exchange_stock_price(symbol)
    
    return stock_data if stock_data else {'Error': 'Stock not found on NSE, BSE, or other exchanges'}
