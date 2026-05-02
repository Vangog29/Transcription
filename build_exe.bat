@echo off
echo --- Cleaning old build files ---
if exist build rd /s /q build
if exist dist rd /s /q dist

echo --- Starting Build Process ---
pip install pyinstaller

pyinstaller --noconfirm --onedir --windowed ^
 --name "SalesIntelligencePro" ^
 --collect-all "customtkinter" ^
 --collect-all "google" ^
 --collect-all "groq" ^
 --add-data "analytics_prompt.md;." ^
 "transcribe_gui.py"

echo --- Copying FFmpeg binaries ---
copy ffmpeg.exe dist\SalesIntelligencePro\
copy ffprobe.exe dist\SalesIntelligencePro\

echo.
echo --- Build Complete! ---
echo Your EXE is located in the "dist/SalesIntelligencePro" folder.
echo All necessary files (FFmpeg, Prompt) have been included.
pause
