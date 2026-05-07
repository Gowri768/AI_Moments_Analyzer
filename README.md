# AI Moments Analyzer

A web application that takes an uploaded video, extracts frames, and uses AI to generate chronological captions and detect objects frame-by-frame. It features a modern, premium web interface built with HTML/CSS/JS and a powerful FastAPI backend running **Salesforce BLIP** (for image captioning) and **YOLOv8** (for object detection).

## Prerequisites
- **Python 3.8+** must be installed on your machine.
- Git (optional, if cloning the repository).

## Installation

1. **Open your terminal** or command prompt and navigate to the project directory:
   ```bash
   cd path/to/AI_Moments_Analyzer
   ```

2. **Install the required Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The AI models are large, so downloading `torch` and the model weights might take a few minutes depending on your internet connection).*

## How to Run the App

There are two ways to start the application:

### Option 1: The Quick Way (Windows Only)
Simply double-click the `run_app.bat` file located in the project folder. It will start the server and automatically open the application in your default web browser.

### Option 2: Using the Terminal (Mac / Linux / Windows)
If you are on Mac/Linux, or prefer to use the terminal manually, follow these steps:

1. **Start the FastAPI Backend server**:
   Run the following command in your terminal from the project root:
   ```bash
   python -m uvicorn app:app --port 8000
   ```
   *Wait until you see `Application startup complete` in the terminal. The first time you run this, it will download the AI models which can take a little bit of time.*

2. **Open the Frontend UI**:
   Since the backend serves the frontend files automatically, you do not need to start a separate web server.
   
   Just open your web browser and navigate to:
   **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

## Usage
Once the website is open, simply drag and drop a `.mp4` video file into the upload zone. The UI will show a loading screen while the AI processes the video, and then display the generated story and chronological timeline tags!
