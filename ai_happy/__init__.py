"""
AI Happy - Deep Reason AI Metacognition Engine

A licensing-ready AI reasoning engine that can be embedded behind hardware
and object detection systems to provide meaningful event interpretation
and human-readable explanations.
"""

__version__ = "1.0.0"
__author__ = "VerdantAI"

from .engine import DeepReasonEngine
from .api import create_app
from .models import EventData, ReasoningResult, LicenseConfig

__all__ = ["DeepReasonEngine", "create_app", "EventData", "ReasoningResult", "LicenseConfig"]