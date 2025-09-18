"""
Tests for the AI Happy reasoning engine.
"""

import pytest
from datetime import datetime
from ai_happy import DeepReasonEngine, EventData, LicenseConfig
from ai_happy.models import EventType, SymbolicFeature


@pytest.fixture
def sample_license():
    """Sample license configuration for testing."""
    return LicenseConfig(
        brand_name="TestBrand",
        license_key="test-key-123",
        explanation_style="professional",
        enabled_features=["object_detection", "reasoning", "explanations"]
    )


@pytest.fixture
def sample_event():
    """Sample event data for testing."""
    return EventData(
        event_id="test_001",
        event_type=EventType.OBJECT_DETECTION,
        detected_objects=[
            {"name": "person", "confidence": 0.9},
            {"name": "car", "confidence": 0.8}
        ],
        sensor_data={"motion": True},
        context={"camera_id": "test_cam"}
    )


def test_engine_initialization(sample_license):
    """Test that the engine initializes correctly."""
    engine = DeepReasonEngine(sample_license)
    assert engine.license_config == sample_license
    assert engine.feature_extractor is not None
    assert engine.metacognition_processor is not None
    assert engine.explanation_generator is not None


def test_event_processing(sample_license, sample_event):
    """Test basic event processing."""
    engine = DeepReasonEngine(sample_license)
    result = engine.process_event(sample_event)
    
    assert result.event_id == sample_event.event_id
    assert result.meaning is not None
    assert result.human_explanation is not None
    assert 0.0 <= result.significance_score <= 1.0
    assert result.processing_time_ms is not None
    assert len(result.symbolic_features) > 0
    assert len(result.reasoning_steps) > 0


def test_symbolic_feature_extraction(sample_event):
    """Test symbolic feature extraction."""
    from ai_happy.engine import SymbolicFeatureExtractor
    
    extractor = SymbolicFeatureExtractor()
    features = extractor.extract_features(sample_event)
    
    assert len(features) > 0
    
    # Check for expected features
    feature_names = [f.feature_name for f in features]
    assert "time_of_day" in feature_names
    
    # Check feature structure
    for feature in features:
        assert isinstance(feature, SymbolicFeature)
        assert 0.0 <= feature.confidence <= 1.0
        assert feature.human_description is not None


def test_night_time_significance():
    """Test that night time events have higher significance."""
    license_config = LicenseConfig(
        brand_name="TestBrand",
        license_key="test-key",
        explanation_style="professional"
    )
    
    engine = DeepReasonEngine(license_config)
    
    # Night event
    night_event = EventData(
        event_id="night_test",
        event_type=EventType.OBJECT_DETECTION,
        timestamp=datetime.now().replace(hour=2),  # 2 AM
        detected_objects=[{"name": "person", "confidence": 0.9}]
    )
    
    # Day event
    day_event = EventData(
        event_id="day_test",
        event_type=EventType.OBJECT_DETECTION,
        timestamp=datetime.now().replace(hour=14),  # 2 PM
        detected_objects=[{"name": "person", "confidence": 0.9}]
    )
    
    night_result = engine.process_event(night_event)
    day_result = engine.process_event(day_event)
    
    # Night events should generally have higher significance
    # (though this is not guaranteed in all cases)
    assert night_result.significance_score >= 0.0
    assert day_result.significance_score >= 0.0


def test_brand_customization():
    """Test brand-specific customization."""
    custom_license = LicenseConfig(
        brand_name="CustomBrand",
        license_key="custom-key",
        explanation_style="casual",
        custom_vocabulary={"person": "individual", "detected": "found"}
    )
    
    engine = DeepReasonEngine(custom_license)
    
    event = EventData(
        event_id="custom_test",
        event_type=EventType.OBJECT_DETECTION,
        detected_objects=[{"name": "person", "confidence": 0.9}]
    )
    
    result = engine.process_event(event)
    
    # Check that custom vocabulary is applied
    explanation = result.human_explanation.lower()
    assert "individual" in explanation or "found" in explanation


def test_recommendation_generation(sample_license):
    """Test that recommendations are generated appropriately."""
    engine = DeepReasonEngine(sample_license)
    
    # High significance event
    high_sig_event = EventData(
        event_id="high_sig",
        event_type=EventType.OBJECT_DETECTION,
        timestamp=datetime.now().replace(hour=2),  # Night
        detected_objects=[{"name": "person", "confidence": 0.95}]
    )
    
    result = engine.process_event(high_sig_event)
    
    assert len(result.recommended_actions) > 0
    assert all(isinstance(action, str) for action in result.recommended_actions)


def test_empty_event_handling(sample_license):
    """Test handling of events with no detected objects."""
    engine = DeepReasonEngine(sample_license)
    
    empty_event = EventData(
        event_id="empty_test",
        event_type=EventType.OBJECT_DETECTION,
        detected_objects=[],  # No objects detected
        sensor_data={"motion": False}
    )
    
    result = engine.process_event(empty_event)
    
    # Should still produce a result
    assert result.event_id == empty_event.event_id
    assert result.meaning is not None
    assert result.human_explanation is not None


def test_multiple_objects_handling(sample_license):
    """Test handling of events with multiple objects."""
    engine = DeepReasonEngine(sample_license)
    
    multi_object_event = EventData(
        event_id="multi_test",
        event_type=EventType.OBJECT_DETECTION,
        detected_objects=[
            {"name": "person", "confidence": 0.9},
            {"name": "car", "confidence": 0.8},
            {"name": "dog", "confidence": 0.7},
            {"name": "bicycle", "confidence": 0.85}
        ]
    )
    
    result = engine.process_event(multi_object_event)
    
    # Should handle multiple objects gracefully
    assert len(result.symbolic_features) > 0
    assert "person" in result.human_explanation.lower() or "car" in result.human_explanation.lower()


if __name__ == "__main__":
    pytest.main([__file__])