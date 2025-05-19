import sys
import os
import threading
import urllib.request
import math

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget,
    QPushButton, QLabel, QLineEdit, QProgressBar, QMessageBox,
    QComboBox, QSpacerItem, QSizePolicy, QListWidget, QAbstractItemView,
    QGroupBox, QGridLayout
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl, pyqtSignal, Qt, QTimer, QPointF
from PyQt5.QtGui import QPixmap, QPainter, QPainterPath, QColor, QIcon
import yt_dlp

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def resource_path(relative_path):
    """ Get absolute path to resource, works for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class LoadingOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(400, 400)

        self.logo_label = QLabel(self)
        self.logo_size = 200
        self.logo_label.setGeometry(100, 100, self.logo_size, self.logo_size)
        self.set_rounded_logo(resource_path("goat_logo.png"))

        self.total_dots = 5
        self.angle_offset = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(300)

    def set_rounded_logo(self, path):
        pixmap = QPixmap(path).scaled(self.logo_size, self.logo_size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        rounded = QPixmap(self.logo_size, self.logo_size)
        rounded.fill(Qt.transparent)

        painter = QPainter(rounded)
        painter.setRenderHint(QPainter.Antialiasing)
        path_circle = QPainterPath()
        path_circle.addEllipse(0, 0, self.logo_size, self.logo_size)
        painter.setClipPath(path_circle)
        painter.drawPixmap(0, 0, pixmap)
        painter.end()

        self.logo_label.setPixmap(rounded)

    def update_animation(self):
        self.angle_offset = (self.angle_offset + 30) % 360
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = QPointF(self.width() / 2, self.height() / 2)
        radius = 130

        for i in range(self.total_dots):
            angle_deg = self.angle_offset + (360 / self.total_dots) * i
            angle_rad = math.radians(angle_deg)
            x = center.x() + radius * math.cos(angle_rad)
            y = center.y() + radius * math.sin(angle_rad)

            color = QColor(66, 133, 244, 220)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(x, y), 10, 10)

# Der Code ist identisch bis zur Stelle, wo Buttons erstellt werden
# Ab hier wurden die Buttons für Einzel-Download entfernt
# und die restlichen Teile entsprechend angepasst.

# ... (alle bisherigen Imports und Initialisierungen bleiben erhalten) ...

class YouTubeDownloaderWindow(QMainWindow):
    progress_signal = pyqtSignal(int, str)
    status_update_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader by G0at with Code 2025")
        self.setGeometry(100, 100, 1600, 950)
        self.setWindowIcon(QIcon("youtube.ico"))
        
        self.progress_signal.connect(self.update_progress)
        self.status_update_signal.connect(self.update_status)

        main_layout = QHBoxLayout()
        self.browser = QWebEngineView()
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122 Safari/537.36")
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        self.browser.setPage(QWebEnginePage(profile, self.browser))
        self.browser.setUrl(QUrl("https://www.youtube.com"))
        main_layout.addWidget(self.browser, stretch=3)

        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube Video URL here")
        self.url_input.setMinimumHeight(30)
        self.url_input.editingFinished.connect(self.fetch_video_info)

        self.audio_quality_label = QLabel("Select Audio Quality (kbps):")
        self.audio_quality_combo = QComboBox()
        self.audio_quality_combo.addItems(["320", "256", "192", "128"])

        self.url_list = QListWidget()
        self.url_list.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.add_to_list_button = QPushButton("Add to List")
        self.remove_selected_button = QPushButton("❌ Remove Selected")
        self.download_all_audio_button = QPushButton("🎵 Download list as MP3")
        self.download_all_video_button = QPushButton("🎬 Download list as Mkv")

        green_style = """
            QPushButton {
                background-color: #1DB954;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1ed760;
            }
            QPushButton:pressed {
                background-color: #159643;
            }
        """
        red_style = """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """
        blue_style = """
            QPushButton {
                background-color: #0000FF;
                color: white;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3333FF;
            }
        """
        for btn in [self.add_to_list_button, self.download_all_audio_button]:
            btn.setStyleSheet(green_style)
        self.remove_selected_button.setStyleSheet(red_style)
        self.download_all_video_button.setStyleSheet(blue_style)

        self.preview_group = QGroupBox("Video Preview")
        preview_layout = QGridLayout()
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(320, 180)
        self.thumbnail_label.setAlignment(Qt.AlignCenter)
        self.video_title = QLabel("Title: -")
        self.channel = QLabel("Channel: -")
        self.duration = QLabel("Duration: -")
        for label in [self.video_title, self.channel, self.duration]:
            label.setWordWrap(True)
        preview_layout.addWidget(self.thumbnail_label, 0, 0, 1, 2)
        preview_layout.addWidget(self.video_title, 1, 0, 1, 2)
        preview_layout.addWidget(self.channel, 2, 0)
        preview_layout.addWidget(self.duration, 2, 1)
        self.preview_group.setLayout(preview_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.status_label = QLabel("Ready")

        right_layout.addWidget(self.url_input)
        right_layout.addWidget(self.audio_quality_label)
        right_layout.addWidget(self.audio_quality_combo)
        right_layout.addWidget(self.add_to_list_button)      
        right_layout.addWidget(QLabel("Download List"))
        right_layout.addWidget(self.url_list)
        right_layout.addWidget(self.remove_selected_button)
        right_layout.addSpacing(30)
        right_layout.addWidget(self.download_all_audio_button)
        right_layout.addWidget(self.download_all_video_button)
        right_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        right_layout.addWidget(self.preview_group)
        right_layout.addWidget(self.progress_bar)
        right_layout.addWidget(self.status_label)

        main_layout.addWidget(right_panel, stretch=1)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.add_to_list_button.clicked.connect(self.add_url_to_list)
        self.remove_selected_button.clicked.connect(self.remove_selected_urls)
        self.download_all_audio_button.clicked.connect(lambda: self.download_list(False))
        self.download_all_video_button.clicked.connect(lambda: self.download_list(True))

        self._is_downloading = False

    def add_url_to_list(self):
        url = self.url_input.text().strip()
        if url:
            self.url_list.addItem(url)
            self.url_input.clear()
            self.clear_preview()
        else:
            QMessageBox.warning(self, "Error", "Please enter a valid URL.")

    def remove_selected_urls(self):
        for item in self.url_list.selectedItems():
            self.url_list.takeItem(self.url_list.row(item))

    def download_list(self, video=True):
        if self._is_downloading:
            QMessageBox.warning(self, "Download in Progress", "Please wait...")
            return
        urls = [self.url_list.item(i).text() for i in range(self.url_list.count())]
        if not urls:
            QMessageBox.warning(self, "Error", "The list is empty.")
            return
        self._is_downloading = True
        options = self.get_ydl_options(video)
        threading.Thread(target=self.run_yt_dlp_thread, args=(urls, options), daemon=True).start()

    def get_ydl_options(self, video=True):
        opts = {
            'progress_hooks': [self.progress_hook],
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'noplaylist': True
        }
        if not video:
            q = self.audio_quality_combo.currentText()
            opts.update({
                'format': 'bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': q,
                }],
                'postprocessor_args': ['-b:a', f'{q}k'],
                'prefer_ffmpeg': True,
            })
        else:
            opts['format'] = 'bestvideo+bestaudio/best'
            opts['merge_output_format'] = 'mkv'
        return opts

    def run_yt_dlp_thread(self, urls, options):
        try:
            for i, url in enumerate(urls):
                self.status_update_signal.emit(f"Download {i+1} of {len(urls)}: {url}")
                with yt_dlp.YoutubeDL(options) as ydl:
                    ydl.download([url])
                self.progress_signal.emit(100, "Done")
        except Exception as e:
            self.progress_signal.emit(0, f"Error: {str(e)}")
        finally:
            self._is_downloading = False

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate')
            downloaded = d.get('downloaded_bytes', 0)
            if total:
                percent = int(downloaded / total * 100)
                self.progress_signal.emit(percent, f"Downloading... {percent}%")
        elif d['status'] == 'finished':
            self.progress_signal.emit(100, "Processing...")

    def update_progress(self, percent, status):
        self.progress_bar.setValue(percent)
        self.status_label.setText(status)

    def update_status(self, text):
        self.status_label.setText(text)

    def fetch_video_info(self):
        url = self.url_input.text().strip()
        if not url:
            self.clear_preview()
            return

        def fetch():
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    if 'entries' in info:
                        info = info['entries'][0]
                    title = info.get('title', '-')
                    uploader = info.get('uploader', '-')
                    duration = info.get('duration_string') or f"{int(info['duration']) // 60}:{int(info['duration']) % 60:02}" if info.get('duration') else "-"
                    thumb = info.get('thumbnail', '')

                    self.video_title.setText(f"Title: {title}")
                    self.channel.setText(f"Channel: {uploader}")
                    self.duration.setText(f"Duration: {duration}")
                    if thumb:
                        data = urllib.request.urlopen(thumb).read()
                        pixmap = QPixmap()
                        pixmap.loadFromData(data)
                        scaled = pixmap.scaled(self.thumbnail_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.thumbnail_label.setPixmap(scaled)
                    else:
                        self.thumbnail_label.clear()
            except Exception:
                self.clear_preview()

        threading.Thread(target=fetch, daemon=True).start()

    def clear_preview(self):
        self.video_title.setText("Title: -")
        self.channel.setText("Channel: -")
        self.duration.setText("Duration: -")
        self.thumbnail_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = LoadingOverlay()
    splash.show()

    QTimer.singleShot(3000, lambda: (splash.close(), YouTubeDownloaderWindow().show()))

    sys.exit(app.exec_())
