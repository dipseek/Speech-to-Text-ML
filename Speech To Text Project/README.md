# Student Evaluation System - Speech to Text

A Python application that uses speech recognition to evaluate student answers against expected responses.

## Features

- **Speech Recording**: Record audio answers using your microphone
- **Speech to Text**: Convert spoken answers to text using Google Speech Recognition
- **Answer Evaluation**: Compare student answers with expected answers using semantic similarity
- **GUI Interface**: User-friendly Tkinter interface

## Requirements

- Python 3.7+
- Microphone access
- Internet connection (for Google Speech Recognition)

## Installation

1. Install required packages:
```bash
pip install SpeechRecognition pyaudio nltk sentence-transformers pandas
```

2. Download NLTK data:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

## Usage

### Method 1: Using the batch file (Windows)
Double-click `run_app.bat` to start the application.

### Method 2: Using Python directly
```bash
python final_project.py
```

## How to Use

1. **Start the Application**: The GUI will open showing available questions
2. **Enter Question Number**: Type a number (1-7) corresponding to the question you want to answer
3. **Record Your Answer**:
   - Click "Start Recording"
   - Speak your answer clearly
   - Click "Stop Recording" when finished
4. **Convert to Text**: Click "Convert to Text" to process your speech
5. **View Results**: See your recognized answer, the expected answer, and similarity score

## Files Description

- `final_project.py` - Main application file
- `question_set.csv` - Database of questions and expected answers
- `preprocess_data.pkl` - Processed question data (auto-generated)
- `run_app.bat` - Windows batch file to run the application
- `test_speech.py` - Test script for speech recognition

## Troubleshooting

- **Microphone Issues**: Ensure your microphone is connected and working
- **Speech Recognition**: Speak clearly and in a quiet environment
- **Internet Connection**: Required for Google Speech Recognition service

## Questions Available

1. What is Python? List some popular applications of Python in the world of technology.
2. What are the benefits of using Python language as a tool in the present scenario?
3. What is the difference between a Mutable datatype and an Immutable data type?
4. What is the difference between a Set and Dictionary?
5. What is a pass in Python?
6. Difference between for loop and while loop in Python 