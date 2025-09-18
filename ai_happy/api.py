"""
FastAPI application for the AI Happy reasoning engine.

Provides REST API endpoints for event processing and licensing.
"""

import time
import psutil
import logging
from typing import Optional
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .models import EventData, ReasoningResult, LicenseConfig, HealthStatus
from .engine import DeepReasonEngine

logger = logging.getLogger(__name__)

# Global variables for application state
engine: Optional[DeepReasonEngine] = None
license_config: Optional[LicenseConfig] = None
app_start_time: Optional[datetime] = None
request_count = 0
total_response_time = 0.0
error_count = 0

# Security
security = HTTPBearer()


async def verify_license(credentials: HTTPAuthorizationCredentials = Depends(security)) -> LicenseConfig:
    """Verify license key and return license configuration."""
    global license_config
    
    if not license_config:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No license configuration available"
        )
    
    if credentials.credentials != license_config.license_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid license key"
        )
    
    return license_config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global engine, app_start_time
    
    # Startup
    app_start_time = datetime.now()
    
    # Initialize with default configuration
    default_license = LicenseConfig(
        brand_name="Demo",
        license_key="demo-key-12345",
        explanation_style="professional",
        daily_request_limit=1000,
        rate_limit_per_minute=60,
        enabled_features=["object_detection", "reasoning", "explanations"]
    )
    
    engine = DeepReasonEngine(default_license)
    logger.info("AI Happy reasoning engine started")
    
    yield
    
    # Shutdown
    logger.info("AI Happy reasoning engine shutting down")


def create_app(license_cfg: Optional[LicenseConfig] = None) -> FastAPI:
    """Create and configure the FastAPI application."""
    global license_config
    
    if license_cfg:
        license_config = license_cfg
    
    app = FastAPI(
        title="AI Happy - Deep Reason Metacognition Engine",
        description="Embeddable AI reasoning engine for hardware and object detection systems",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS middleware for cross-origin requests
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.middleware("http")
    async def track_requests(request, call_next):
        """Middleware to track request metrics."""
        global request_count, total_response_time, error_count
        
        start_time = time.time()
        request_count += 1
        
        try:
            response = await call_next(request)
            processing_time = time.time() - start_time
            total_response_time += processing_time
            return response
        except Exception as e:
            error_count += 1
            processing_time = time.time() - start_time
            total_response_time += processing_time
            raise
    
    @app.get("/", response_model=dict)
    async def root():
        """Root endpoint with basic information."""
        return {
            "name": "AI Happy - Deep Reason Metacognition Engine",
            "version": "1.0.0",
            "description": "Embeddable AI reasoning engine for hardware and object detection systems",
            "status": "operational",
            "endpoints": {
                "health": "/health",
                "process_event": "/api/v1/process",
                "configure_license": "/api/v1/license"
            }
        }
    
    @app.get("/health", response_model=HealthStatus)
    async def health_check():
        """Health check endpoint."""
        global app_start_time, request_count, total_response_time, error_count
        
        if not app_start_time:
            app_start_time = datetime.now()
        
        uptime = (datetime.now() - app_start_time).total_seconds()
        avg_response_time = (total_response_time / request_count * 1000) if request_count > 0 else 0.0
        error_rate = (error_count / request_count) if request_count > 0 else 0.0
        
        # Get system metrics
        memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # MB
        cpu_usage = psutil.cpu_percent(interval=1)
        
        status = "healthy"
        if error_rate > 0.1:  # 10% error rate
            status = "degraded"
        if error_rate > 0.25 or cpu_usage > 90:  # 25% error rate or 90% CPU
            status = "unhealthy"
        
        return HealthStatus(
            status=status,
            timestamp=datetime.now(),
            version="1.0.0",
            uptime_seconds=uptime,
            average_response_time_ms=avg_response_time,
            requests_processed=request_count,
            error_rate=error_rate,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage
        )
    
    @app.post("/api/v1/process", response_model=ReasoningResult)
    async def process_event(
        event_data: EventData,
        license_cfg: LicenseConfig = Depends(verify_license)
    ):
        """
        Process an event through the reasoning engine.
        
        This is the main endpoint that hardware and object detection systems
        will use to send event data for analysis.
        """
        global engine
        
        if not engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Reasoning engine not initialized"
            )
        
        try:
            # Check rate limits
            if license_cfg.rate_limit_per_minute:
                # In production, implement proper rate limiting with Redis or similar
                pass
            
            # Process the event
            result = engine.process_event(event_data)
            
            logger.info(f"Processed event {event_data.event_id} for brand {license_cfg.brand_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing event {event_data.event_id}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing event: {str(e)}"
            )
    
    @app.post("/api/v1/license")
    async def configure_license(new_license: LicenseConfig):
        """
        Configure or update license settings.
        
        This endpoint allows brands to update their licensing configuration.
        In production, this would require additional authentication.
        """
        global license_config, engine
        
        try:
            license_config = new_license
            
            # Reinitialize engine with new license
            engine = DeepReasonEngine(license_config)
            
            logger.info(f"License updated for brand: {new_license.brand_name}")
            
            return {
                "status": "success",
                "message": f"License configured for {new_license.brand_name}",
                "features_enabled": new_license.enabled_features
            }
            
        except Exception as e:
            logger.error(f"Error configuring license: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error configuring license: {str(e)}"
            )
    
    @app.get("/api/v1/license", response_model=dict)
    async def get_license_info(license_cfg: LicenseConfig = Depends(verify_license)):
        """Get current license information."""
        return {
            "brand_name": license_cfg.brand_name,
            "explanation_style": license_cfg.explanation_style,
            "enabled_features": license_cfg.enabled_features,
            "daily_request_limit": license_cfg.daily_request_limit,
            "rate_limit_per_minute": license_cfg.rate_limit_per_minute
        }
    
    @app.post("/api/v1/batch-process")
    async def batch_process_events(
        events: list[EventData],
        license_cfg: LicenseConfig = Depends(verify_license)
    ):
        """
        Process multiple events in batch.
        
        Useful for processing multiple events from hardware systems efficiently.
        """
        global engine
        
        if not engine:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Reasoning engine not initialized"
            )
        
        if len(events) > 100:  # Limit batch size
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Batch size cannot exceed 100 events"
            )
        
        try:
            results = []
            for event_data in events:
                result = engine.process_event(event_data)
                results.append(result)
            
            logger.info(f"Processed batch of {len(events)} events for brand {license_cfg.brand_name}")
            
            return {
                "status": "success",
                "processed_count": len(results),
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Error processing batch: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error processing batch: {str(e)}"
            )
    
    return app


# Create the default app instance
app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)