@echo off
echo --- Starting Build Process ---
pip install pyinstaller

pyinstaller --noconfirm --onedir --windowed ^
 --name "SalesIntelligencePro" ^
 --collect-all "customtkinter" ^
 --collect-all "google" ^
 --collect-all "groq" ^
 --add-data "analytics_prompt.md;." ^
 "transcribe_gui.py"

echo.
echo --- Build Complete! ---
echo Your EXE is located in the "dist/SalesIntelligencePro" folder.
echo Don't forget to copy ffmpeg.exe and ffprobe.exe into that folder!
pause
