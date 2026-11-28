"""Точка входа Chat_AG"""

import sys
import os
import traceback

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QIcon
    from main_screen.main_window import MainWindow

    def main():
        app = QApplication(sys.argv)
        # Гарантируем создание PNG галочки до загрузки UI
        from main_screen.checkbox_style import _ensure_check_png
        _ensure_check_png()
        from main_screen.checkbox_style import checkbox_style
        app.setStyleSheet(checkbox_style())
        app.setApplicationName("Chat_AG")
        app.setApplicationVersion("1.0.3")

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        icon_path = os.path.join(base_path, 'chat_ag_icon.ico')

        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            print(f"✅ Иконка приложения установлена: {icon_path}")
        else:
            print(f"⚠️ Иконка не найдена: {icon_path}")

        window = MainWindow()
        # Автозапуск сервера оверлея
        try:
            from core.settings_manager import SettingsManager
            _obs_cfg = SettingsManager().settings.get("obs_overlay", {})
            if _obs_cfg.get("enabled") or _obs_cfg.get("autostart_server"):
                from core.overlay_server import start_server
                start_server(_obs_cfg.get("port", 8383))
        except Exception as e:
            print(f"⚠️ Сервер оверлея не запущен: {e}")
        window.setWindowIcon(QIcon(icon_path) if os.path.exists(icon_path) else QIcon())
        window.show()
        import atexit

        def cleanup():
            """Очистка при закрытии"""
            try:
                from parameters.sound.audio import _tts_thread, _tts_queue
                if _tts_thread and _tts_thread.is_alive():
                    _tts_queue.put(None)
                    _tts_thread.join(timeout=2)
            except:
                pass

        atexit.register(cleanup)

        sys.exit(app.exec())

    if __name__ == "__main__":
        main()

except Exception as e:
    print("=" * 60)
    print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
    print("=" * 60)
    traceback.print_exc()
    input("\nНажмите Enter для выхода...")
    sys.exit(1)