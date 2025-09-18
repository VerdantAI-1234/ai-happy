"""
Data models for the AI Happy reasoning engine.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class EventType(str, Enum):
    """Types of events that can be processed by the reasoning engine."""
    OBJECT_DETECTION = "object_detection"
    MOTION_DETECTION = "motion_detection"
    FACIAL_RECOGNITION = "facial_recognition"
    ANOMALY_DETECTION = "anomaly_detection"
    CUSTOM = "custom"


class EventData(BaseModel):
    """
    Input event data from hardware/object detection systems.
    """
    event_id: str = Field(..., description="Unique identifier for the event")
    event_type: EventType = Field(..., description="Type of event detected")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the event occurred")
    
    # Object detection data
    detected_objects: List[Dict[str, Any]] = Field(default_factory=list, description="List of detected objects with confidence scores")
    image_metadata: Optional[Dict[str, Any]] = Field(default=None, description="Image metadata if applicable")
    
    # Sensor data
    sensor_data: Dict[str, Any] = Field(default_factory=dict, description="Additional sensor readings")
    location: Optional[Dict[str, float]] = Field(default=None, description="Location coordinates if available")
    
    # Context
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional contextual information")
    brand_config: Optional[Dict[str, Any]] = Field(default=None, description="Brand-specific configuration")


class SymbolicFeature(BaseModel):
    """
    Symbolic human features extracted from events.
    """
    feature_name: str = Field(..., description="Name of the symbolic feature")
    feature_value: Any = Field(..., description="Value of the feature")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in the feature extraction")
    human_description: str = Field(..., description="Human-readable description of the feature")


class ReasoningStep(BaseModel):
    """
    Individual step in the reasoning process.
    """
    step_id: int = Field(..., description="Sequential step identifier")
    operation: str = Field(..., description="Type of reasoning operation performed")
    input_data: Dict[str, Any] = Field(..., description="Input data for this step")
    output_data: Dict[str, Any] = Field(..., description="Output data from this step")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence in this reasoning step")
    explanation: str = Field(..., description="Human-readable explanation of this step")


class ReasoningResult(BaseModel):
    """
    Complete reasoning result with human explanation.
    """
    event_id: str = Field(..., description="Original event ID")
    processed_at: datetime = Field(default_factory=datetime.now, description="When processing was completed")
    
    # Extracted features
    symbolic_features: List[SymbolicFeature] = Field(default_factory=list, description="Extracted symbolic features")
    
    # Reasoning process
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list, description="Step-by-step reasoning process")
    
    # Final interpretation
    meaning: str = Field(..., description="High-level meaning of the event")
    human_explanation: str = Field(..., description="Detailed human-readable explanation")
    significance_score: float = Field(..., ge=0.0, le=1.0, description="Overall significance of the event")
    
    # Recommendations
    recommended_actions: List[str] = Field(default_factory=list, description="Recommended actions based on the analysis")
    
    # Metadata
    processing_time_ms: Optional[float] = Field(default=None, description="Time taken to process in milliseconds")
    model_version: str = Field(default="1.0.0", description="Version of the reasoning model used")


class LicenseConfig(BaseModel):
    """
    Configuration for brand licensing and customization.
    """
    brand_name: str = Field(..., description="Name of the licensed brand")
    license_key: str = Field(..., description="License key for authentication")
    
    # Customization options
    custom_vocabulary: Dict[str, str] = Field(default_factory=dict, description="Brand-specific terminology")
    explanation_style: str = Field(default="professional", description="Style of explanations (professional, casual, technical)")
    focus_areas: List[str] = Field(default_factory=list, description="Areas of focus for reasoning")
    
    # API limits
    daily_request_limit: Optional[int] = Field(default=None, description="Daily API request limit")
    rate_limit_per_minute: Optional[int] = Field(default=None, description="Rate limit per minute")
    
    # Features
    enabled_features: List[str] = Field(default_factory=list, description="List of enabled features")
    custom_models: Dict[str, str] = Field(default_factory=dict, description="Custom model configurations")


class HealthStatus(BaseModel):
    """
    Health status of the reasoning engine.
    """
    status: str = Field(..., description="Overall status (healthy, degraded, unhealthy)")
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0.0")
    uptime_seconds: float = Field(..., description="Uptime in seconds")
    
    # Performance metrics
    average_response_time_ms: float = Field(..., description="Average response time in milliseconds")
    requests_processed: int = Field(..., description="Total requests processed")
    error_rate: float = Field(..., ge=0.0, le=1.0, description="Error rate as a percentage")
    
    # Resource usage
    memory_usage_mb: float = Field(..., description="Memory usage in MB")
    cpu_usage_percent: float = Field(..., ge=0.0, le=100.0, description="CPU usage percentage")