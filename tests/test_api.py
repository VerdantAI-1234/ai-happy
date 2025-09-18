"""
Tests for the API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from ai_happy.api import create_app
from ai_happy.models import LicenseConfig


@pytest.fixture
def test_license():
    """Test license configuration."""
    return LicenseConfig(
        brand_name="TestAPI",
        license_key="test-api-key-123",
        explanation_style="professional",
        daily_request_limit=100,
        rate_limit_per_minute=10,
        enabled_features=["object_detection", "reasoning", "explanations"]
    )


@pytest.fixture
def client(test_license):
    """Test client with configured license."""
    app = create_app(test_license)
    return TestClient(app)


@pytest.fixture
def auth_headers(test_license):
    """Authentication headers for API requests."""
    return {"Authorization": f"Bearer {test_license.license_key}"}


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AI Happy - Deep Reason Metacognition Engine"
    assert "endpoints" in data


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded", "unhealthy"]
    assert "uptime_seconds" in data
    assert "version" in data


def test_process_event_endpoint(client, auth_headers):
    """Test the main event processing endpoint."""
    event_data = {
        "event_id": "api_test_001",
        "event_type": "object_detection",
        "timestamp": datetime.now().isoformat(),
        "detected_objects": [
            {"name": "person", "confidence": 0.9},
            {"name": "car", "confidence": 0.8}
        ],
        "sensor_data": {"motion": True},
        "context": {"camera_id": "test_cam"}
    }
    
    response = client.post("/api/v1/process", json=event_data, headers=auth_headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["event_id"] == event_data["event_id"]
    assert "meaning" in result
    assert "human_explanation" in result
    assert "significance_score" in result
    assert "symbolic_features" in result
    assert "reasoning_steps" in result


def test_process_event_unauthorized(client):
    """Test process endpoint without authorization."""
    event_data = {
        "event_id": "unauth_test",
        "event_type": "object_detection",
        "detected_objects": []
    }
    
    response = client.post("/api/v1/process", json=event_data)
    assert response.status_code == 401


def test_process_event_invalid_license(client):
    """Test process endpoint with invalid license key."""
    event_data = {
        "event_id": "invalid_test",
        "event_type": "object_detection",
        "detected_objects": []
    }
    
    headers = {"Authorization": "Bearer invalid-key"}
    response = client.post("/api/v1/process", json=event_data, headers=headers)
    assert response.status_code == 401


def test_batch_process_endpoint(client, auth_headers):
    """Test batch processing endpoint."""
    events = [
        {
            "event_id": "batch_test_001",
            "event_type": "object_detection",
            "detected_objects": [{"name": "person", "confidence": 0.9}]
        },
        {
            "event_id": "batch_test_002", 
            "event_type": "object_detection",
            "detected_objects": [{"name": "car", "confidence": 0.8}]
        }
    ]
    
    response = client.post("/api/v1/batch-process", json=events, headers=auth_headers)
    assert response.status_code == 200
    
    result = response.json()
    assert result["status"] == "success"
    assert result["processed_count"] == 2
    assert len(result["results"]) == 2


def test_batch_process_oversized(client, auth_headers):
    """Test batch processing with too many events."""
    # Create 101 events (over the limit of 100)
    events = [
        {
            "event_id": f"batch_oversized_{i:03d}",
            "event_type": "object_detection",
            "detected_objects": []
        }
        for i in range(101)
    ]
    
    response = client.post("/api/v1/batch-process", json=events, headers=auth_headers)
    assert response.status_code == 400
    assert "exceed 100 events" in response.json()["detail"]


def test_configure_license_endpoint(client):
    """Test license configuration endpoint."""
    new_license = {
        "brand_name": "NewBrand",
        "license_key": "new-key-456",
        "explanation_style": "casual",
        "enabled_features": ["object_detection", "reasoning"]
    }
    
    response = client.post("/api/v1/license", json=new_license)
    assert response.status_code == 200
    
    result = response.json()
    assert result["status"] == "success"
    assert "NewBrand" in result["message"]


def test_get_license_info_endpoint(client, auth_headers):
    """Test getting license information."""
    response = client.get("/api/v1/license", headers=auth_headers)
    assert response.status_code == 200
    
    result = response.json()
    assert "brand_name" in result
    assert "explanation_style" in result
    assert "enabled_features" in result


def test_malformed_event_data(client, auth_headers):
    """Test handling of malformed event data."""
    malformed_data = {
        "event_id": "malformed_test",
        # Missing required event_type
        "detected_objects": []
    }
    
    response = client.post("/api/v1/process", json=malformed_data, headers=auth_headers)
    assert response.status_code == 422  # Validation error


if __name__ == "__main__":
    pytest.main([__file__])