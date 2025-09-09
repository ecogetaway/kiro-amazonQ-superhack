"""
Autonomous Knowledge Base Agent
Manages knowledge articles, suggests solutions, and creates new knowledge from resolved incidents
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import Counter

from ..models.knowledge_base import KnowledgeArticle, ArticleType, ArticleStatus
from ..models.incident import Incident
from ..models.problem import Problem

class AutonomousKnowledgeAgent:
    """Agent that manages knowledge base and provides intelligent suggestions"""
    
    def __init__(self):
        self.knowledge_articles = []
        self.suggestions_made = []
        self.articles_created = []
        
        # Initialize with sample knowledge base
        self._create_sample_articles()
    
    def _create_sample_articles(self):
        """Create sample knowledge articles for demo"""
        sample_articles = [
            {
                "id": "KB-001",
                "title": "Email Server Slow Response - Memory Leak Fix",
                "content": "**Problem:** Email server experiencing slow response times\n\n**Root Cause:** Memory leak in email service process\n\n**Solution:**\n1. Restart email service: `sudo systemctl restart postfix`\n2. Clear memory cache: `sudo sync && echo 3 > /proc/sys/vm/drop_caches`\n3. Monitor memory usage: `free -h`\n\n**Prevention:** Schedule weekly service restarts",
                "article_type": ArticleType.SOLUTION,
                "keywords": ["email", "slow", "memory", "postfix", "restart"],
                "category": "Email Systems",
                "related_incidents": ["INC-001", "INC-004"],
                "usage_count": 15,
                "effectiveness_score": 0.9
            },
            {
                "id": "KB-002", 
                "title": "Database Connection Timeout - Quick Workaround",
                "content": "**Problem:** Applications experiencing database connection timeouts\n\n**Immediate Workaround:**\n1. Increase connection pool size in app config\n2. Restart application servers\n3. Monitor active connections: `SHOW PROCESSLIST`\n\n**Temporary Fix:** Valid for 24-48 hours while permanent solution is implemented",
                "article_type": ArticleType.WORKAROUND,
                "keywords": ["database", "timeout", "connection", "pool"],
                "category": "Database",
                "related_incidents": ["INC-002"],
                "usage_count": 8,
                "effectiveness_score": 0.7
            },
            {
                "id": "KB-003",
                "title": "High CPU Usage - Performance Optimization",
                "content": "**Problem:** Server showing high CPU utilization\n\n**Root Cause Analysis:**\n- Check top processes: `top -c`\n- Identify resource-heavy queries\n- Review recent deployments\n\n**Solution Steps:**\n1. Kill runaway processes if identified\n2. Optimize database queries\n3. Scale horizontally if needed\n4. Implement CPU monitoring alerts",
                "article_type": ArticleType.ROOT_CAUSE,
                "keywords": ["cpu", "high", "performance", "optimization"],
                "category": "Performance",
                "related_problems": ["PRB-001"],
                "usage_count": 12,
                "effectiveness_score": 0.8
            }
        ]
        
        for article_data in sample_articles:
            article = KnowledgeArticle(
                id=article_data["id"],
                title=article_data["title"],
                content=article_data["content"],
                article_type=article_data["article_type"],
                status=ArticleStatus.PUBLISHED,
                keywords=article_data["keywords"],
                related_incidents=article_data.get("related_incidents", []),
                related_problems=article_data.get("related_problems", []),
                created_at=datetime.now() - timedelta(days=30),
                updated_at=datetime.now() - timedelta(days=5),
                author="Knowledge Agent",
                category=article_data["category"],
                subcategory="General",
                usage_count=article_data["usage_count"],
                effectiveness_score=article_data["effectiveness_score"],
                auto_generated=True
            )
            self.knowledge_articles.append(article)
    
    def search_knowledge_base(self, query: str, incident: Incident = None) -> List[Dict]:
        """Search knowledge base for relevant articles"""
        query_words = set(query.lower().split())
        
        if incident:
            # Add incident-specific terms
            incident_words = set((incident.title + " " + incident.description).lower().split())
            query_words.update(incident_words)
        
        suggestions = []
        
        for article in self.knowledge_articles:
            if article.status != ArticleStatus.PUBLISHED:
                continue
            
            # Calculate relevance score
            keyword_matches = len(set(article.keywords).intersection(query_words))
            title_matches = len(set(article.title.lower().split()).intersection(query_words))
            
            relevance_score = (keyword_matches * 0.6) + (title_matches * 0.4)
            
            if relevance_score > 0:
                suggestions.append({
                    "article": article,
                    "relevance_score": relevance_score,
                    "match_reason": f"Matched {keyword_matches} keywords, {title_matches} title words"
                })
        
        # Sort by relevance and effectiveness
        suggestions.sort(key=lambda x: (x["relevance_score"], x["article"].effectiveness_score), reverse=True)
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def suggest_articles_for_incident(self, incident: Incident) -> List[Dict]:
        """Automatically suggest knowledge articles for an incident"""
        search_query = f"{incident.title} {incident.affected_system}"
        suggestions = self.search_knowledge_base(search_query, incident)
        
        # Log suggestion for tracking
        suggestion_record = {
            "incident_id": incident.id,
            "suggestions": [s["article"].id for s in suggestions],
            "timestamp": datetime.now(),
            "auto_suggested": True
        }
        self.suggestions_made.append(suggestion_record)
        
        return suggestions
    
    def create_knowledge_from_resolution(self, incident: Incident, resolution_notes: str) -> KnowledgeArticle:
        """Automatically create knowledge article from resolved incident"""
        
        # Generate article content
        article_id = f"KB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        content = f"""**Problem:** {incident.title}

