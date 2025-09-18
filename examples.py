"""
Example usage of the AI Happy reasoning engine.

This file demonstrates how to use the engine both as a library
and through the API for hardware integration.
"""

import asyncio
import json
from datetime import datetime
from ai_happy import DeepReasonEngine, EventData, LicenseConfig
from ai_happy.models import EventType

# Example 1: Direct library usage
def example_direct_usage():
    """Example of using the reasoning engine directly as a library."""
    print("=== Direct Library Usage Example ===")
    
    # Create a license configuration for a brand
    brand_license = LicenseConfig(
        brand_name="SmartSecurity Inc",
        license_key="smartsec-2024-key",
        explanation_style="professional",
        custom_vocabulary={
            "person": "individual",
            "detected": "identified"
        },
        focus_areas=["security", "monitoring"],
        enabled_features=["object_detection", "reasoning", "explanations"]
    )
    
    # Initialize the reasoning engine
    engine = DeepReasonEngine(brand_license)
    
    # Create sample event data (as would come from object detection hardware)
    event_data = EventData(
        event_id="evt_001_night_motion",
        event_type=EventType.OBJECT_DETECTION,
        timestamp=datetime.now().replace(hour=23, minute=30),  # Night time
        detected_objects=[
            {"name": "person", "confidence": 0.92, "bbox": [100, 200, 300, 400]},
            {"name": "car", "confidence": 0.87, "bbox": [50, 300, 250, 500]}
        ],
        sensor_data={
            "motion_detected": True,
            "light_level": 0.1,
            "temperature": 15.5
        },
        location={"lat": 37.7749, "lng": -122.4194},
        context={
            "camera_id": "cam_entrance_01",
            "zone": "parking_area"
        }
    )
    
    # Process the event
    result = engine.process_event(event_data)
    
    # Display results
    print(f"Event ID: {result.event_id}")
    print(f"Meaning: {result.meaning}")
    print(f"Significance Score: {result.significance_score:.2f}")
    print(f"Processing Time: {result.processing_time_ms:.2f}ms")
    print("\nHuman Explanation:")
    print(result.human_explanation)
    print("\nRecommended Actions:")
    for action in result.recommended_actions:
        print(f"- {action}")
    
    print("\nSymbolic Features Extracted:")
    for feature in result.symbolic_features:
        print(f"- {feature.feature_name}: {feature.feature_value} (confidence: {feature.confidence:.2f})")
    
    print("\nReasoning Steps:")
    for step in result.reasoning_steps:
        print(f"Step {step.step_id}: {step.operation} - {step.explanation}")


