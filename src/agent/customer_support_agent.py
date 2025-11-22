"""Customer Support Agent - Main AI agent for handling customer support interactions"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime
from config.config import Config
from src.knowledge_base import KnowledgeBase
from src.ticket_system import TicketRetriever
from src.utils.text_processing import TextProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class CustomerSupportAgent:
    """
    Customer Support Agent that can:
    - Retrieve ticket details from system of record (Jira-like)
    - Search knowledge base for relevant information
    - Address customer concerns using AI
    """
    
    def __init__(self, 
                 knowledge_base: Optional[KnowledgeBase] = None,
                 ticket_retriever: Optional[TicketRetriever] = None):
        """
        Initialize Customer Support Agent
        
        Args:
            knowledge_base: KnowledgeBase instance. Creates new one if not provided
            ticket_retriever: TicketRetriever instance. Creates new one if not provided
        """
        self.knowledge_base = knowledge_base or KnowledgeBase()
        self.ticket_retriever = ticket_retriever or TicketRetriever()
        self.text_processor = TextProcessor()
        self.conversation_history: List[Dict] = []
        
        logger.info("Customer Support Agent initialized")
    
    def process_query(self, user_query: str, conversation_id: Optional[str] = None) -> Dict:
        """
        Process a customer query and generate a response
        
        Args:
            user_query: Customer's query/question
            conversation_id: Optional conversation ID for tracking
            
        Returns:
            Dictionary containing response and metadata
        """
        logger.info(f"Processing query: {user_query[:100]}...")
        
        # Extract ticket reference if present
        ticket_ref = self.text_processor.extract_ticket_reference(user_query)
        
        # Initialize response structure
        response_data = {
            "response": "",
            "ticket_details": None,
            "knowledge_base_results": [],
            "conversation_id": conversation_id or f"conv-{datetime.now().timestamp()}",
            "timestamp": datetime.now().isoformat(),
            "sources": []
        }
        
        # Step 1: Retrieve ticket details if reference provided
        ticket_details = None
        if ticket_ref:
            logger.info(f"Extracted ticket reference: {ticket_ref}")
            ticket_details = self.ticket_retriever.get_ticket(ticket_ref)
            response_data["ticket_details"] = ticket_details
            
            if ticket_details:
                response_data["sources"].append({
                    "type": "ticket",
                    "id": ticket_ref,
                    "title": ticket_details.get("title", "")
                })
            else:
                logger.warning(f"Ticket {ticket_ref} not found")
        
        # Step 2: Search knowledge base for relevant information
        knowledge_results = self.knowledge_base.search(user_query)
        response_data["knowledge_base_results"] = knowledge_results[:3]  # Top 3 results
        
        for kb_result in knowledge_results[:3]:
            response_data["sources"].append({
                "type": "knowledge_base",
                "id": kb_result.get("id", ""),
                "title": kb_result.get("title", "")
            })
        
        # Step 3: Generate comprehensive response
        response = self._generate_response(
            user_query=user_query,
            ticket_details=ticket_details,
            knowledge_results=knowledge_results
        )
        
        response_data["response"] = response
        
        # Step 4: Store conversation history
        self.conversation_history.append({
            "timestamp": response_data["timestamp"],
            "user_query": user_query,
            "agent_response": response,
            "ticket_reference": ticket_ref,
            "conversation_id": response_data["conversation_id"]
        })
        
        logger.info(f"Generated response for query")
        return response_data
    
    def _generate_response(self, 
                          user_query: str,
                          ticket_details: Optional[Dict],
                          knowledge_results: List[Dict]) -> str:
        """
        Generate response based on query, ticket details, and knowledge base results
        
        Args:
            user_query: Original user query
            ticket_details: Retrieved ticket details (if any)
            knowledge_results: Relevant knowledge base articles
            
        Returns:
            Generated response text
        """
        response_parts = []
        
        # Start with greeting if this is beginning of conversation
        if len(self.conversation_history) == 0:
            response_parts.append("Hello! I'm your customer support agent. How can I help you today?")
            response_parts.append("")
        
        # Include ticket information if available
        if ticket_details:
            response_parts.append(f"**Ticket Information:**")
            response_parts.append(f"📋 **Ticket ID:** {ticket_details.get('id', 'N/A')}")
            response_parts.append(f"📌 **Title:** {ticket_details.get('title', 'N/A')}")
            response_parts.append(f"📊 **Status:** {ticket_details.get('status', 'N/A')}")
            response_parts.append(f"⚡ **Priority:** {ticket_details.get('priority', 'N/A')}")
            
            description = ticket_details.get('description', '')
            if description:
                response_parts.append(f"\n**Description:** {description}")
            
            # Include recent comments if available
            comments = ticket_details.get('comments', [])
            if comments:
                response_parts.append(f"\n**Latest Updates:**")
                for comment in comments[-2:]:  # Last 2 comments
                    author = comment.get('author', 'N/A')
                    body = comment.get('body', '')[:200]  # Truncate long comments
                    response_parts.append(f"  - {author}: {body}")
            
            response_parts.append("")
        
        # Include relevant knowledge base information
        if knowledge_results:
            response_parts.append(f"**Relevant Information:**")
            
            for idx, kb_article in enumerate(knowledge_results[:3], 1):
                title = kb_article.get('title', 'Untitled')
                content = kb_article.get('content', '')[:300]  # Truncate long content
                category = kb_article.get('category', 'general')
                
                response_parts.append(f"\n{idx}. **{title}** ({category})")
                response_parts.append(f"   {content}")
                
                if len(content) >= 300:
                    response_parts.append("   ...")
            
            response_parts.append("")
        
        # Generate contextual response based on query and retrieved information
        contextual_response = self._create_contextual_response(
            user_query, ticket_details, knowledge_results
        )
        
        if contextual_response:
            response_parts.append(f"**Based on your query:**")
            response_parts.append(contextual_response)
        
        # If no relevant information found
        if not ticket_details and not knowledge_results:
            response_parts.append(
                "I couldn't find specific information related to your query. "
                "Could you please provide more details or a ticket reference? "
                "I'm here to help you!"
            )
        
        # Add closing statement
        response_parts.append("\n---")
        response_parts.append("Is there anything else I can help you with?")
        
        return "\n".join(response_parts)
    
    def _create_contextual_response(self,
                                   user_query: str,
                                   ticket_details: Optional[Dict],
                                   knowledge_results: List[Dict]) -> str:
        """
        Create a contextual response based on the query and retrieved information
        
        Args:
            user_query: User's query
            ticket_details: Ticket details if available
            knowledge_results: Knowledge base results
            
        Returns:
            Contextual response text
        """
        query_lower = user_query.lower()
        
        # Check for common query patterns
        if "status" in query_lower and ticket_details:
            status = ticket_details.get('status', 'Unknown')
            return f"Your ticket is currently **{status}**. "
        
        if "progress" in query_lower and ticket_details:
            status = ticket_details.get('status', 'Unknown')
            comments = ticket_details.get('comments', [])
            if comments:
                latest_comment = comments[-1].get('body', '')
                return f"Latest update on your ticket: {latest_comment[:200]}"
        
        if "resolve" in query_lower or "fix" in query_lower:
            if knowledge_results:
                top_result = knowledge_results[0]
                solution = top_result.get('content', '')[:200]
                return f"Based on our knowledge base, here's a potential solution: {solution}"
            return "I'm looking into solutions for you. Please check the relevant information above."
        
        if "error" in query_lower or "issue" in query_lower:
            if ticket_details:
                description = ticket_details.get('description', '')
                return f"I see you're experiencing an issue. Your ticket describes: {description[:200]}"
        
        # Generic helpful response
        if knowledge_results:
            return (
                "I've found some relevant information above that might help address your concern. "
                "Please review the details and let me know if you need further assistance."
            )
        
        return ""
    
    def get_conversation_history(self, conversation_id: Optional[str] = None) -> List[Dict]:
        """
        Get conversation history
        
        Args:
            conversation_id: Optional conversation ID to filter by
            
        Returns:
            List of conversation entries
        """
        if conversation_id:
            return [
                entry for entry in self.conversation_history
                if entry.get("conversation_id") == conversation_id
            ]
        return self.conversation_history.copy()
    
    def clear_conversation_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

