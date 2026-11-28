"""Базовый класс для всех платформ"""

from PyQt6.QtCore import QThread, pyqtSignal


class BasePlatformWorker(QThread):
    """Базовый воркер платформы"""

    connected = pyqtSignal(str)
    disconnected = pyqtSignal(str)
    message_received = pyqtSignal(str, str, str, dict, list)
    error_occurred = pyqtSignal(str)

    def __init__(self, platform_name: str, config: dict):
        super().__init__()
        self.platform_name = platform_name
        self.config = config
        self._is_running = False

    def run(self):
        """Запуск воркера — переопределяется в наследниках"""
        self._is_running = True
        try:
            self._connect()
            while self._is_running:
                self._process_messages()
                self.msleep(100)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self._disconnect()

    def stop(self):
        """Остановить воркер"""
        self._is_running = False
        self.wait()

    def send_message(self, message: str):
        """Отправить сообщение — переопределяется в наследниках"""
        raise NotImplementedError

    def _connect(self):
        """Подключение к платформе — переопределяется"""
        pass

    def _disconnect(self):
        """Отключение от платформы — переопределяется"""
        pass

    def _process_messages(self):
        """Обработка сообщений — переопределяется"""
        pass