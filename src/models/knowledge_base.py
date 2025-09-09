"""
Knowledge Base data model for ITSM solution
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict

class ArticleType(Enum):
    SOLUTION = "Solution"
    WORKAROUND = "Workaround"
    ROOT_CAUSE = "Root Cause"
    PROCEDURE = "Procedure"

class ArticleStatus(Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"
    UNDER_REVIEW = "Under Review"

@dataclass
class KnowledgeArticle:
    """Knowledge base article for solutions and procedures"""
    
    id: str
    title: str
    content: str
    article_type: ArticleType
    status: ArticleStatus
    keywords: List[str]
    related_incidents: List[str]
    related_problems: List[str]
    created_at: datetime
    updated_at: datetime
    author: str
    category: str
    subcategory: str
    resolution_time_saved: Optional[int] = None  # minutes
    usage_count: int = 0
    effectiveness_score: float = 0.0
    auto_generated: bool = False
    
    def __post_init__(self):
        if not self.keywords:
            self.keywords = []
        if not self.related_incidents:
            self.related_incidents = []
        if not self.related_problems:
            self.related_problems = []
    
    def add_usage(self, resolution_time_saved: int = None):
        """Track article usage and effectiveness"""
        self.usage_count += 1
        if resolution_time_saved:
            self.resolution_time_saved = resolution_time_saved
            # Update effectiveness score based on usage and time saved
            self.effectiveness_score = min(1.0, (self.usage_count * 0.1) + (resolution_time_saved / 100))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "article_type": self.article_type.value,
            "status": self.status.value,
            "keywords": self.keywords,
            "related_incidents": self.related_incidents,
            "related_problems": self.related_problems,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "author": self.author,
            "category": self.category,
            "subcategory": self.subcategory,
            "resolution_time_saved": self.resolution_time_saved,
            "usage_count": self.usage_count,
            "effectiveness_score": self.effectiveness_score,
            "auto_generated": self.auto_generated
        }