# Youtube-Downloader
Youtube Downloader in PyQt5

🛠️ YouTube Downloader – Installation Guide (Windows)

📁 1. Requirements
    Make sure you have Python 3.8 or higher installed:  


📦 2. Install Required Packages
    pip install PyQt5 PyQtWebEngine yt-dlp

📂 3. Project Structure

    youtube_downloader/
    ├── downloader.py           ← your main script
    ├── goat_logo.png           ← animated splash logo
    ├── youtube.ico             ← window icon
    └── downloads/              ← auto-created for finished files



📦 5. Build with PyInstaller (Optional)
    
    pyinstaller --noconfirm --windowed --icon=youtube.ico --add-data "goat_logo.png;." downloader.py

📌 Notes
- The script supports multiple video URLs.
- You can download MP3 audio files in different bitrates, or complete videos as .mkv.
