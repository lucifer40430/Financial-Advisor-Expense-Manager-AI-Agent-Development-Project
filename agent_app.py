from logging import PlaceHolder

import os

import requests

import yfinance as yf

from dotenv import load_dotenv

from langchain_core.tools import tool

from langchain_groq import ChatGroq

from langchain_community.tools import DuckDuckGoSearchRun

from langchain.agents import create_agent



import gradio as gr

load_dotenv()

WEATHERSTACK_API = os.getenv("WEATHERSTACK_API_KEY")


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@tool
def get_stock_price(ticker: str) -> str:
    """
    Use this tool to fetch the current real-time stock price and basic market data for a given ticker symbol.
    Input should be the official stock ticker symbol in uppercase (e.g., 'AAPL' for Apple, 'MSFT' for Microsoft, 'GOOGL' for Google).
    """
    try:
        stock = yf.Ticker(ticker)
        # Fetch current market price info
        info = stock.info
        current_price = info.get('regularMarketPrice') or info.get('currentPrice')
        currency = info.get('currency', 'USD')
        market_cap = info.get('marketCap', 'N/A')
        
        if current_price is None:
            return f"Could not find live price data for ticker {ticker}."
            
        return f"Ticker: {ticker} | Current Price: {current_price} {currency} | Market Cap: {market_cap}"
    except Exception as e:
        return f"Error fetching stock data for {ticker}: {str(e)}"

@tool
def get_stock_trends_and_news(ticker: str) -> str:
    """
    Use this tool to fetch recent news headlines and market trends/sentiment related to a specific stock ticker.
    Input should be the official stock ticker symbol in uppercase (e.g., 'TSLA', 'AMZN').
    """
    try:
        stock = yf.Ticker(ticker)
        news_items = stock.news[:3] # Fetch the top 3 recent news articles
        
        if not news_items:
            return f"No recent news found for ticker {ticker}."
            
        result = f"Recent market trends and news for {ticker}:\n"
        for item in news_items:
            title = item.get('title')
            publisher = item.get('publisher')
            result += f"- {title} (Published by {publisher})\n"
            
        return result
    except Exception as e:
        return f"Error fetching news for {ticker}: {str(e)}"





class SmartAgent:

    def __init__(self):

        print("Initializing SmartAgent...")

        self.groq_key = os.getenv("GROQ_API_KEY")

        self.search_tool = DuckDuckGoSearchRun()
        
        self.llm = ChatGroq(
            model="openai/gpt-oss-20b", temperature=0, api_key=self.groq_key
        )
        
       

        template_string = """Answer the following questions as best you can. You have access to the following tools:



       

{tools}



Use the following format:



Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question



Begin!



Question: {input}

Thought:{agent_scratchpad}"""

        self.agent = create_agent(
            model=self.llm,
            tools=[self.search_tool, get_stock_price, get_stock_trends_and_news],
            system_prompt=template_string,
        )

        print("agent is ready")

    def run_query(self, query):

        print(f"Query:{query}")

        response = self.agent.invoke({"messages": [{"role": "user", "content": query}]})

        return response["messages"][-1].content


def launch_ui():

    print("Launching Gradio UI...")

    agent_system = SmartAgent()

    iface = gr.Interface(
        fn=agent_system.run_query,
        inputs=gr.Textbox(
            label="Ask the Smart Agent",
            placeholder="Enter your query here...",
            lines=2,
        ),
        outputs=gr.Textbox(lines=10),
        title="Smart Agent",
        description="Ask the Smart Agent anything about financial advice and expenses.",
    )

    iface.launch(share=True)


if __name__ == "__main__":

    launch_ui()
