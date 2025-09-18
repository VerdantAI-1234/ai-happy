# AI Happy - Deep Reason Metacognition Engine

**A licensing-ready AI reasoning engine that can be embedded behind hardware and object detection systems to provide meaningful event interpretation and human-readable explanations.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

AI Happy is a Deep Reason reasoning metacognition engine designed for commercial licensing to brands. It provides a sophisticated AI layer that can be embedded behind hardware and object detection systems, transforming raw event data into meaningful insights with human-readable explanations.

### Key Features

- **🧠 Symbolic Reasoning**: Extracts symbolic human features from event data
- **🔍 Metacognitive Processing**: Multi-step reasoning process with explainable AI
- **📝 Human Explanations**: Generates detailed, natural language explanations
- **🏢 Brand Licensing**: Configurable for multiple brands with customization options
- **🔌 API-First Design**: RESTful API for easy hardware integration
- **⚡ Real-time Processing**: Fast event processing suitable for real-time systems
- **📊 Batch Processing**: Efficient handling of multiple events
- **🛡️ Secure & Scalable**: Built with enterprise requirements in mind

## Use Cases

- **Security Systems**: Intelligent video surveillance with contextual understanding
- **Retail Analytics**: Customer behavior analysis and insights
- **Smart Buildings**: Automated facility management with reasoning
- **IoT Devices**: Enhanced object detection with meaningful interpretation
- **Autonomous Systems**: Decision support with explainable reasoning

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/VerdantAI-1234/ai-happy.git
cd ai-happy

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

#### 1. Direct Library Usage

```python
from ai_happy import DeepReasonEngine, EventData, LicenseConfig
from ai_happy.models import EventType
from datetime import datetime

# Configure your brand license
license_config = LicenseConfig(
    brand_name="Your Brand",
    license_key="your-license-key",
    explanation_style="professional",
    enabled_features=["object_detection", "reasoning", "explanations"]
)

# Initialize the reasoning engine
engine = DeepReasonEngine(license_config)

# Create event data (from your object detection system)
event_data = EventData(
    event_id="event_001",
    event_type=EventType.OBJECT_DETECTION,
    detected_objects=[
        {"name": "person", "confidence": 0.92},
        {"name": "car", "confidence": 0.87}
    ],
    sensor_data={"motion": True, "light_level": 0.8},
    context={"camera_id": "entrance_cam"}
)

# Process the event
result = engine.process_event(event_data)

# Get human-readable results
print(f"Meaning: {result.meaning}")
print(f"Explanation: {result.human_explanation}")
print(f"Significance: {result.significance_score}")
```

#### 2. API Server Usage

```bash
# Start the API server
python main.py

# The server will start on http://localhost:8000
```

```python
import httpx

# Send event to API
event_data = {
    "event_id": "api_event_001",
    "event_type": "object_detection",
    "detected_objects": [{"name": "person", "confidence": 0.9}],
    "sensor_data": {"motion": True}
}

headers = {"Authorization": "Bearer your-license-key"}

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/process",
        json=event_data,
        headers=headers
    )
    result = response.json()
    print(result["human_explanation"])
```

## API Documentation

### Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check and system metrics
- `POST /api/v1/process` - Process single event
- `POST /api/v1/batch-process` - Process multiple events
- `POST /api/v1/license` - Configure license settings
- `GET /api/v1/license` - Get current license information

### Authentication

All API endpoints require a valid license key in the Authorization header:

```
Authorization: Bearer your-license-key
```

### Event Data Format

```json
{
  "event_id": "unique_event_identifier",
  "event_type": "object_detection",
  "timestamp": "2024-01-01T12:00:00Z",
  "detected_objects": [
    {
      "name": "person",
      "confidence": 0.92,
      "bbox": [100, 200, 300, 400]
    }
  ],
  "sensor_data": {
    "motion": true,
    "light_level": 0.8,
    "temperature": 20.5
  },
  "location": {
    "lat": 37.7749,
    "lng": -122.4194
  },
  "context": {
    "camera_id": "cam_001",
    "zone": "entrance"
  }
}
```

### Response Format

