"""
Example usage of Customer Support Agent
This file demonstrates how to use the agent programmatically
"""

from src.agent import CustomerSupportAgent
from src.knowledge_base import KnowledgeBase
from src.ticket_system import TicketRetriever
from src.utils.logger import setup_logger

logger = setup_logger("Example")


def example_basic_usage():
    """Example 1: Basic usage with ticket reference"""
    print("\n" + "="*60)
    print("Example 1: Basic Usage - Query with Ticket Reference")
    print("="*60 + "\n")
    
    # Initialize agent
    agent = CustomerSupportAgent()
    
    # Process a query with ticket reference
    query = "What's the status of ticket PROJ-1001?"
    response = agent.process_query(query)
    
    print(f"Query: {query}\n")
    print(f"Response:\n{response['response']}\n")
    print(f"Ticket Found: {response['ticket_details'] is not None}")
    print(f"Knowledge Base Results: {len(response['knowledge_base_results'])}")


def example_knowledge_base_search():
    """Example 2: Knowledge base search"""
    print("\n" + "="*60)
    print("Example 2: Knowledge Base Search")
    print("="*60 + "\n")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Search for relevant articles
    query = "password reset"
    results = kb.search(query, max_results=3)
    
    print(f"Search Query: '{query}'\n")
    print(f"Found {len(results)} relevant articles:\n")
    
    for idx, article in enumerate(results, 1):
        print(f"{idx}. {article['title']}")
        print(f"   Category: {article['category']}")
        print(f"   Relevance Score: {article.get('relevance_score', 0):.2f}")
        print(f"   Content Preview: {article['content'][:100]}...")
        print()


def example_ticket_retrieval():
    """Example 3: Ticket retrieval"""
    print("\n" + "="*60)
    print("Example 3: Ticket Retrieval")
    print("="*60 + "\n")
    
    # Initialize ticket retriever
    ticket_retriever = TicketRetriever()
    
    # Retrieve a ticket
    ticket_id = "PROJ-1002"
    ticket = ticket_retriever.get_ticket(ticket_id)
    
    if ticket:
        print(f"Ticket ID: {ticket['id']}")
        print(f"Title: {ticket['title']}")
        print(f"Status: {ticket['status']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Description: {ticket['description'][:200]}...")
        print(f"Comments: {len(ticket.get('comments', []))}")
    else:
        print(f"Ticket {ticket_id} not found")


def example_conversation_flow():
    """Example 4: Multi-turn conversation"""
    print("\n" + "="*60)
    print("Example 4: Multi-turn Conversation")
    print("="*60 + "\n")
    
    # Initialize agent
    agent = CustomerSupportAgent()
    
    # Simulate a conversation
    queries = [
        "I'm having login issues",
        "What's the status of PROJ-1001?",
        "How do I reset my password?"
    ]
    
    conversation_id = None
    
    for idx, query in enumerate(queries, 1):
        print(f"\nTurn {idx}:")
        print(f"User: {query}")
        
        response = agent.process_query(query, conversation_id)
        conversation_id = response['conversation_id']
        
        print(f"Agent: {response['response'][:200]}...")
        print(f"Sources: {len(response['sources'])}")
    
    # Get conversation history
    print("\n" + "-"*60)
    print("Conversation History:")
    print("-"*60)
    history = agent.get_conversation_history(conversation_id)
    for entry in history:
        print(f"\nQ: {entry['user_query']}")
        print(f"A: {entry['agent_response'][:150]}...")


def example_custom_knowledge_base():
    """Example 5: Adding custom knowledge base articles"""
    print("\n" + "="*60)
    print("Example 5: Custom Knowledge Base")
    print("="*60 + "\n")
    
    # Initialize knowledge base
    kb = KnowledgeBase()
    
    # Add custom articles
    kb.add_article(
        title="How to Contact Support",
        content="You can contact support via email at support@example.com or call us at 1-800-SUPPORT. Our business hours are Monday-Friday, 9 AM to 5 PM EST.",
        category="support",
        tags=["contact", "support", "email", "phone"]
    )
    
    kb.add_article(
        title="Refund Policy",
        content="Refunds are available within 30 days of purchase. To request a refund, go to your account settings and click 'Request Refund'. Processing takes 5-7 business days.",
        category="billing",
        tags=["refund", "policy", "billing", "money"]
    )
    
    # Search for the new articles
    results = kb.search("refund policy", max_results=2)
    
    print("Search Results:")
    for article in results:
        print(f"\n- {article['title']}")
        print(f"  {article['content'][:100]}...")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Customer Support Agent - Example Usage")
    print("="*60)
    
    # Run examples
    example_basic_usage()
    example_knowledge_base_search()
    example_ticket_retrieval()
    example_conversation_flow()
    example_custom_knowledge_base()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60 + "\n")

