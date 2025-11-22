"""Text processing utilities"""

import re
from typing import List, Dict
from collections import Counter


class TextProcessor:
    """Utility class for text processing operations"""
    
    @staticmethod
    def extract_ticket_reference(text: str) -> str:
        """
        Extract ticket reference from text
        
        Args:
            text: Input text that may contain ticket reference
            
        Returns:
            Extracted ticket reference or empty string
        """
        # Patterns for common ticket formats: PROJ-123, TICKET-456, #789, etc.
        patterns = [
            r'[A-Z]+-\d+',  # JIRA style: PROJ-123
            r'#[A-Z]+-\d+',  # With hash: #PROJ-123
            r'TICKET-\d+',  # TICKET-456
            r'#\d+',  # Simple number: #789
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Remove hash if present
                ticket_ref = match.group(0).replace('#', '')
                return ticket_ref.upper()
        
        return ""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def extract_keywords(text: str, min_length: int = 3) -> List[str]:
        """
        Extract keywords from text
        
        Args:
            text: Input text
            min_length: Minimum keyword length
            
        Returns:
            List of keywords
        """
        # Remove special characters and split
        words = re.findall(r'\b\w+\b', text.lower())
        # Filter by length and common stop words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 
                     'was', 'were', 'been', 'be', 'have', 'has', 'had', 'do', 
                     'does', 'did', 'will', 'would', 'should', 'could', 'may', 
                     'might', 'must', 'can', 'this', 'that', 'these', 'those'}
        
        keywords = [w for w in words if len(w) >= min_length and w not in stop_words]
        # Return unique keywords sorted by frequency
        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common()]
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate simple word-based similarity between two texts
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score between 0 and 1
        """
        words1 = set(TextProcessor.extract_keywords(text1))
        words2 = set(TextProcessor.extract_keywords(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    @staticmethod
    def format_response(response: str, max_length: int = 500) -> str:
        """
        Format response text
        
        Args:
            response: Raw response text
            max_length: Maximum length before truncation
            
        Returns:
            Formatted response
        """
        response = TextProcessor.clean_text(response)
        
        if len(response) > max_length:
            response = response[:max_length] + "..."
        
        return response

