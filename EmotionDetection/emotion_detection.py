"""
Module for detecting emotions in a given text using Watson NLP API.

Covers:
    - Task 2: Basic emotion detection via Watson API
    - Task 3: Formatted output with dominant emotion
    - Task 7: Error handling for blank input (status code 400)
"""
import json
import requests


def emotion_detector(text_to_analyze):
    """
    Analyze emotion from input text using the Watson NLP EmotionPredict endpoint.

    Args:
        text_to_analyze (str): The raw text to evaluate for emotional content.

    Returns:
        dict: A dictionary containing scores for 'anger', 'disgust', 'fear',
              'joy', and 'sadness', plus 'dominant_emotion' (the highest-scoring
              emotion). All values are None when the input is blank or invalid.
    """
    # Task 7 – guard against blank input before even calling the API
    if not text_to_analyze or not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = (
        'https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        # Network error (timeout, no route, DNS failure, etc.)
        # Return None values so the caller can show a friendly message.
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Task 7 – handle HTTP 400 returned by the API (e.g. empty / invalid body)
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    # Task 3 – parse and format the successful response
    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    scores_dict = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }

    dominant_emotion = max(scores_dict, key=scores_dict.get)

    return {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
        'dominant_emotion': dominant_emotion
    }
