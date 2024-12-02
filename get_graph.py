def get_graph(ticker_symbol, period='1y'):
    import yfinance as yf
    from asciichartpy import plot
    
    stock = yf.Ticker(ticker_symbol)
    hist = stock.history(period=period)
    
    prices = hist['Close'].tolist()
    sampled_prices = prices[::5]
    
    config = {
        'height': 8,
        'format': '{:6.1f}'
    }
    
    print(f"\n{ticker_symbol}")
    print("-" * 50)
    
    print(plot(sampled_prices, config))
    
    print(f"\nStart: ${prices[0]:.1f} | End: ${prices[-1]:.1f}")
    
    return hist
