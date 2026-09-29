# Personal Chef Agent

Personal Chef Agent is an AI agent built with LangChain that helps users discover recipes and meal ideas based on their requests.

The project explores several important concepts in modern AI agent development, including tool calling, web search, conversational memory, and structured outputs.

## Features

- Natural-language recipe and meal requests
- Web search using Tavily
- AI-controlled tool calling
- Short-term conversational memory
- Stateful conversations using thread IDs
- Gemini-powered agent
- Optional structured recipe responses using Pydantic

## Tech Stack

- Python
- LangChain
- LangGraph
- Google Gemini
- Tavily Search API
- Pydantic

## How It Works

The application uses a LangChain agent connected to external tools.

```text
User Request
     |
     v
LangChain Agent
     |
     +-------------------+
     |                   |
     v                   v
Gemini LLM         Tavily Search Tool
     |                   |
     +---------+---------+
               |
               v
        Recipe Response
               |
               v
      Conversation Memory
```

The model determines whether it can answer directly or whether additional information should be retrieved using the search tool.

## Web Search Tool

The agent has access to a custom search tool powered by Tavily.

Conceptually:

```python
@tool
def search_web(query: str):
    ...
```

The tool allows the agent to retrieve external information when a request benefits from web search.

Rather than manually deciding when search should happen, the tool is exposed to the agent so the model can decide when it is appropriate to use it.

## Agent

The agent is created using LangChain's agent functionality with Gemini as the underlying model.

Example architecture:

```python
agent = create_agent(
    model="google_genai:...",
    tools=[search_web],
    checkpointer=memory
)
```

This combines:

- an LLM
- external tools
- conversation state

into a single agent workflow.

## Short-Term Memory

The project uses LangGraph's:

```python
InMemorySaver
```

to maintain state between messages.

A `thread_id` identifies a conversation:

```python
config = {
    "configurable": {
        "thread_id": "1"
    }
}
```

Messages sent using the same thread can access previous conversational context.

This enables interactions such as:

```text
User: Give me a pasta recipe using mushrooms.

Agent: ...

User: Can you make that vegetarian and spicier?
```

The second request can be interpreted using the previous conversation instead of being treated as an unrelated prompt.

## Structured Output

The project also explores structured responses using Pydantic.

A recipe schema can define fields such as:

```python
class Recipe(BaseModel):
    name: str
    ingredients: list[str]
    instructions: list[str]
```

Structured output makes agent responses easier for other applications or interfaces to consume programmatically.

## Setup

Clone the repository:

```bash
git clone <your-repository-url>
cd personal-chef-agent
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Never commit API keys or `.env` files to GitHub.

## Run

```bash
python3 main.py
```

Then enter a food or recipe request when prompted.

Example:

```text
What ingredients do you have?
> chicken, rice, garlic, onions
```

The agent can use the provided information and its available tools to help generate a recipe.

## What I Learned

This project was built while learning the foundations of AI agents with LangChain and LangGraph.

It gave me hands-on experience with:

- LLM agents
- Tool calling
- Web search integration
- Short-term memory
- Conversation threads
- Structured outputs
- Pydantic schemas
- Gemini integration

The project helped bridge the gap between simple LLM API calls and stateful AI systems that can interact with external tools.
