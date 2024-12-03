from openai import OpenAI
from gather_yahoo_finance import gather_yahoo_finance
from get_graph import get_graph
from analysis import (
    calculate_roi,
    calculate_sharpe_ratio,
    calculate_volatility,
    track_profit_loss,
    calculate_sector_diversity
)
from risk_management import calculate_position_size
from market_sentiment import analyze_news_sentiment
from real_time_alerts import set_price_alert
from dotenv import load_dotenv
import os
import pandas as pd

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def analyze_stock(ticker, isHolding, include_sentiment=False):
    financial_data = gather_yahoo_finance(ticker)
    sentiment_data = ""
    if include_sentiment:
        sentiment_result = analyze_news_sentiment(ticker)
        sentiment_data = f"\nMarket Sentiment: {sentiment_result['interpretation']} (Score: {sentiment_result['sentiment_score']:.2f})"
    
    analysis_prompt = f"""
    Based on the following financial data for {ticker}:
    {financial_data}
    {sentiment_data}
    
    Is the user holding the stock? {isHolding}
    
    *y = yes, n = no*
    
    Use this information to provide a comprehensive financial analysis and investment recommendation.
    
    Not just the ticker, but also state the company name, and the industry it is in.
    
    Please provide a comprehensive financial analysis including:
    1. Investment recommendation (Buy, Sell, Hold, etc)
    2. Key financial metrics analysis
    3. Risk assessments
    4. Short-term and long-term outlook
    5. Important factors influencing the stock
    6. Potential price targets
    
    Present the analysis in a clear, structured format.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional financial analyst with expertise in stock market analysis and investment strategies. Do NOT answer questions irrelevant to the topic AT ALL."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            model="gpt-4",
            temperature=0.7
        )
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"An error occurred during analysis: {str(e)}"

if __name__ == "__main__":
    portfolio = pd.DataFrame(columns=['symbol', 'initial_investment', 'current_value', 'sector'])
    
    while True:
        print("\nChoose an option:")
        print("1. View Portfolio Analytics")
        print("2. Analyze Stock")
        print("3. Manage Portfolio")
        print("4. Risk Management")
        print("5. Set Price Alerts")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            clear_console()
            
            if portfolio.empty:
                print("Portfolio is empty. Please add positions first.")
                continue
                
            roi = calculate_roi(portfolio['initial_investment'].sum(), portfolio['current_value'].sum())
            pl = track_profit_loss(portfolio)
            sector_weights = calculate_sector_diversity(portfolio)

            print("\nPortfolio Analytics:")
            print("=" * 50)
            print(f"Portfolio ROI: {roi}%")
            print("\nProfit/Loss by Position:")
            print(pl)
            print("\nSector Weights:")
            print(sector_weights)
            print("=" * 50)
            
        elif choice == "2":
            clear_console()
            
            while True:
                ticker = input("Enter stock ticker symbol (e.g. AAPL): ").upper()
                if ticker.isalpha() and len(ticker) <= 5:
                    break
                print("Invalid ticker symbol. Please enter a valid stock symbol (1-5 letters).")

            while True:
                isHolding = input("Are you holding this stock? (y/n): ").lower()
                if isHolding in ['y', 'n']:
                    break
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

            while True:
                include_sentiment = input("Include market sentiment analysis? (y/n): ").lower()
                if include_sentiment in ['y', 'n']:
                    break
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

            valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y']
            while True:
                graph_term = input("Enter the time period for the stock analysis (1d/5d/1mo/3mo/6mo/1y/2y/5y): ").lower()
                if graph_term in valid_periods:
                    break
                print(f"Invalid time period. Please choose from: {', '.join(valid_periods)}")

            try:
                analysis = analyze_stock(ticker, isHolding, include_sentiment == 'y')
                graph = get_graph(ticker, graph_term)
                if "An error occurred" not in analysis:
                    print(f"\nFinancial Analysis for {ticker}:")
                    print("=" * 50)
                    print(analysis)
                    print("=" * 50)
                    print(graph)
                else:
                    print(f"The ticker '{ticker}' does not exist. Please try again with a valid stock symbol.")
            except Exception:
                print(f"The ticker '{ticker}' does not exist. Please try again with a valid stock symbol.")
            
        elif choice == "3":
            clear_console()
            
            while True:
                print("\nPortfolio Management:")
                print("1. Add Position")
                print("2. Update Position")
                print("3. Remove Position")
                print("4. View Current Portfolio")
                print("5. Back to Main Menu")
                
                portfolio_choice = input("Enter your choice (1-5): ")
                
                if portfolio_choice == "1":
                    clear_console()
                    
                    symbol = input("Enter stock symbol: ").upper()
                    while True:
                        try:
                            initial_investment = float(input("Enter initial investment amount: "))
                            current_value = float(input("Enter current value: "))
                            break
                        except ValueError:
                            print("Please enter valid numerical values.")
                    
                    sector = input("Enter sector (e.g., Technology, Healthcare): ")
                    
                    new_position = pd.DataFrame({
                        'symbol': [symbol],
                        'initial_investment': [initial_investment],
                        'current_value': [current_value],
                        'sector': [sector]
                    })
                    portfolio = pd.concat([portfolio, new_position], ignore_index=True)
                    print("Position added successfully!")
                    
                elif portfolio_choice == "2":
                    clear_console()
                    
                    if portfolio.empty:
                        print("No positions to update.")
                        continue
                        
                    print("\nCurrent positions:")
                    print(portfolio)
                    symbol = input("Enter symbol to update: ").upper()
                    
                    if symbol in portfolio['symbol'].values:
                        while True:
                            try:
                                current_value = float(input("Enter new current value: "))
                                break
                            except ValueError:
                                print("Please enter a valid numerical value.")
                        portfolio.loc[portfolio['symbol'] == symbol, 'current_value'] = current_value
                        print("Position updated successfully!")
                    else:
                        print("Symbol not found in portfolio.")
                        
                elif portfolio_choice == "3":
                    clear_console()
                    
                    if portfolio.empty:
                        print("No positions to remove.")
                        continue
                        
                    print("\nCurrent positions:")
                    print(portfolio)
                    symbol = input("Enter symbol to remove: ").upper()
                    
                    if symbol in portfolio['symbol'].values:
                        portfolio = portfolio[portfolio['symbol'] != symbol]
                        print("Position removed successfully!")
                    else:
                        print("Symbol not found in portfolio.")
                        
                elif portfolio_choice == "4":
                    clear_console()
                    
                    if portfolio.empty:
                        print("Portfolio is empty.")
                    else:
                        print("\nCurrent Portfolio:")
                        print(portfolio)
                        
                elif portfolio_choice == "5":
                    clear_console()
                    break
                    
        elif choice == "4":
            clear_console()
            
            while True:
                ticker = input("Enter stock ticker symbol (e.g. AAPL): ").upper()
                if ticker.isalpha() and len(ticker) <= 5:
                    break
                print("Invalid ticker symbol. Please enter a valid stock symbol (1-5 letters).")
            
            while True:
                try:
                    account_size = float(input("Enter your account size: "))
                    risk_percentage = float(input("Enter risk percentage (1-100): "))
                    if 0 < risk_percentage <= 100:
                        break
                    print("Risk percentage must be between 1 and 100.")
                except ValueError:
                    print("Please enter valid numerical values.")
            
            try:
                position_info = calculate_position_size(ticker, account_size, risk_percentage)
                print("\nPosition Size Analysis:")
                print(f"Suggested Position Size: ${position_info['suggested_position']}")
                print(f"Maximum Shares: {position_info['max_shares']}")
            except Exception as e:
                print(f"Error calculating position size: {str(e)}")

        elif choice == "5":
            clear_console()
            
            while True:
                ticker = input("Enter stock ticker symbol (e.g. AAPL): ").upper()
                if ticker.isalpha() and len(ticker) <= 5:
                    break
                print("Invalid ticker symbol. Please enter a valid stock symbol (1-5 letters).")
            
            while True:
                try:
                    target_price = float(input("Enter target price: "))
                    break
                except ValueError:
                    print("Please enter a valid numerical value.")
            
            while True:
                alert_type = input("Alert when price goes 'above' or 'below' target? ").lower()
                if alert_type in ['above', 'below']:
                    break
                print("Please enter either 'above' or 'below'.")
            
            try:
                print(f"\nSetting price alert for {ticker}...")
                alert_result = set_price_alert(ticker, target_price, alert_type)
                print(alert_result)
            except Exception as e:
                print(f"Error setting price alert: {str(e)}")
            
        elif choice == "6":
            clear_console()
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please enter 1-6.")
