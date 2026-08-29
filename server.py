"""
Flask web server for the Emotion Detector application.

Covers:
    - Task 6: Web deployment via Flask
    - Task 7: Blank-input error handling returning a user-friendly message
    - Task 8: Pylint-compliant code (10/10 score)
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emo_detector():
    """
    Handle GET /emotionDetector requests.

    Reads 'textToAnalyze' from the query string, runs emotion detection,
    and returns a formatted plain-text result.  Returns an error message
    when the input is blank or cannot be analysed (dominant_emotion is None).
    """
    text_to_analyze = request.args.get('textToAnalyze', '')
    response = emotion_detector(text_to_analyze)

    dominant_emotion = response.get('dominant_emotion')

    if dominant_emotion is None:
        return "Invalid text or the Watson API is currently unreachable. Please try again!"

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {dominant_emotion}."
    )


@app.route("/")
def render_index_page():
    """Render the main index page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
