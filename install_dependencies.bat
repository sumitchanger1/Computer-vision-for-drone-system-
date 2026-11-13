@echo off
echo ======================================================================
echo Desktop AI Assistant - Dependency Installer
echo ======================================================================
echo.
echo This will install all required Python packages...
echo.
pause

echo Installing dependencies...
echo.

pip install openai-whisper opencv-python pyautogui sounddevice soundfile soundfile librosa keyboard pynput pillow numpy requests

echo.
echo ======================================================================
echo Installation complete!
echo ======================================================================
echo.
echo You can now run:
echo   1. DesktopAI-Assistant.exe
echo   OR
echo   2. python launcher.py
echo.
pause