# Example 2: API client usage
async def example_api_usage():
    """Example of using the reasoning engine through the API."""
    print("\n=== API Usage Example ===")
    
    import httpx
    
    # This would be the API endpoint where the reasoning engine is deployed
    base_url = "http://localhost:8000"
    
    # License key for authentication
    headers = {
        "Authorization": "Bearer demo-key-12345",
        "Content-Type": "application/json"
    }
    
    # Example event data from hardware
    event_data = {
        "event_id": "api_evt_002_morning_activity",
        "event_type": "object_detection",
        "timestamp": datetime.now().replace(hour=9, minute=15).isoformat(),
        "detected_objects": [
            {"name": "person", "confidence": 0.95},
            {"name": "dog", "confidence": 0.88},
            {"name": "bicycle", "confidence": 0.91}
        ],
        "sensor_data": {
            "motion_detected": True,
            "light_level": 0.8,
            "weather": "sunny"
        },
        "context": {
            "camera_id": "cam_park_entrance",
            "zone": "recreational_area"
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            # Check API health
            health_response = await client.get(f"{base_url}/health")
            print(f"API Health Status: {health_response.json()['status']}")
            
            # Process event through API
            response = await client.post(
                f"{base_url}/api/v1/process",
                headers=headers,
                json=event_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"\nAPI Processing Result:")
                print(f"Meaning: {result['meaning']}")
                print(f"Significance: {result['significance_score']}")
                print(f"Explanation: {result['human_explanation']}")
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"Could not connect to API (make sure server is running): {e}")


# Example 3: Hardware integration template
def hardware_integration_example():
    """Example of how hardware systems would integrate with the engine."""
    print("\n=== Hardware Integration Example ===")
    
    class HardwareSimulator:
        """Simulates a hardware system with object detection."""
        
        def __init__(self, engine: DeepReasonEngine):
            self.engine = engine
            self.camera_id = "hardware_cam_01"
        
        def on_object_detected(self, objects, sensor_readings):
            """Called when the hardware detects objects."""
            # Create event data
            event_data = EventData(
                event_id=f"hw_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                event_type=EventType.OBJECT_DETECTION,
                detected_objects=objects,
                sensor_data=sensor_readings,
                context={
                    "camera_id": self.camera_id,
                    "hardware_version": "v2.1.0"
                }
            )
            
            # Process through reasoning engine
            result = self.engine.process_event(event_data)
            
            # Take action based on significance
            if result.significance_score > 0.7:
                self.send_alert(result)
            elif result.significance_score > 0.4:
                self.log_event(result)
            
            return result
        
        def send_alert(self, result):
            """Send high-priority alert."""
            print(f"🚨 HIGH PRIORITY ALERT: {result.meaning}")
            print(f"   Explanation: {result.human_explanation}")
        
        def log_event(self, result):
            """Log moderate-priority event."""
            print(f"📝 Event logged: {result.meaning}")
    
    # Initialize hardware with reasoning engine
    brand_config = LicenseConfig(
        brand_name="SecureTech Hardware",
        license_key="securetech-hw-2024",
        explanation_style="technical",
        focus_areas=["security", "hardware_integration"]
    )
    
    engine = DeepReasonEngine(brand_config)
    hardware = HardwareSimulator(engine)
    
    # Simulate hardware detections
    detections = [
        {
            "objects": [{"name": "person", "confidence": 0.94}],
            "sensors": {"motion": True, "sound_level": 0.3}
        },
        {
            "objects": [{"name": "car", "confidence": 0.89}, {"name": "person", "confidence": 0.76}],
            "sensors": {"motion": True, "light_level": 0.9}
        }
    ]
    
    for i, detection in enumerate(detections, 1):
        print(f"\nHardware Detection #{i}:")
        result = hardware.on_object_detected(
            detection["objects"], 
            detection["sensors"]
        )


# Example 4: Brand customization showcase
def brand_customization_example():
    """Show how different brands can customize the engine."""
    print("\n=== Brand Customization Example ===")
    
    # Brand 1: Retail store
    retail_config = LicenseConfig(
        brand_name="MegaMart Retail",
        license_key="megamart-retail-key",
        explanation_style="casual",
        custom_vocabulary={
            "person": "customer",
            "detected": "spotted",
            "significant": "important"
        },
        focus_areas=["customer_behavior", "theft_prevention"],
        enabled_features=["object_detection", "reasoning", "customer_insights"]
    )
    
    # Brand 2: Security company
    security_config = LicenseConfig(
        brand_name="EliteGuard Security",
        license_key="eliteguard-sec-key",
        explanation_style="professional",
        custom_vocabulary={
            "person": "subject",
            "event": "incident",
            "activity": "movement"
        },
        focus_areas=["perimeter_security", "threat_assessment"],
        enabled_features=["object_detection", "reasoning", "threat_analysis"]
    )
    
    # Same event, different brand interpretations
    event_data = EventData(
        event_id="brand_comparison_001",
        event_type=EventType.OBJECT_DETECTION,
        detected_objects=[{"name": "person", "confidence": 0.92}],
        timestamp=datetime.now().replace(hour=22),  # Evening
        context={"zone": "restricted_area"}
    )
    
    # Process with retail configuration
    retail_engine = DeepReasonEngine(retail_config)
    retail_result = retail_engine.process_event(event_data)
    
    print("Retail Store Interpretation:")
    print(f"- {retail_result.human_explanation}")
    
    # Process with security configuration
    security_engine = DeepReasonEngine(security_config)
    security_result = security_engine.process_event(event_data)
    
    print("\nSecurity Company Interpretation:")
    print(f"- {security_result.human_explanation}")


def main():
    """Run all examples."""
    print("AI Happy - Deep Reason Metacognition Engine Examples")
    print("=" * 60)
    
    # Run examples
    example_direct_usage()
    
    # API example (async)
    print("\nRunning API example...")
    try:
        asyncio.run(example_api_usage())
    except Exception as e:
        print(f"API example skipped: {e}")
    
    hardware_integration_example()
    brand_customization_example()
    
    print("\n" + "=" * 60)
    print("Examples completed! The AI Happy engine is ready for licensing and embedding.")


if __name__ == "__main__":
    main()