**System Affected:** {incident.affected_system}

**Description:** {incident.description}

**Resolution Steps:**
{resolution_notes}

**Category:** {incident.category if hasattr(incident, 'category') else 'General'}

**Auto-generated from incident:** {incident.id}
**Resolution Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
        
        # Extract keywords from incident
        keywords = []
        text_to_analyze = f"{incident.title} {incident.description} {resolution_notes}".lower()
        
        # Common ITSM keywords
        common_keywords = [
            "email", "database", "server", "network", "cpu", "memory", "disk",
            "slow", "timeout", "error", "failure", "restart", "connection"
        ]
        
        for keyword in common_keywords:
            if keyword in text_to_analyze:
                keywords.append(keyword)
        
        # Create new knowledge article
        article = KnowledgeArticle(
            id=article_id,
            title=f"{incident.title} - Resolution Guide",
            content=content,
            article_type=ArticleType.SOLUTION,
            status=ArticleStatus.PUBLISHED,
            keywords=keywords,
            related_incidents=[incident.id],
            related_problems=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            author="Knowledge Agent",
            category=getattr(incident, 'category', 'General'),
            subcategory=getattr(incident, 'subcategory', 'Auto-Generated'),
            auto_generated=True
        )
        
        self.knowledge_articles.append(article)
        self.articles_created.append(article)
        
        print(f"📚 Knowledge Agent: Created article {article_id} from incident {incident.id}")
        
        return article
    
    def get_knowledge_metrics(self) -> Dict:
        """Get knowledge base performance metrics"""
        total_articles = len(self.knowledge_articles)
        auto_generated = len([a for a in self.knowledge_articles if a.auto_generated])
        total_usage = sum(a.usage_count for a in self.knowledge_articles)
        avg_effectiveness = sum(a.effectiveness_score for a in self.knowledge_articles) / max(1, total_articles)
        
        return {
            "total_articles": total_articles,
            "auto_generated_articles": auto_generated,
            "suggestions_made": len(self.suggestions_made),
            "total_usage_count": total_usage,
            "average_effectiveness": avg_effectiveness,
            "articles_created_today": len([a for a in self.articles_created 
                                         if a.created_at.date() == datetime.now().date()])
        }
    
    def get_top_articles(self, limit: int = 5) -> List[KnowledgeArticle]:
        """Get most effective knowledge articles"""
        published_articles = [a for a in self.knowledge_articles if a.status == ArticleStatus.PUBLISHED]
        return sorted(published_articles, key=lambda x: x.effectiveness_score, reverse=True)[:limit]