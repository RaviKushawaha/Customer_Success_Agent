"""Configuration management for the Customer Support Agent"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for application settings"""
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    
    # Ticket System Configuration (Jira-like)
    TICKET_SYSTEM_URL: str = os.getenv("TICKET_SYSTEM_URL", "https://api.jira.com")
    TICKET_SYSTEM_USERNAME: Optional[str] = os.getenv("TICKET_SYSTEM_USERNAME")
    TICKET_SYSTEM_API_TOKEN: Optional[str] = os.getenv("TICKET_SYSTEM_API_TOKEN")
    
    # Knowledge Base Configuration
    KNOWLEDGE_BASE_PATH: str = os.getenv("KNOWLEDGE_BASE_PATH", "data/knowledge_base")
    
    # Agent Configuration
    AGENT_TEMPERATURE: float = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
    AGENT_MODEL: str = os.getenv("AGENT_MODEL", "gpt-3.5-turbo")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/customer_support_agent.log")
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))

