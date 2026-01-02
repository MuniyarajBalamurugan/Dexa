from google.adk.agents import Agent 
from google.adk.tools import google_search

web_search_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-exp",
    description="A simple assistant for real-time Q&A.",
    instruction="Answer briefly using Google Search.",
    tools=[google_search]
)

