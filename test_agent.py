from langchain_agent import LangChainSQLAgent
from database import Database
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

db = Database()
agent = LangChainSQLAgent(db, openai_api_key=os.getenv("OPENAI_API_KEY"))

# Run a test query (use asyncio for async process_query)
async def main():
    result = await agent.process_query("Top factory downtime reasons")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())