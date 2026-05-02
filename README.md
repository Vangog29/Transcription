# Sales Intelligence Pro (Groq + Gemma 4)

Professional tool for automated transcription of sales calls using **Groq (Whisper-large-v3)** and intelligent quality assurance analytics via **Google's Gemma 4 31B** model.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## 🚀 Key Features
- **High-Performance Transcription**: Uses Groq API for near-instant speech-to-text.
- **AI Analytics**: Intelligent call analysis, scoring, and insight extraction using Google's Gemma 4.
- **Smart Compression**: Automatically compresses large audio files (>25MB) to meet API limits without losing quality.
- **Portable & User-Friendly**: Modern GUI built with CustomTkinter, can be compiled into a single `.exe`.
- **Flexible Configuration**: Externalize your system prompts and API keys for security and customization.

## 🛠 Tech Stack
- **Backend**: Python 3.10+
- **Transcription**: Groq SDK (Whisper-large-v3)
- **Analytics**: Google GenAI SDK (Gemma-4-31b-it)
- **GUI**: CustomTkinter
- **Audio Processing**: FFmpeg

## 📦 Installation & Setup

### 1. Requirements
- Python 3.10 or higher
- FFmpeg (included in release or must be in PATH)
- API Keys for [Groq](https://console.groq.com/) and [Google AI Studio](https://aistudio.google.com/)

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/SalesIntelligencePro.git
cd SalesIntelligencePro

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. API Configuration
Create two files (or use the Settings tab in the app):
- `api_kay_groc.md`: Paste your Groq API key.
- `api_kay_google.md`: Paste your Google API key.

## 🔨 Building Executable
To create a standalone `.exe` file, use the provided build script:
```bash
build_exe.bat
```
The output will be in the `dist/` folder.

## 📄 Documentation
- [User Guide (RU)](INSTRUCTIONS.md) - How to use the application.
- [Build Guide (RU)](BUILD_GUIDE.md) - Technical details for compilation.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📜 License
This project is [MIT](LICENSE) licensed.
