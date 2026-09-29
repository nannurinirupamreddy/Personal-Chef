from langchain.agents import create_agent
from langchain.tools import tool
from tavily import TavilyClient
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
from pydantic import BaseModel
from typing import List

class Recipe(BaseModel):
    recipe_name: str
    ingredients: List[str]
    process: List[str]

load_dotenv()

@tool('search_web', description="a tool to search the web, the tool takes a prompt mentioning the ingredients")
def search_web(query: str):
    client = TavilyClient()

    return client.search(query)

agent = create_agent(
    model="google_genai:gemini-3.5-flash", 
    tools=[search_web],
    checkpointer=InMemorySaver(),
    # response_format=Recipe
)

config = {
    "configurable": {
        "thread_id": "1"
    }
}

while True:
    message = HumanMessage(content=input("Enter your message: "))

    if message.content.lower() == "exit":
        break

    response = agent.invoke(
        {"messages": [
            (SystemMessage(content="You are a personal chef, give a recipe based on the ingredients, you can use the necessary tools for the recipe.")),
            message
        ]},
        config
    )

    result = response["messages"][-1].content

    print(result[0]["text"])
    # When returning response, for the process fields, give it as a list of steps.

    # print(response.recipe_name)

    