"""Аудио утилиты — pyttsx3 с пересозданием движка"""

import threading
import queue

_tts_queue = None
_tts_thread = None
_voices_cache = []
_voices_ready = None
_lock = threading.Lock()
_started = False


def _ensure_worker():
    global _tts_queue, _tts_thread, _voices_ready, _started
    with _lock:
        if _started:
            return
        _tts_queue = queue.Queue()
        _voices_ready = threading.Event()
        _tts_thread = threading.Thread(target=_tts_worker, daemon=True)
        _tts_thread.start()
        _started = True


def _tts_worker():
    global _voices_cache
    import pyttsx3

    # Читаем голоса
    try:
        eng = pyttsx3.init()
        voices = eng.getProperty('voices')
        _voices_cache = [(v.id, v.name) for v in voices]
        eng.stop()
        del eng
    except Exception as e:
        print(f"⚠️ Ошибка чтения голосов: {e}")
        _voices_cache = []
    _voices_ready.set()

    # Крутим очередь
    while True:
        task = _tts_queue.get()
        if task is None:
            break
        text, voice_id, rate, volume = task
        try:
            eng = pyttsx3.init()
            if voice_id:
                eng.setProperty('voice', voice_id)
            eng.setProperty('rate', max(50, min(300, int(rate))))
            eng.setProperty('volume', max(0.0, min(1.0, float(volume) / 100.0)))
            eng.say(text)
            eng.runAndWait()
            eng.stop()
            del eng
        except Exception as e:
            print(f"❌ Ошибка TTS: {e}")


def get_voices(timeout=2.0):
    _ensure_worker()
    _voices_ready.wait(timeout=timeout)
    return _voices_cache if _voices_cache else [("", "Голоса не найдены")]


def speak(text: str, voice_id: str = "", rate: int = 200, volume: int = 100):
    if not text:
        return
    _ensure_worker()
    _tts_queue.put((text, voice_id, rate, volume))


def play_sound(file_path: str = ""):
    try:
        if not file_path or file_path == "По умолчанию":
            import winsound
            winsound.MessageBeep(winsound.MB_OK)
            return
        if file_path == "Без звука":
            return
        from PyQt6.QtMultimedia import QSoundEffect
        from PyQt6.QtCore import QUrl
        sound = QSoundEffect()
        sound.setSource(QUrl.fromLocalFile(file_path))
        sound.setVolume(1.0)
        sound.play()
    except Exception as e:
        print(f"❌ Ошибка воспроизведения: {e}")