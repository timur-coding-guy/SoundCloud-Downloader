import yt_dlp
import os
import tempfile
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)


class SoundcloudDownloader:
    def __init__(self):
        self.output_dir = Path(tempfile.mkdtemp())

    def download(self, url: str) -> tuple[str, str, str]:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            "writethumbnail": True,
            "writeinfojson": True,
            "embedmetadata": True,
            "concurrentfragments": 8,
            "buffersize": 64 * 1024,
            "http_chunk_size": 10 * 1024 * 1024,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                },
                {
                    "key": "FFmpegMetadata",
                },
            ],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "download")
            thumbnail = info.get("thumbnail", "")
            filename = ydl.prepare_filename(info)
            base_name = os.path.splitext(filename)[0]
            mp3_path = f"{base_name}.mp3"

        return mp3_path, title, thumbnail

    def cleanup(self, filepath: str):
        base = os.path.splitext(filepath)[0]
        extensions = [".mp3", ".jpg", ".png", ".webp", ".json"]
        for ext in extensions:
            file_path = base + ext
            if os.path.exists(file_path):
                os.remove(file_path)
        if self.output_dir.exists():
            for file in self.output_dir.iterdir():
                file.unlink()
            os.rmdir(self.output_dir)

    def cleanup_dir(self):
        if self.output_dir.exists():
            for file in self.output_dir.iterdir():
                file.unlink()
            os.rmdir(self.output_dir)
