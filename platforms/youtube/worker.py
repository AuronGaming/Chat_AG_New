"""YouTube чат worker"""

import time
import urllib.request
import json
from PyQt6.QtCore import pyqtSignal
from ..base import BasePlatformWorker


class YoutubeWorker(BasePlatformWorker):
    """Воркер YouTube"""

    def __init__(self, config: dict):
        super().__init__("youtube", config)
        self.api_key = config.get("api_key", "")
        self.channel_id = config.get("channel_id", "")
        self.live_chat_id = None
        self._next_page_token = None

    def _connect(self):
        """Подключение к YouTube Live Chat"""
        try:
            if not self.api_key or not self.channel_id:
                self.error_occurred.emit("Не заполнены настройки")
                return

            # Получаем live_chat_id
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={self.channel_id}&eventType=live&type=video&key={self.api_key}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            if "items" in data and len(data["items"]) > 0:
                video_id = data["items"][0]["id"]["videoId"]
                self._get_live_chat_id(video_id)
                self.connected.emit(self.channel_id)
            else:
                self.error_occurred.emit("Стрим не найден")
        except Exception as e:
            self.error_occurred.emit(f"YouTube ошибка: {e}")

    def _get_live_chat_id(self, video_id: str):
        """Получить ID чата"""
        url = f"https://www.googleapis.com/youtube/v3/videos?part=liveStreamingDetails&id={video_id}&key={self.api_key}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())

        if "items" in data and len(data["items"]) > 0:
            self.live_chat_id = data["items"][0]["snippet"]["liveChatId"]

    def _disconnect(self):
        """Отключение"""
        self.live_chat_id = None
        self.disconnected.emit(self.channel_id)

    def _process_messages(self):
        """Обработка сообщений"""
        if not self.live_chat_id or not self.api_key:
            return

        try:
            url = f"https://www.googleapis.com/youtube/v3/liveChat/messages?liveChatId={self.live_chat_id}&part=snippet,authorDetails&key={self.api_key}"
            if self._next_page_token:
                url += f"&pageToken={self._next_page_token}"

            req = urllib.request.Request(url)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            self._next_page_token = data.get("nextPageToken")

            if "items" in data:
                for item in data["items"]:
                    self._parse_message(item)

            # YouTube API лимит — ждём pollingIntervalMillis
            polling_interval = data.get("pollingIntervalMillis", 5000)
            self.msleep(polling_interval)
        except Exception as e:
            self.error_occurred.emit(f"YouTube ошибка: {e}")
            self.msleep(5000)

    def _parse_message(self, item: dict):
        """Парсинг сообщения YouTube"""
        try:
            author = item.get("authorDetails", {}).get("displayName", "unknown")
            message = item.get("snippet", {}).get("displayMessage", "")
            color = item.get("authorDetails", {}).get("channelId", "")

            self.message_received.emit(author, message, color, {}, [])
        except Exception as e:
            print(f"Ошибка парсинга YouTube: {e}")

    def send_message(self, message: str):
        """Отправить сообщение (требует OAuth)"""
        print(f"YouTube: отправка сообщений требует OAuth 2.0")