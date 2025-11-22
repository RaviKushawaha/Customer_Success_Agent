# Customer Support Agent

An AI-powered customer support agent system that can retrieve ticket details from Jira-like systems, search knowledge bases, and address customer concerns intelligently.

## Features

- 🤖 **AI Agent**: Intelligent customer support agent that handles customer queries
- 📋 **Ticket Retrieval**: Fetch ticket details from system of record (Jira-like systems)
- 📚 **Knowledge Base**: Search and retrieve relevant information from knowledge base
- 💬 **Conversational Interface**: Interactive chat interface for customer interactions
- 🔍 **Smart Search**: Semantic search across knowledge base articles
- 📊 **Conversation Tracking**: Maintain conversation history and context


## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone the repository** (or navigate to the project directory)

```bash
cd Customer_Support_Agentic_Systems
```

2. **Create a virtual environment** (recommended)

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here  # Optional, for enhanced AI features

# Ticket System Configuration (Jira)
TICKET_SYSTEM_URL=https://your-jira-instance.atlassian.net
TICKET_SYSTEM_USERNAME=your_username
TICKET_SYSTEM_API_TOKEN=your_api_token

# Knowledge Base Configuration
KNOWLEDGE_BASE_PATH=data/knowledge_base

# Agent Configuration
AGENT_TEMPERATURE=0.7
AGENT_MODEL=gpt-3.5-turbo

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/customer_support_agent.log

# Search Configuration
MAX_SEARCH_RESULTS=5
SIMILARITY_THRESHOLD=0.7
```

## Usage

### Interactive Chat Mode

Run the agent in interactive chat mode:

```bash
python main.py
```

This will start an interactive session where you can:
- Ask questions about issues
- Reference tickets (e.g., "What's the status of PROJ-1001?")
- Type `exit` to quit
- Type `history` to see conversation history

### Demo Mode

Run pre-configured demo queries:

```bash
python main.py demo
```

### Programmatic Usage

```python
from src.agent import CustomerSupportAgent
from src.knowledge_base import KnowledgeBase
from src.ticket_system import TicketRetriever

# Initialize components
kb = KnowledgeBase()
ticket_retriever = TicketRetriever()
agent = CustomerSupportAgent(knowledge_base=kb, ticket_retriever=ticket_retriever)

# Process a query
response = agent.process_query("What's the status of ticket PROJ-1001?")

print(response["response"])
print(f"Ticket details: {response['ticket_details']}")
print(f"Knowledge base results: {response['knowledge_base_results']}")
```

## Key Components

### CustomerSupportAgent

The main agent class that orchestrates ticket retrieval, knowledge base searches, and response generation.

**Methods:**
- `process_query(user_query, conversation_id)`: Process customer query and generate response
- `get_conversation_history(conversation_id)`: Retrieve conversation history
- `clear_conversation_history()`: Clear conversation history

### KnowledgeBase

Manages knowledge base articles and provides search functionality.

**Methods:**
- `search(query, max_results)`: Search knowledge base for relevant articles
- `add_article(title, content, category, tags)`: Add new article to knowledge base
- `get_article_by_id(article_id)`: Retrieve specific article by ID

### TicketRetriever

Retrieves ticket details from Jira-like systems.

**Methods:**
- `get_ticket(ticket_id)`: Retrieve ticket by ID
- `search_tickets(query, max_results)`: Search tickets by query

### TextProcessor

Utility class for text processing operations.

**Methods:**
- `extract_ticket_reference(text)`: Extract ticket reference from text
- `extract_keywords(text)`: Extract keywords from text
- `calculate_similarity(text1, text2)`: Calculate similarity between texts

## Configuration

Configuration is managed through:
1. Environment variables (`.env` file)
2. `config/config.py` (default values)

Key configuration options:
- `TICKET_SYSTEM_URL`: URL of your Jira instance
- `TICKET_SYSTEM_USERNAME`: Username for API authentication
- `TICKET_SYSTEM_API_TOKEN`: API token for authentication
- `KNOWLEDGE_BASE_PATH`: Path to knowledge base directory
- `MAX_SEARCH_RESULTS`: Maximum number of search results
- `SIMILARITY_THRESHOLD`: Minimum similarity score for results

## Ticket System Integration

The system supports integration with Jira and Jira-like systems. To connect to a real Jira instance:

1. Generate an API token from your Jira account
2. Set `TICKET_SYSTEM_URL`, `TICKET_SYSTEM_USERNAME`, and `TICKET_SYSTEM_API_TOKEN` in `.env`
3. The system will automatically use API integration when credentials are provided

For demo purposes, the system uses local ticket storage in `data/tickets.json`.

## Knowledge Base

Knowledge base articles can be stored as JSON files in the `data/knowledge_base/` directory.

Example article format:

```json
{
  "id": "KB-1",
  "title": "How to Reset Your Password",
  "content": "Detailed instructions...",
  "category": "authentication",
  "tags": ["password", "login"],
  "keywords": ["password", "reset", "login"]
}
```

You can also programmatically add articles:

```python
kb = KnowledgeBase()
kb.add_article(
    title="Article Title",
    content="Article content...",
    category="general",
    tags=["tag1", "tag2"]
)
```

## Logging

Logs are written to:
- Console (INFO level and above)
- File: `logs/customer_support_agent.log` (DEBUG level and above)

Configure log level via `LOG_LEVEL` environment variable.

## Examples

### Example 1: Query with Ticket Reference

```python
agent = CustomerSupportAgent()
response = agent.process_query("What's the status of PROJ-1001?")

# Response includes:
# - Ticket details (status, priority, description)
# - Recent comments/updates
# - Relevant knowledge base articles
```

### Example 2: General Query

```python
response = agent.process_query("I'm having login issues. Can you help?")

# Response includes:
# - Relevant knowledge base articles about login
# - Troubleshooting steps
# - Contextual suggestions
```

### Example 3: Knowledge Base Search

```python
kb = KnowledgeBase()
results = kb.search("password reset", max_results=3)

for result in results:
    print(f"{result['title']}: {result['content'][:100]}")
```

## Extending the System

### Adding Custom Ticket Sources

Extend `TicketRetriever` class to add support for other ticket systems:

```python
class CustomTicketRetriever(TicketRetriever):
    def _fetch_ticket_from_api(self, ticket_id):
        # Implement custom API integration
        pass
```

### Enhancing AI Responses

To integrate with OpenAI or other LLM services, modify the `_generate_response` method in `CustomerSupportAgent`:

```python
from openai import OpenAI

client = OpenAI(api_key=Config.OPENAI_API_KEY)

# Use LLM to generate more sophisticated responses
```

### Adding New Knowledge Sources

Extend `KnowledgeBase` to connect to external knowledge sources (databases, APIs, etc.).

## Troubleshooting

### Issue: Tickets not found

- Check that `data/tickets.json` exists with sample tickets
- For real Jira integration, verify API credentials in `.env`
- Check logs for API errors

### Issue: Knowledge base empty

- Ensure `data/knowledge_base/` directory exists
- Add JSON files with articles or use `add_article()` method
- Check file permissions

### Issue: Import errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)


---

**Built with ❤️ by Ravi Kush**

