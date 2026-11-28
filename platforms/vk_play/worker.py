"""VK Play чат worker"""

import json
import urllib.request
from PyQt6.QtCore import pyqtSignal
from ..base import BasePlatformWorker


class VkPlayWorker(BasePlatformWorker):
    """Воркер VK Play"""

    def __init__(self, config: dict):
        super().__init__("vk_play", config)
        self.channel = config.get("channel", "")
        self.token = config.get("token", "")
        self._last_message_id = 0

    def _connect(self):
        """Подключение к VK Play"""
        try:
            if not self.channel or not self.token:
                self.error_occurred.emit("Не заполнены настройки")
                return

            self.connected.emit(self.channel)
        except Exception as e:
            self.error_occurred.emit(f"VK Play ошибка: {e}")

    def _disconnect(self):
        """Отключение"""
        self.disconnected.emit(self.channel)

    def _process_messages(self):
        """Обработка сообщений"""
        if not self.channel or not self.token:
            return

        try:
            # VK Play API для получения сообщений чата
            url = f"https://api.vkplay.live/v1/chat/{self.channel}/messages"
            headers = {"Authorization": f"Bearer {self.token}"}
            req = urllib.request.Request(url, headers=headers)

            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())

            if "messages" in data:
                for msg in data["messages"]:
                    msg_id = msg.get("id", 0)
                    if msg_id > self._last_message_id:
                        self._parse_message(msg)
                        self._last_message_id = msg_id

            self.msleep(2000)
        except Exception as e:
            self.error_occurred.emit(f"VK Play ошибка: {e}")
            self.msleep(5000)

    def _parse_message(self, msg: dict):
        """Парсинг сообщения VK Play"""
        try:
            username = msg.get("user", {}).get("nickname", "unknown")
            message = msg.get("text", "")
            color = msg.get("user", {}).get("color", "")

            self.message_received.emit(username, message, color, {}, [])
        except Exception as e:
            print(f"Ошибка парсинга VK Play: {e}")

    def send_message(self, message: str):
        """Отправить сообщение"""
        if not self.channel or not self.token:
            return

        try:
            url = f"https://api.vkplay.live/v1/chat/{self.channel}/messages"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            data = json.dumps({"text": message}).encode()
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")

            with urllib.request.urlopen(req) as response:
                response.read()
        except Exception as e:
            self.error_occurred.emit(f"Ошибка отправки: {e}")