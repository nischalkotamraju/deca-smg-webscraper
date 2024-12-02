def gather_yahoo_finance(query):
    import yfinance as yf
    import pandas as pd
    
    try:
        ticker = yf.Ticker(query)
        info = ticker.info
        history = ticker.history(period="1mo")

        data = {
            "Symbol": query,
            "Company Name": info.get('longName', 'N/A'),
            "Current Price": info.get('currentPrice', 'N/A'),
            "52 Week High": info.get('fiftyTwoWeekHigh', 'N/A'),
            "52 Week Low": info.get('fiftyTwoWeekLow', 'N/A'),
            "Market Cap": info.get('marketCap', 'N/A'),
            "Volume": info.get('volume', 'N/A'),
            "Average Volume": info.get('averageVolume', 'N/A'),
            "PE Ratio": info.get('trailingPE', 'N/A'),
            "EPS": info.get('trailingEps', 'N/A'),
            "Dividend Yield": info.get('dividendYield', 'N/A') * 100 if info.get('dividendYield') else 'N/A',
            "1 Month Return": ((history['Close'].iloc[-1] / history['Close'].iloc[0]) - 1) * 100
        }
        
        return pd.DataFrame([data])
    except Exception as e:
        print(f"Error fetching data for {query}: {str(e)}")
        return pd.DataFrame()