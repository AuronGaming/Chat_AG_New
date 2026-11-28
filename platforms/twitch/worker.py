"""Twitch чат worker"""

import json
import socket
from PyQt6.QtCore import pyqtSignal
from ..base import BasePlatformWorker


class TwitchWorker(BasePlatformWorker):
    """Воркер Twitch"""

    def __init__(self, config: dict):
        super().__init__("twitch", config)
        self.channel = config.get("channel", "").lstrip("#")
        self.token = config.get("token", "")
        self._sock = None

    def _connect(self):
        """Подключение к Twitch IRC"""
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect(("irc.chat.twitch.tv", 6667))

            if self.token:
                self._sock.send(f"PASS oauth:{self.token}\r\n".encode())
            self._sock.send(f"NICK justinfan12345\r\n".encode())
            self._sock.send(f"JOIN #{self.channel}\r\n".encode())
            self._sock.send("CAP REQ :twitch.tv/tags twitch.tv/commands\r\n".encode())

            self.connected.emit(self.channel)
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _disconnect(self):
        """Отключение"""
        if self._sock:
            try:
                self._sock.send(f"PART #{self.channel}\r\n".encode())
                self._sock.close()
            except:
                pass
            self._sock = None
        self.disconnected.emit(self.channel)

    def _process_messages(self):
        """Обработка сообщений"""
        if not self._sock:
            return
        try:
            self._sock.setblocking(False)
            try:
                data = self._sock.recv(2048).decode("utf-8", errors="ignore")
                if not data:
                    return

                lines = data.split("\r\n")
                for line in lines:
                    if line.startswith("PING"):
                        self._sock.send("PONG :tmi.twitch.tv\r\n".encode())
                    elif "PRIVMSG" in line:
                        self._parse_message(line)
            except BlockingIOError:
                pass
        except Exception as e:
            self.error_occurred.emit(str(e))

    def _parse_message(self, line: str):
        """Парсинг сообщения Twitch"""
        try:
            # Извлечение username
            username = "unknown"
            if line.startswith("@"):
                tags_end = line.find(" ")
                tags = line[1:tags_end]
                for tag in tags.split(";"):
                    if tag.startswith("display-name="):
                        username = tag.split("=", 1)[1]

            # Извлечение сообщения
            msg_start = line.find("PRIVMSG") + len("PRIVMSG")
            msg_end = line.find(" :", msg_start)
            message = line[msg_end + 2:] if msg_end > msg_start else ""

            # Цвет (из тегов)
            color = ""
            if line.startswith("@"):
                tags_end = line.find(" ")
                tags = line[1:tags_end]
                for tag in tags.split(";"):
                    if tag.startswith("color="):
                        color = tag.split("=", 1)[1]

            self.message_received.emit(username, message, color, {}, [])
        except Exception as e:
            print(f"Ошибка парсинга Twitch: {e}")

    def send_message(self, message: str):
        """Отправить сообщение в чат"""
        if self._sock and self.token:
            try:
                self._sock.send(f"PRIVMSG #{self.channel} :{message}\r\n".encode())
            except Exception as e:
                self.error_occurred.emit(f"Ошибка отправки: {e}")