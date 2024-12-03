from yahoo_fin import stock_info
import time
import yfinance as yf

def set_price_alert(ticker, target_price, alert_type='above'):
    while True:
        current_price = stock_info.get_live_price(ticker)
        if alert_type == 'above' and current_price >= target_price:
            return f"Alert: {ticker} has reached {current_price}, above target {target_price}"
        elif alert_type == 'below' and current_price <= target_price:
            return f"Alert: {ticker} has dropped to {current_price}, below target {target_price}"
        time.sleep(60)
