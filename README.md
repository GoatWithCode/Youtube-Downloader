# Youtube-Downloader
Youtube Downloader in PyQt5

🛠️ YouTube Downloader – Installation Guide (Windows)

📁 1. Requirements
    Make sure you have Python 3.8 or higher installed:  
    The Application use ffmpeg download here: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip


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

- You can Download the Binary here: https://c.gmx.net/@329938113155568689/wq6hzWsyPuDKUyHVwcUi8Q
  

<img src="https://github.com/GoatWithCode/Pornhub-Downloader/blob/main/Screenshot%202025-05-20%20170528.png" alt="Youtube-downloader" width="800" height="400">
