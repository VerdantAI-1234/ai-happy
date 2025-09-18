"""
Deep Reason AI Metacognition Engine

Core reasoning engine that processes events and generates human-readable explanations.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import numpy as np
from .models import EventData, ReasoningResult, SymbolicFeature, ReasoningStep, LicenseConfig

logger = logging.getLogger(__name__)


class SymbolicFeatureExtractor:
    """
    Extracts symbolic human features from event data.
    """
    
    def __init__(self):
        # Common object categories and their symbolic meanings
        self.object_symbolism = {
            "person": {"social_presence": True, "human_activity": True},
            "car": {"transportation": True, "mobility": True, "modern_life": True},
            "dog": {"companionship": True, "loyalty": True, "domestic_life": True},
            "cat": {"independence": True, "comfort": True, "domestic_life": True},
            "bird": {"freedom": True, "nature": True, "vitality": True},
            "bicycle": {"health": True, "exercise": True, "eco_friendly": True},
            "book": {"knowledge": True, "learning": True, "intellectual_activity": True},
            "phone": {"communication": True, "connectivity": True, "modern_life": True},
        }
    
    def extract_features(self, event_data: EventData) -> List[SymbolicFeature]:
        """Extract symbolic features from event data."""
        features = []
        
        # Extract features from detected objects
        for obj in event_data.detected_objects:
            obj_name = obj.get("name", "").lower()
            confidence = obj.get("confidence", 0.0)
            
            if obj_name in self.object_symbolism:
                symbolism = self.object_symbolism[obj_name]
                for symbol, present in symbolism.items():
                    if present:
                        features.append(SymbolicFeature(
                            feature_name=symbol,
                            feature_value=True,
                            confidence=confidence * 0.8,  # Slightly reduce confidence for symbolic interpretation
                            human_description=f"Presence of {obj_name} suggests {symbol.replace('_', ' ')}"
                        ))
        
        # Extract temporal features
        hour = event_data.timestamp.hour
        if 6 <= hour < 12:
            features.append(SymbolicFeature(
                feature_name="time_of_day",
                feature_value="morning",
                confidence=1.0,
                human_description="Event occurred during morning hours, suggesting daily routine activities"
            ))
        elif 12 <= hour < 18:
            features.append(SymbolicFeature(
                feature_name="time_of_day",
                feature_value="afternoon",
                confidence=1.0,
                human_description="Event occurred during afternoon, indicating active daytime period"
            ))
        elif 18 <= hour < 22:
            features.append(SymbolicFeature(
                feature_name="time_of_day",
                feature_value="evening",
                confidence=1.0,
                human_description="Event occurred during evening, suggesting end-of-day activities"
            ))
        else:
            features.append(SymbolicFeature(
                feature_name="time_of_day",
                feature_value="night",
                confidence=1.0,
                human_description="Event occurred during night hours, indicating unusual or security-relevant activity"
            ))
        
        # Extract location-based features if available
        if event_data.location:
            features.append(SymbolicFeature(
                feature_name="location_tracked",
                feature_value=True,
                confidence=1.0,
                human_description="Event has location information, enabling spatial context analysis"
            ))
        
        return features


class MetacognitionProcessor:
    """
    Processes symbolic features using metacognitive reasoning.
    """
    
    def __init__(self):
        self.reasoning_patterns = {
            "routine_activity": {
                "triggers": ["human_activity", "morning", "domestic_life"],
                "meaning": "routine daily activity",
                "significance": 0.3
            },
            "social_interaction": {
                "triggers": ["social_presence", "communication"],
                "meaning": "social interaction or gathering",
                "significance": 0.6
            },
            "security_event": {
                "triggers": ["night", "human_activity"],
                "meaning": "potential security-relevant event",
                "significance": 0.8
            },
            "lifestyle_activity": {
                "triggers": ["exercise", "health", "eco_friendly"],
                "meaning": "health and lifestyle conscious activity",
                "significance": 0.5
            },
            "modern_life": {
                "triggers": ["modern_life", "connectivity", "transportation"],
                "meaning": "modern lifestyle and technology usage",
                "significance": 0.4
            }
        }
    
    def process(self, features: List[SymbolicFeature]) -> List[ReasoningStep]:
        """Process symbolic features through metacognitive reasoning."""
        steps = []
        feature_names = [f.feature_name for f in features]
        feature_values = [f.feature_value for f in features]
        
        step_id = 1
        
        # Step 1: Feature aggregation
        steps.append(ReasoningStep(
            step_id=step_id,
            operation="feature_aggregation",
            input_data={"features": feature_names},
            output_data={"aggregated_features": feature_names},
            confidence=0.9,
            explanation=f"Identified {len(features)} symbolic features from the event data"
        ))
        step_id += 1
        
        # Step 2: Pattern matching
        matched_patterns = []
        for pattern_name, pattern in self.reasoning_patterns.items():
            triggers = pattern["triggers"]
            matches = sum(1 for trigger in triggers if trigger in feature_names)
            if matches >= len(triggers) * 0.6:  # 60% match threshold
                matched_patterns.append({
                    "name": pattern_name,
                    "match_score": matches / len(triggers),
                    "meaning": pattern["meaning"],
                    "significance": pattern["significance"]
                })
        
        steps.append(ReasoningStep(
            step_id=step_id,
            operation="pattern_matching",
            input_data={"features": feature_names, "patterns": list(self.reasoning_patterns.keys())},
            output_data={"matched_patterns": matched_patterns},
            confidence=0.8,
            explanation=f"Matched {len(matched_patterns)} reasoning patterns based on feature combinations"
        ))
        step_id += 1
        
        # Step 3: Significance assessment
        overall_significance = 0.0
        if matched_patterns:
            overall_significance = max(p["significance"] for p in matched_patterns)
        
        steps.append(ReasoningStep(
            step_id=step_id,
            operation="significance_assessment",
            input_data={"matched_patterns": matched_patterns},
            output_data={"significance_score": overall_significance},
            confidence=0.7,
            explanation=f"Assessed overall event significance as {overall_significance:.2f} based on pattern analysis"
        ))
        
        return steps


class ExplanationGenerator:
    """
    Generates human-readable explanations from reasoning results.
    """
    
    def __init__(self, license_config: Optional[LicenseConfig] = None):
        self.license_config = license_config
        self.style = "professional"
        if license_config:
            self.style = license_config.explanation_style
    
    def generate_explanation(self, event_data: EventData, features: List[SymbolicFeature], 
                           reasoning_steps: List[ReasoningStep]) -> tuple[str, str]:
        """Generate meaning and detailed explanation."""
        
        # Extract key information
        objects = [obj.get("name", "unknown") for obj in event_data.detected_objects]
        time_features = [f for f in features if f.feature_name == "time_of_day"]
        symbolic_meanings = [f for f in features if f.feature_name not in ["time_of_day", "location_tracked"]]
        
        # Determine primary meaning
        if reasoning_steps:
            last_step = reasoning_steps[-1]
            significance = last_step.output_data.get("significance_score", 0.0)
            
            if significance > 0.7:
                meaning = "Significant event requiring attention"
            elif significance > 0.4:
                meaning = "Notable activity with moderate importance"
            else:
                meaning = "Routine activity with standard patterns"
        else:
            meaning = "Event detected with basic object recognition"
        
        # Generate detailed explanation
        explanation_parts = []
        
        # Context setting
        time_desc = time_features[0].human_description if time_features else "at an unspecified time"
        explanation_parts.append(f"An event was detected {time_desc}.")
        
        # Object description
        if objects:
            if len(objects) == 1:
                explanation_parts.append(f"The system identified a {objects[0]} in the scene.")
            else:
                obj_list = ", ".join(objects[:-1]) + f" and {objects[-1]}"
                explanation_parts.append(f"The system identified multiple objects: {obj_list}.")
        
        # Symbolic interpretation
        if symbolic_meanings:
            symbol_descriptions = [f.human_description.lower() for f in symbolic_meanings[:3]]  # Limit to top 3
            if symbol_descriptions:
                explanation_parts.append("This suggests " + "; ".join(symbol_descriptions) + ".")
        
        # Reasoning process summary
        if reasoning_steps:
            pattern_step = next((s for s in reasoning_steps if s.operation == "pattern_matching"), None)
            if pattern_step:
                matched_patterns = pattern_step.output_data.get("matched_patterns", [])
                if matched_patterns:
                    primary_pattern = max(matched_patterns, key=lambda p: p["match_score"])
                    explanation_parts.append(f"The analysis indicates this represents {primary_pattern['meaning']}.")
        
        # Brand customization
        if self.license_config and self.license_config.custom_vocabulary:
            # Apply custom vocabulary replacements
            explanation = " ".join(explanation_parts)
            for original, replacement in self.license_config.custom_vocabulary.items():
                explanation = explanation.replace(original, replacement)
            explanation_parts = [explanation]
        
        detailed_explanation = " ".join(explanation_parts)
        
        return meaning, detailed_explanation


class DeepReasonEngine:
    """
    Main reasoning engine that orchestrates the entire process.
    """
    
    def __init__(self, license_config: Optional[LicenseConfig] = None):
        self.license_config = license_config
        self.feature_extractor = SymbolicFeatureExtractor()
        self.metacognition_processor = MetacognitionProcessor()
        self.explanation_generator = ExplanationGenerator(license_config)
        
        logger.info(f"DeepReasonEngine initialized with license: {license_config.brand_name if license_config else 'None'}")
    
    def process_event(self, event_data: EventData) -> ReasoningResult:
        """
        Process an event through the complete reasoning pipeline.
        """
        start_time = time.time()
        
        try:
            # Step 1: Extract symbolic features
            symbolic_features = self.feature_extractor.extract_features(event_data)
            logger.debug(f"Extracted {len(symbolic_features)} symbolic features")
            
            # Step 2: Metacognitive processing
            reasoning_steps = self.metacognition_processor.process(symbolic_features)
            logger.debug(f"Completed {len(reasoning_steps)} reasoning steps")
            
            # Step 3: Generate human explanation
            meaning, human_explanation = self.explanation_generator.generate_explanation(
                event_data, symbolic_features, reasoning_steps
            )
            
            # Step 4: Calculate final significance
            significance_score = 0.5  # Default
            if reasoning_steps:
                last_step = reasoning_steps[-1]
                significance_score = last_step.output_data.get("significance_score", 0.5)
            
            # Step 5: Generate recommendations
            recommendations = self._generate_recommendations(significance_score, symbolic_features)
            
            processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            result = ReasoningResult(
                event_id=event_data.event_id,
                symbolic_features=symbolic_features,
                reasoning_steps=reasoning_steps,
                meaning=meaning,
                human_explanation=human_explanation,
                significance_score=significance_score,
                recommended_actions=recommendations,
                processing_time_ms=processing_time,
                model_version="1.0.0"
            )
            
            logger.info(f"Successfully processed event {event_data.event_id} in {processing_time:.2f}ms")
            return result
            
        except Exception as e:
            logger.error(f"Error processing event {event_data.event_id}: {str(e)}")
            raise
    
    def _generate_recommendations(self, significance_score: float, 
                                 features: List[SymbolicFeature]) -> List[str]:
        """Generate actionable recommendations based on the analysis."""
        recommendations = []
        
        if significance_score > 0.7:
            recommendations.append("Review this event for potential security implications")
            recommendations.append("Consider alerting relevant personnel")
        elif significance_score > 0.4:
            recommendations.append("Log this event for pattern analysis")
            recommendations.append("Monitor for similar events in the area")
        else:
            recommendations.append("Archive as routine activity")
        
        # Feature-specific recommendations
        night_features = [f for f in features if f.feature_value == "night"]
        if night_features:
            recommendations.append("Increase monitoring sensitivity during night hours")
        
        social_features = [f for f in features if "social" in f.feature_name]
        if social_features:
            recommendations.append("Consider social dynamics in area planning")
        
        return recommendations[:3]  # Limit to top 3 recommendations