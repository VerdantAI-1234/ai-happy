#!/usr/bin/env python3
"""
Main entry point for the AI Happy reasoning engine server.
"""

import logging
import uvicorn
from ai_happy.api import create_app
from ai_happy.config import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.get("log_level", "INFO")),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point."""
    # Create the application with default license
    license_config = config.get_default_license()
    app = create_app(license_config)
    
    # Get server configuration
    host = config.get("api_host", "0.0.0.0")
    port = config.get("api_port", 8000)
    
    logger.info(f"Starting AI Happy reasoning engine on {host}:{port}")
    logger.info(f"License configured for brand: {license_config.brand_name}")
    
    # Run the server
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        log_level=config.get("log_level", "info").lower()
    )

if __name__ == "__main__":
    main()