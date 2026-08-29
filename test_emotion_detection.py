"""
Unit tests for the EmotionDetection package.

Covers Task 5: verifies dominant emotion for five standard test sentences
plus a blank-input guard test.

The Watson API endpoint is only reachable inside the IBM Skills Network lab.
Outside the lab, responses are mocked so the test suite passes locally without
a network connection.  The production code (emotion_detection.py) is unchanged
and will hit the real endpoint when run inside the lab.
"""
import json
import unittest
from unittest.mock import patch, MagicMock

from EmotionDetection.emotion_detection import emotion_detector


def _make_mock_response(emotion_scores, status_code=200):
    """
    Build a mock requests.Response with the Watson API JSON payload.

    Args:
        emotion_scores (dict): e.g. {'anger': 0.8, 'disgust': 0.05, ...}
        status_code (int): HTTP status code to simulate.

    Returns:
        MagicMock: A mock that mimics requests.Response.
    """
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.ok = status_code < 400
    payload = {
        "emotionPredictions": [
            {"emotion": emotion_scores}
        ]
    }
    mock_response.text = json.dumps(payload)
    return mock_response


class TestEmotionDetection(unittest.TestCase):
    """Test suite for Watson NLP emotion detection (mocked API calls)."""

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_joy(self, mock_post):
        """Statement expected to produce joy as the dominant emotion."""
        mock_post.return_value = _make_mock_response({
            'anger': 0.01, 'disgust': 0.01, 'fear': 0.02,
            'joy': 0.95, 'sadness': 0.01
        })
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_anger(self, mock_post):
        """Statement expected to produce anger as the dominant emotion."""
        mock_post.return_value = _make_mock_response({
            'anger': 0.90, 'disgust': 0.05, 'fear': 0.02,
            'joy': 0.01, 'sadness': 0.02
        })
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_disgust(self, mock_post):
        """Statement expected to produce disgust as the dominant emotion."""
        mock_post.return_value = _make_mock_response({
            'anger': 0.05, 'disgust': 0.88, 'fear': 0.03,
            'joy': 0.01, 'sadness': 0.03
        })
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_sadness(self, mock_post):
        """Statement expected to produce sadness as the dominant emotion."""
        mock_post.return_value = _make_mock_response({
            'anger': 0.02, 'disgust': 0.02, 'fear': 0.05,
            'joy': 0.02, 'sadness': 0.89
        })
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_fear(self, mock_post):
        """Statement expected to produce fear as the dominant emotion."""
        mock_post.return_value = _make_mock_response({
            'anger': 0.03, 'disgust': 0.02, 'fear': 0.91,
            'joy': 0.01, 'sadness': 0.03
        })
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')

    def test_blank_input(self):
        """Blank input must return None for all fields including dominant_emotion.

        No API call should be made at all for blank input.
        """
        result = emotion_detector("")
        self.assertIsNone(result['dominant_emotion'])
        for key in ('anger', 'disgust', 'fear', 'joy', 'sadness'):
            self.assertIsNone(result[key])

    @patch('EmotionDetection.emotion_detection.requests.post')
    def test_status_400_returns_none(self, mock_post):
        """HTTP 400 from the API must produce a None dominant_emotion."""
        mock_post.return_value = _make_mock_response({}, status_code=400)
        result = emotion_detector("some text that causes 400")
        self.assertIsNone(result['dominant_emotion'])


if __name__ == '__main__':
    unittest.main()
