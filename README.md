# Youtube-Downloader
Youtube Downloader in PyQt5

🛠️ YouTube Downloader – Installation Guide (Windows)

📁 1. Requirements
    Make sure you have Python 3.8 or higher installed:  
    The Application use ffmpeg
   
    https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

    

📦 2. Install Required Packages
    
    pip install PyQt5 PyQtWebEngine yt-dlp

📂 3. Project Structure

    youtube_downloader/
    ├── downloader.py           
    ├── ffmpeg                  
    ├── goat_logo.png           
    ├── youtube.ico             
    └── downloads/              ← auto-created for finished files



📦 5. Build with PyInstaller (Optional)
    
    pyinstaller --noconfirm --windowed --icon=youtube.ico --add-data "goat_logo.png;." downloader.py

📌 Notes
- The script supports multiple video URLs.
- You can download MP3 audio files in different bitrates, or complete videos as .mkv.

<img src="https://github.com/GoatWithCode/Youtube-Downloader/blob/main/Screenshot%202025-05-19%20152554.png" alt="Girl in a jacket" width="800" height="400">
