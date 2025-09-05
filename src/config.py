"""
Configuration management for AI-powered ITSM solution
Handles API keys, settings, and environment variables
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Configuration settings for the ITSM solution"""
    
    # API Keys
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"
    
    # Agent Settings
    correlation_threshold: float = 0.7
    anomaly_threshold: float = 2.0
    problem_pattern_threshold: int = 3
    
    # Demo Settings
    demo_mode: bool = True
    response_delay: float = 1.0  # Simulate thinking time
    
    def __post_init__(self):
        """Load configuration from environment variables"""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")

# Global configuration instance
config = Config()