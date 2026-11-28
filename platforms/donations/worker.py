"""DonationAlerts worker"""

import json
import websocket
from PyQt6.QtCore import pyqtSignal, QThread
from ..base import BasePlatformWorker


class DonationAlertsWorker(BasePlatformWorker):
    """Воркер DonationAlerts"""

    donation_received = pyqtSignal(str, str, float, str, str)

    def __init__(self, config: dict):
        super().__init__("donation_alerts", config)
        self.token = config.get("token", "")
        self._ws = None

    def _connect(self):
        """Подключение к DonationAlerts WebSocket"""
        try:
            if not self.token:
                self.error_occurred.emit("Токен не указан")
                return

            ws_url = f"wss://connect.donationalerts.com:443/socket.io/?EIO=3&transport=websocket"
            self._ws = websocket.WebSocketApp(
                ws_url,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close
            )
            self._ws.run_forever()
        except Exception as e:
            self.error_occurred.emit(f"DonationAlerts ошибка: {e}")

    def _on_open(self, ws):
        """WebSocket открыт"""
        self.connected.emit("donation_alerts")
        # Авторизация
        auth_msg = f'42["addon:connect", {{"token": "{self.token}"}}]'
        ws.send(auth_msg)

    def _on_message(self, ws, message: str):
        """Получено сообщение"""
        try:
            if message.startswith("42"):
                data = json.loads(message[2:])
                event = data[0]
                payload = data[1]

                if event == "donation":
                    self._handle_donation(payload)
                elif event == "chat_message":
                    self._handle_chat_message(payload)
        except Exception as e:
            print(f"Ошибка парсинга DA: {e}")

    def _handle_donation(self, payload: dict):
        """Обработка доната"""
        username = payload.get("username", "unknown")
        amount = float(payload.get("amount", 0))
        currency = payload.get("currency", "RUB")
        message = payload.get("message", "")

        self.donation_received.emit("donation_alerts", username, amount, currency, message)

    def _handle_chat_message(self, payload: dict):
        """Обработка сообщения чата"""
        username = payload.get("from", "unknown")
        message = payload.get("message", "")

        self.message_received.emit(username, message, "", {}, [])

    def _on_error(self, ws, error):
        """Ошибка WebSocket"""
        self.error_occurred.emit(str(error))

    def _on_close(self, ws, close_status_code, close_msg):
        """WebSocket закрыт"""
        self.disconnected.emit("donation_alerts")

    def _disconnect(self):
        """Отключение"""
        if self._ws:
            self._ws.close()
            self._ws = None

    def send_message(self, message: str):
        """DonationAlerts не поддерживает отправку сообщений"""
        pass