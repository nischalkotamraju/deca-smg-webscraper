import numpy as np
import yfinance as yf

def calculate_position_size(ticker, account_size, risk_percentage):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    
    daily_volatility = hist['Close'].pct_change().std()
    
    max_position = account_size * (risk_percentage / 100)
    
    suggested_position = max_position * (1 - daily_volatility)
    
    return {
        'suggested_position': round(suggested_position, 2),
        'max_shares': round(suggested_position / stock.info['currentPrice'], 0)
    }
