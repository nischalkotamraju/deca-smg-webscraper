from openai import OpenAI
from gather_yahoo_finance import gather_yahoo_finance
from get_graph import get_graph
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

def analyze_stock(ticker, isHolding):
    financial_data = gather_yahoo_finance(ticker)
    
    analysis_prompt = f"""
    Based on the following financial data for {ticker}:
    {financial_data}
    
    Is the user holding the stock? {isHolding}
    
    *y = yes, n = no*
    
    Use this information to provide a comprehensive financial analysis and investment recommendation.
    
    Please provide a comprehensive financial analysis including:
    1. Investment recommendation (Buy, Sell, Hold, etc, not limited to these)
    2. Key financial metrics analysis
    3. Risk assessment
    4. Short-term and long-term outlook
    5. Important factors influencing the stock
    6. Potential price targets
    
    Present the analysis in a clear, structured format.

    Don't make the responses too long, though. This is supposed to be short and concise in a way that gets to the point and makes it easy for someone to understand.

    Take out any unnecessary text or formatting that would be in the actual ChatGPT response, such as "**This is an example**". The asterisks are just for formatting, and they get in the way. This is not the only example, but refrain from using things like that. DO NOT use bolding, italics, etc.
    
    Keep a conclusion at the end of every analysis.

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
    while True:
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

        valid_periods = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y']
        while True:
            graph_term = input("Enter the time period for the stock analysis (1d/5d/1mo/3mo/6mo/1y/2y/5y/10y/ytd/max): ").lower()
            if graph_term in valid_periods:
                break
            print(f"Invalid time period. Please choose from: {', '.join(valid_periods)}")

        try:
            analysis = analyze_stock(ticker, isHolding)
            graph = get_graph(ticker, graph_term)
            if "An error occurred" not in analysis:
                print(f"\nFinancial Analysis for {ticker}:")
                print("=" * 50)
                print(analysis)
                
                print("=" * 50)
                print(graph)
                break
            else:
                print(f"The ticker '{ticker}' does not exist. Please try again with a valid stock symbol.")
        except Exception:
            print(f"The ticker '{ticker}' does not exist. Please try again with a valid stock symbol.")
