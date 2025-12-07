"""
Main entry point for Customer Support Agent
Example usage and demo script
"""

import time
import sys

from src.agent import CustomerSupportAgent
from src.knowledge_base import KnowledgeBase
from src.ticket_system import TicketRetriever
from src.utils.logger import setup_logger

logger = setup_logger("Main")


def type_text(text: str, delay: float = 0.03) -> None:
    """Print text with a typing effect"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # New line after typing


def initialize_sample_knowledge_base(kb: KnowledgeBase) -> None:
    """Initialize knowledge base with sample articles"""
    
    articles = [
        {
            "id": "KB-1",
            "title": "How to Reset Your Password",
            "content": "To reset your password, go to the login page and click 'Forgot Password'. Enter your email address and check your inbox for a password reset link. Click the link and follow the instructions to create a new password.",
            "category": "authentication",
            "tags": ["password", "login", "reset", "authentication"],
            "keywords": ["password", "reset", "login", "forgot", "email", "authentication"]
        },
        {
            "id": "KB-2",
            "title": "Troubleshooting Login Issues",
            "content": "If you're experiencing login issues, first check that you're using the correct username and password. Clear your browser cache and cookies, then try again. If the problem persists, ensure your account is not locked. Contact support if issues continue.",
            "category": "authentication",
            "tags": ["login", "troubleshooting", "error", "authentication"],
            "keywords": ["login", "issue", "error", "troubleshoot", "password", "username", "cache", "cookies"]
        },
        {
            "id": "KB-3",
            "title": "Payment Processing Guide",
            "content": "To process a payment, select the payment method and enter your card details. Ensure all information is correct before submitting. For failed transactions, check your card details and account balance. Contact your bank if issues persist.",
            "category": "payments",
            "tags": ["payment", "transaction", "card", "billing"],
            "keywords": ["payment", "transaction", "card", "billing", "failed", "balance", "bank"]
        },
        {
            "id": "KB-4",
            "title": "Understanding Error Code 500",
            "content": "Error code 500 indicates an internal server error. This is typically a temporary issue on our end. Please wait a few minutes and try again. If the error persists, it may indicate a service outage. Check our status page for updates.",
            "category": "errors",
            "tags": ["error", "500", "server", "troubleshooting"],
            "keywords": ["error", "500", "server", "internal", "outage", "temporary", "status"]
        },
        {
            "id": "KB-5",
            "title": "Account Activation Process",
            "content": "After creating an account, check your email for an activation link. Click the link to activate your account. If you don't receive the email, check your spam folder. You can request a new activation link from the login page.",
            "category": "account",
            "tags": ["account", "activation", "email", "registration"],
            "keywords": ["account", "activation", "email", "link", "spam", "register", "create"]
        }
    ]
    
    # Add articles to knowledge base
    for article in articles:
        kb.add_article(
            title=article["title"],
            content=article["content"],
            category=article["category"],
            tags=article["tags"]
        )
    
    logger.info(f"Initialized knowledge base with {len(articles)} sample articles")


def interactive_chat() -> None:
    """Run interactive chat session with the customer support agent"""
    
    print("\n" + "="*60)
    print("Welcome to Customer Support Agent")
    print("="*60)
    print("\nYou can:")
    print("  - Ask questions about issues")
    print("  - Reference tickets (e.g., 'What's the status of PROJ-1001?')")
    print("  - Type 'exit' to quit")
    print("  - Type 'history' to see conversation history")
    print("\n" + "-"*60 + "\n")
    
    # Initialize agent
    kb = KnowledgeBase()
    initialize_sample_knowledge_base(kb)
    ticket_retriever = TicketRetriever()
    agent = CustomerSupportAgent(knowledge_base=kb, ticket_retriever=ticket_retriever)
    
    conversation_id = None
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nThank you for using Customer Support Agent. Goodbye!")
                break
            
            if user_input.lower() == 'history':
                history = agent.get_conversation_history(conversation_id)
                if history:
                    print("\n--- Conversation History ---")
                    for entry in history:
                        print(f"\n[You]: {entry['user_query']}")
                        print(f"[Agent]: {entry['agent_response'][:200]}...")
                    print("--- End History ---\n")
                else:
                    print("No conversation history available.\n")
                continue
            
            # Process query
            response_data = agent.process_query(user_input, conversation_id)
            conversation_id = response_data["conversation_id"]
            
            # Display response
            print(f"\nAgent:\n{response_data['response']}\n")
            print("-"*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error in interactive chat: {e}")
            print(f"\nSorry, an error occurred: {e}\n")


def demo_queries() -> None:
    """Run demo queries to showcase the agent's capabilities"""
    
    print("\n" + "="*60)
    type_text("Customer Support Agent - Demo Mode", delay=0.05)
    print("="*60 + "\n")
    time.sleep(0.5)
    
    # Initialize agent
    type_text("Initializing agent...", delay=0.05)
    time.sleep(0.8)
    kb = KnowledgeBase()
    initialize_sample_knowledge_base(kb)
    ticket_retriever = TicketRetriever()
    agent = CustomerSupportAgent(knowledge_base=kb, ticket_retriever=ticket_retriever)
    type_text("Agent ready!\n", delay=0.05)
    time.sleep(0.5)
    
    # Demo queries
    demo_queries_list = [
        "What's the status of ticket PROJ-1001?",
        "I'm having login issues. Can you help?",
        "Tell me about PROJ-1002",
        "I got an error code 500. What should I do?",
        "How do I reset my password?",
    ]
    
    for idx, query in enumerate(demo_queries_list, 1):
        print(f"\n{'='*60}")
        type_text(f"Demo Query {idx}: {query}", delay=0.03)
        print('='*60)
        time.sleep(0.8)
        
        type_text("\nProcessing query...", delay=0.05)
        time.sleep(1.0)
        
        response_data = agent.process_query(query)
        
        type_text("\nResponse:", delay=0.05)
        time.sleep(0.3)
        type_text(response_data['response'], delay=0.02)
        
        time.sleep(0.5)
        type_text(f"\nSources found: {len(response_data['sources'])}", delay=0.05)
        time.sleep(0.3)
        for source in response_data['sources']:
            source_text = f"  - {source['type']}: {source.get('title', source.get('id', ''))}"
            type_text(source_text, delay=0.03)
        
        print("\n" + "-"*60)
        time.sleep(1.2)
    
    time.sleep(0.5)
    type_text("\nDemo completed!\n", delay=0.05)


def main():
    """Main entry point"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_queries()
    else:
        interactive_chat()


if __name__ == "__main__":
    main()

