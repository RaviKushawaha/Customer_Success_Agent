"""Knowledge Base implementation for searching customer support information"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from config.config import Config
from src.utils.text_processing import TextProcessor
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class KnowledgeBase:
    """Knowledge Base for storing and retrieving customer support information"""
    
    def __init__(self, base_path: Optional[str] = None):
        """
        Initialize Knowledge Base
        
        Args:
            base_path: Path to knowledge base directory. Defaults to Config.KNOWLEDGE_BASE_PATH
        """
        self.base_path = Path(base_path or Config.KNOWLEDGE_BASE_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.text_processor = TextProcessor()
        self._articles: List[Dict] = []
        self._load_articles()
        logger.info(f"Knowledge Base initialized with {len(self._articles)} articles")
    
    def _load_articles(self) -> None:
        """Load all articles from knowledge base directory"""
        self._articles = []
        
        # Load JSON files from knowledge base directory
        for json_file in self.base_path.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                    if isinstance(articles, list):
                        self._articles.extend(articles)
                    elif isinstance(articles, dict):
                        self._articles.append(articles)
                logger.debug(f"Loaded articles from {json_file}")
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")
    
    def add_article(self, title: str, content: str, category: str = "general", 
                   tags: List[str] = None) -> None:
        """
        Add a new article to the knowledge base
        
        Args:
            title: Article title
            content: Article content
            category: Article category
            tags: List of tags for the article
        """
        article = {
            "id": f"KB-{len(self._articles) + 1}",
            "title": title,
            "content": content,
            "category": category,
            "tags": tags or [],
            "keywords": self.text_processor.extract_keywords(f"{title} {content}")
        }
        self._articles.append(article)
        logger.info(f"Added new article: {title}")
    
    def search(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Search the knowledge base for relevant articles
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of relevant articles sorted by relevance
        """
        if not query:
            return []
        
        max_results = max_results or Config.MAX_SEARCH_RESULTS
        query_lower = query.lower()
        query_keywords = set(self.text_processor.extract_keywords(query))
        
        results = []
        
        for article in self._articles:
            score = 0.0
            
            # Exact title match
            if query_lower in article.get("title", "").lower():
                score += 10.0
            
            # Content similarity
            content_sim = self.text_processor.calculate_similarity(
                query, f"{article.get('title', '')} {article.get('content', '')}"
            )
            score += content_sim * 5.0
            
            # Keyword matching
            article_keywords = set(article.get("keywords", []))
            if query_keywords and article_keywords:
                keyword_overlap = len(query_keywords.intersection(article_keywords))
                keyword_score = keyword_overlap / max(len(query_keywords), 1)
                score += keyword_score * 3.0
            
            # Tag matching
            article_tags = [tag.lower() for tag in article.get("tags", [])]
            if query_lower in " ".join(article_tags):
                score += 2.0
            
            # Category matching
            if query_lower in article.get("category", "").lower():
                score += 1.0
            
            if score > 0:
                article_copy = article.copy()
                article_copy["relevance_score"] = score
                results.append(article_copy)
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        # Filter by threshold
        threshold = Config.SIMILARITY_THRESHOLD
        filtered_results = [
            r for r in results 
            if r.get("relevance_score", 0) >= threshold
        ]
        
        logger.info(f"Knowledge base search for '{query}' returned {len(filtered_results)} results")
        return filtered_results[:max_results]
    
    def get_article_by_id(self, article_id: str) -> Optional[Dict]:
        """
        Get a specific article by ID
        
        Args:
            article_id: Article ID
            
        Returns:
            Article dictionary or None if not found
        """
        for article in self._articles:
            if article.get("id") == article_id:
                return article
        return None
    
    def get_all_articles(self) -> List[Dict]:
        """
        Get all articles in the knowledge base
        
        Returns:
            List of all articles
        """
        return self._articles.copy()
    
    def save_articles(self, filename: str = "knowledge_base.json") -> None:
        """
        Save articles to a JSON file
        
        Args:
            filename: Name of the file to save to
        """
        filepath = self.base_path / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self._articles, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved {len(self._articles)} articles to {filepath}")