```json
{
  "event_id": "unique_event_identifier",
  "processed_at": "2024-01-01T12:00:01Z",
  "meaning": "Routine daily activity",
  "human_explanation": "An event was detected during morning hours, suggesting daily routine activities. The system identified a person in the scene. This suggests human activity and social presence.",
  "significance_score": 0.4,
  "symbolic_features": [
    {
      "feature_name": "human_activity",
      "feature_value": true,
      "confidence": 0.92,
      "human_description": "Presence of person suggests human activity"
    }
  ],
  "reasoning_steps": [
    {
      "step_id": 1,
      "operation": "feature_aggregation",
      "confidence": 0.9,
      "explanation": "Identified 3 symbolic features from the event data"
    }
  ],
  "recommended_actions": [
    "Log this event for pattern analysis",
    "Monitor for similar events in the area"
  ],
  "processing_time_ms": 45.2
}
```

## Brand Licensing & Customization

### License Configuration

```python
license_config = LicenseConfig(
    brand_name="Your Brand Name",
    license_key="your-unique-license-key",
    
    # Customization options
    explanation_style="professional",  # "professional", "casual", "technical"
    custom_vocabulary={
        "person": "customer",
        "detected": "identified"
    },
    focus_areas=["security", "customer_behavior"],
    
    # API limits
    daily_request_limit=10000,
    rate_limit_per_minute=100,
    
    # Feature controls
    enabled_features=["object_detection", "reasoning", "explanations", "recommendations"]
)
```

### Brand-Specific Features

- **Custom Vocabulary**: Replace standard terms with brand-specific language
- **Explanation Styles**: Professional, casual, or technical tone
- **Focus Areas**: Emphasize specific domains (security, retail, etc.)
- **Feature Controls**: Enable/disable specific functionality
- **Rate Limiting**: Control API usage per brand
- **Custom Models**: Integration with brand-specific AI models

## Hardware Integration

### Object Detection Integration

```python
class HardwareIntegration:
    def __init__(self, license_config):
        self.engine = DeepReasonEngine(license_config)
    
    def on_detection_event(self, detected_objects, sensor_data):
        """Called when hardware detects objects"""
        event_data = EventData(
            event_id=f"hw_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            event_type=EventType.OBJECT_DETECTION,
            detected_objects=detected_objects,
            sensor_data=sensor_data
        )
        
        result = self.engine.process_event(event_data)
        
        # Take action based on significance
        if result.significance_score > 0.7:
            self.send_alert(result)
        elif result.significance_score > 0.4:
            self.log_event(result)
        
        return result
```

### Supported Hardware Types

- IP Cameras with AI processing
- Edge computing devices
- IoT sensors with object detection
- Security systems
- Retail analytics platforms
- Smart building systems

## Development

### Running Tests

```bash
# Install test dependencies
pip install -r test-requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=ai_happy --cov-report=html
```

### Development Setup

```bash
# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt -r test-requirements.txt

# Run linting
flake8 ai_happy/

# Run the example
python examples.py
```

### Project Structure

```
ai-happy/
├── ai_happy/
│   ├── __init__.py          # Package initialization
│   ├── models.py            # Data models and schemas
│   ├── engine.py            # Core reasoning engine
│   ├── api.py              # FastAPI application
│   └── config.py           # Configuration management
├── tests/
│   ├── test_engine.py      # Engine tests
│   └── test_api.py         # API tests
├── examples.py             # Usage examples
├── main.py                 # Server entry point
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Examples

See `examples.py` for comprehensive usage examples including:

- Direct library usage
- API client integration
- Hardware integration patterns
- Brand customization examples
- Batch processing
- Error handling

## Performance

- **Processing Time**: Typically 20-100ms per event
- **Throughput**: 100+ events/second on standard hardware
- **Memory Usage**: ~50MB base memory footprint
- **Scalability**: Horizontally scalable via API instances

## Security

- License key authentication
- Rate limiting per brand
- Input validation and sanitization
- Configurable CORS policies
- No sensitive data logging

## Licensing

This project is licensed under the MIT License - see the LICENSE file for details.

### Commercial Licensing

For commercial use and brand licensing:

1. Contact VerdantAI for licensing terms
2. Obtain your unique license key
3. Configure your brand-specific settings
4. Integrate with your hardware systems

## Support

- **Documentation**: See examples and API documentation above
- **Issues**: Report issues on GitHub
- **Commercial Support**: Contact VerdantAI for enterprise support

## Roadmap

- [ ] Advanced reasoning models
- [ ] Multi-language support
- [ ] Real-time streaming processing
- [ ] Enhanced brand customization
- [ ] Mobile SDK
- [ ] Cloud deployment options

---

**Ready to license AI Happy for your brand?** Contact VerdantAI to get started with embedding intelligent reasoning into your hardware systems.
