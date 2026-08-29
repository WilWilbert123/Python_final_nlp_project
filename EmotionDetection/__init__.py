"""
EmotionDetection package initializer.

Exposes the emotion_detector function at the package level so callers can use:

    from EmotionDetection import emotion_detector
"""
from .emotion_detection import emotion_detector

__all__ = ['emotion_detector']
