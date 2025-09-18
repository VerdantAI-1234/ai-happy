"""
Configuration management for AI Happy reasoning engine.
"""

import os
import json
from typing import Optional, Dict, Any
from .models import LicenseConfig


class Config:
    """
    Configuration manager for the AI Happy reasoning engine.
    """
    
    def __init__(self):
        self.config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables or config file."""
        config = {
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "api_host": os.getenv("API_HOST", "0.0.0.0"),
            "api_port": int(os.getenv("API_PORT", "8000")),
            "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
            "default_license": {
                "brand_name": os.getenv("DEFAULT_BRAND_NAME", "Demo"),
                "license_key": os.getenv("DEFAULT_LICENSE_KEY", "demo-key-12345"),
                "explanation_style": os.getenv("EXPLANATION_STYLE", "professional"),
                "daily_request_limit": int(os.getenv("DAILY_REQUEST_LIMIT", "1000")),
                "rate_limit_per_minute": int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
                "enabled_features": os.getenv("ENABLED_FEATURES", "object_detection,reasoning,explanations").split(",")
            }
        }
        
        # Load from config file if exists
        config_file = os.getenv("AI_HAPPY_CONFIG", "config.json")
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    config.update(file_config)
            except Exception as e:
                print(f"Warning: Could not load config file {config_file}: {e}")
        
        return config
    
    def get_default_license(self) -> LicenseConfig:
        """Get default license configuration."""
        license_data = self.config_data["default_license"]
        return LicenseConfig(
            brand_name=license_data["brand_name"],
            license_key=license_data["license_key"],
            explanation_style=license_data["explanation_style"],
            daily_request_limit=license_data["daily_request_limit"],
            rate_limit_per_minute=license_data["rate_limit_per_minute"],
            enabled_features=license_data["enabled_features"],
            custom_vocabulary={},
            focus_areas=[],
            custom_models={}
        )
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config_data.get(key, default)


# Global config instance
config = Config()