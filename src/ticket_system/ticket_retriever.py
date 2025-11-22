"""Ticket Retriever for fetching ticket details from Jira-like systems"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime
import requests
from config.config import Config
from src.utils.logger import setup_logger
from src.utils.text_processing import TextProcessor

logger = setup_logger(__name__)


class TicketRetriever:
    """Retriever for fetching ticket details from system of record (Jira-like)"""
    
    def __init__(self, api_url: Optional[str] = None, 
                 username: Optional[str] = None,
                 api_token: Optional[str] = None):
        """
        Initialize Ticket Retriever
        
        Args:
            api_url: Base URL of the ticket system API
            username: Username for authentication
            api_token: API token for authentication
        """
        self.api_url = api_url or Config.TICKET_SYSTEM_URL
        self.username = username or Config.TICKET_SYSTEM_USERNAME
        self.api_token = api_token or Config.TICKET_SYSTEM_API_TOKEN
        self.text_processor = TextProcessor()
        
        # For demo purposes, we'll use a local file-based ticket system
        # In production, this would connect to actual Jira API
        self.tickets_file = Path("data/tickets.json")
        self._initialize_local_tickets()
        
        logger.info(f"Ticket Retriever initialized for {self.api_url}")
    
    def _initialize_local_tickets(self) -> None:
        """Initialize local ticket storage for demo purposes"""
        self.tickets_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.tickets_file.exists():
            sample_tickets = [
                {
                    "id": "PROJ-1001",
                    "title": "Unable to login to application",
                    "description": "User is experiencing login issues with error message 'Invalid credentials'",
                    "status": "Open",
                    "priority": "High",
                    "assignee": "support-team",
                    "reporter": "customer@example.com",
                    "created_date": "2024-01-15T10:30:00Z",
                    "updated_date": "2024-01-15T14:20:00Z",
                    "comments": [
                        {
                            "author": "support-team",
                            "body": "Please check if you're using the correct password",
                            "created_date": "2024-01-15T11:00:00Z"
                        }
                    ]
                },
                {
                    "id": "PROJ-1002",
                    "title": "Feature request: Add dark mode",
                    "description": "Customer requests dark mode theme for better visibility",
                    "status": "In Progress",
                    "priority": "Medium",
                    "assignee": "dev-team",
                    "reporter": "user@example.com",
                    "created_date": "2024-01-14T09:15:00Z",
                    "updated_date": "2024-01-16T08:45:00Z",
                    "comments": [
                        {
                            "author": "dev-team",
                            "body": "Dark mode is planned for Q2 release",
                            "created_date": "2024-01-14T16:30:00Z"
                        }
                    ]
                },
                {
                    "id": "PROJ-1003",
                    "title": "Payment processing error",
                    "description": "Transaction failed with error code 500. Customer unable to complete purchase.",
                    "status": "Resolved",
                    "priority": "Critical",
                    "assignee": "payment-team",
                    "reporter": "merchant@example.com",
                    "created_date": "2024-01-13T15:20:00Z",
                    "updated_date": "2024-01-14T10:10:00Z",
                    "comments": [
                        {
                            "author": "payment-team",
                            "body": "Issue resolved. Was a temporary service outage.",
                            "created_date": "2024-01-14T10:10:00Z"
                        }
                    ]
                }
            ]
            with open(self.tickets_file, 'w', encoding='utf-8') as f:
                json.dump(sample_tickets, f, indent=2)
            logger.info(f"Initialized local tickets file with {len(sample_tickets)} sample tickets")
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """
        Retrieve ticket details by ticket ID
        
        Args:
            ticket_id: Ticket ID (e.g., "PROJ-1001")
            
        Returns:
            Ticket dictionary or None if not found
        """
        # Clean ticket ID
        ticket_id = self.text_processor.clean_text(ticket_id).upper()
        
        # Try to fetch from local storage first (for demo)
        ticket = self._get_ticket_from_local(ticket_id)
        
        if ticket:
            logger.info(f"Retrieved ticket {ticket_id} from local storage")
            return ticket
        
        # In production, fetch from actual API
        ticket = self._fetch_ticket_from_api(ticket_id)
        
        if ticket:
            logger.info(f"Retrieved ticket {ticket_id} from API")
            return ticket
        
        logger.warning(f"Ticket {ticket_id} not found")
        return None
    
    def _get_ticket_from_local(self, ticket_id: str) -> Optional[Dict]:
        """Get ticket from local JSON file"""
        try:
            if self.tickets_file.exists():
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    tickets = json.load(f)
                    for ticket in tickets:
                        if ticket.get("id", "").upper() == ticket_id:
                            return ticket
        except Exception as e:
            logger.error(f"Error reading local tickets: {e}")
        return None
    
    def _fetch_ticket_from_api(self, ticket_id: str) -> Optional[Dict]:
        """
        Fetch ticket from actual API (Jira-like system)
        
        Args:
            ticket_id: Ticket ID
            
        Returns:
            Ticket dictionary or None
        """
        if not self.username or not self.api_token:
            logger.warning("API credentials not configured. Using local tickets only.")
            return None
        
        try:
            # Construct API endpoint
            url = f"{self.api_url}/rest/api/2/issue/{ticket_id}"
            
            # Make authenticated request
            response = requests.get(
                url,
                auth=(self.username, self.api_token),
                headers={"Accept": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # Transform Jira API response to our format
                return self._transform_jira_response(data)
            else:
                logger.error(f"API request failed with status {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching ticket from API: {e}")
            return None
    
    def _transform_jira_response(self, jira_data: Dict) -> Dict:
        """
        Transform Jira API response to our ticket format
        
        Args:
            jira_data: Raw Jira API response
            
        Returns:
            Transformed ticket dictionary
        """
        fields = jira_data.get("fields", {})
        return {
            "id": jira_data.get("key", ""),
            "title": fields.get("summary", ""),
            "description": fields.get("description", ""),
            "status": fields.get("status", {}).get("name", ""),
            "priority": fields.get("priority", {}).get("name", ""),
            "assignee": fields.get("assignee", {}).get("displayName", ""),
            "reporter": fields.get("reporter", {}).get("displayName", ""),
            "created_date": fields.get("created", ""),
            "updated_date": fields.get("updated", ""),
            "comments": [
                {
                    "author": comment.get("author", {}).get("displayName", ""),
                    "body": comment.get("body", ""),
                    "created_date": comment.get("created", "")
                }
                for comment in fields.get("comment", {}).get("comments", [])
            ]
        }
    
    def search_tickets(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        Search tickets by query
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            List of matching tickets
        """
        query_lower = query.lower()
        matching_tickets = []
        
        try:
            if self.tickets_file.exists():
                with open(self.tickets_file, 'r', encoding='utf-8') as f:
                    tickets = json.load(f)
                    
                    for ticket in tickets:
                        score = 0.0
                        title = ticket.get("title", "").lower()
                        description = ticket.get("description", "").lower()
                        ticket_id = ticket.get("id", "").lower()
                        
                        # Check if query matches ticket ID
                        if query_lower in ticket_id:
                            score += 10.0
                        
                        # Check title match
                        if query_lower in title:
                            score += 5.0
                        
                        # Check description match
                        if query_lower in description:
                            score += 2.0
                        
                        # Calculate similarity
                        text_content = f"{title} {description}"
                        similarity = self.text_processor.calculate_similarity(query, text_content)
                        score += similarity * 3.0
                        
                        if score > 0:
                            ticket_copy = ticket.copy()
                            ticket_copy["match_score"] = score
                            matching_tickets.append(ticket_copy)
                    
                    # Sort by score
                    matching_tickets.sort(key=lambda x: x.get("match_score", 0), reverse=True)
                    logger.info(f"Ticket search for '{query}' returned {len(matching_tickets)} results")
                    return matching_tickets[:max_results]
        
        except Exception as e:
            logger.error(f"Error searching tickets: {e}")
        
        return []

