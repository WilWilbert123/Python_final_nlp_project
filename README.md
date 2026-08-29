# Emotion Detector

**Project Name:** Emotion Detector  
**Course:** IBM AI Developer Professional Certificate  
**Final Project:** AI-Based Web Application using Watson NLP  
**Developer:** Wilbert Gamis  

---

## Project Overview

Emotion Detector is an AI-based web application that analyzes the emotions present in a given text using the **IBM Watson NLP Emotion Predict** API. The application identifies five core emotions — **anger**, **disgust**, **fear**, **joy**, and **sadness** — and returns the **dominant emotion** from the input text.

---

## Project Structure

```
final_nlp_project/
│
├── EmotionDetection/
│   ├── __init__.py          # Package initializer (Task 4)
│   └── emotion_detection.py # Core detection logic (Tasks 2, 3, 7)
│
├── templates/
│   └── index.html           # Front-end UI
│
├── static/
│   └── mywebscript.js       # Client-side JavaScript
│
├── test_emotion_detection.py # Unit tests (Task 5)
├── server.py                 # Flask web server (Tasks 6, 7, 8)
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---

## Technologies Used

- **Python 3** — Core programming language
- **Flask** — Web framework for deployment
- **IBM Watson NLP** — Emotion Predict API (`emotion_aggregated-workflow_lang_en_stock`)
- **Requests** — HTTP client for Watson API calls
- **Pylint** — Static code analysis
- **Unittest** — Built-in Python testing framework

---

## Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/final_nlp_project.git
cd final_nlp_project

# 2. Install dependencies
pip3 install -r requirements.txt
```

---

## Running the Application

```bash
python3 server.py
```

Open your browser at **http://localhost:5001**

---

## Task Summary

| Task | Description | File(s) |
|------|-------------|---------|
| Task 1 | Clone the project repository | `README.md` |
| Task 2 | Create emotion detection application | `EmotionDetection/emotion_detection.py` |
| Task 3 | Format the output of the application | `EmotionDetection/emotion_detection.py` |
| Task 4 | Package the application | `EmotionDetection/__init__.py` |
| Task 5 | Run unit tests | `test_emotion_detection.py` |
| Task 6 | Web deployment using Flask | `server.py`, `templates/index.html` |
| Task 7 | Incorporate error handling | `emotion_detection.py`, `server.py` |
| Task 8 | Run static code analysis (Pylint 10/10) | `server.py` |

---

## Running Unit Tests

```bash
python3 -m unittest test_emotion_detection.py -v
```

Expected output:
```
test_anger ... ok
test_blank_input ... ok
test_disgust ... ok
test_fear ... ok
test_joy ... ok
test_sadness ... ok
test_status_400_returns_none ... ok

Ran 7 tests in 0.002s

OK
```

---

## Static Code Analysis

```bash
python3 -m pylint server.py
python3 -m pylint EmotionDetection/emotion_detection.py
```

Expected output:
```
Your code has been rated at 10.00/10
```

---

## License

MIT License — free to use and modify.
# Python_final_nlp_project
