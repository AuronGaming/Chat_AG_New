"""Локальный сервер тем Chat_AG: HTTP для файлов тем + WebSocket для сообщений"""

import base64
import hashlib
import json
import os
import socket
import struct
import threading
from urllib.parse import unquote

THEMES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'themes'))
WS_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

_clients = []
_clients_lock = threading.Lock()
_server_instance = None


def _send_frame(conn, opcode: int, payload: bytes):
    """Отправить WS-кадр (сервер -> клиент, без маски)"""
    header = bytes([0x80 | opcode])
    n = len(payload)
    if n < 126:
        header += bytes([n])
    elif n < 65536:
        header += bytes([126]) + struct.pack(">H", n)
    else:
        header += bytes([127]) + struct.pack(">Q", n)
    conn.sendall(header + payload)


def broadcast(message: dict):
    """Разослать сообщение во все подключённые оверлеи"""
    payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
    with _clients_lock:
        dead = []
        for c in _clients:
            try:
                _send_frame(c, 0x1, payload)
            except Exception:
                dead.append(c)
        for c in dead:
            if c in _clients:
                _clients.remove(c)


class OverlayServer:
    def __init__(self, port: int = 8383):
        self.port = port
        self.sock = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("127.0.0.1", self.port))
        self.sock.listen(16)
        self.running = True
        self.thread = threading.Thread(target=self._accept_loop, daemon=True)
        self.thread.start()
        print(f"🌐 Сервер оверлея запущен: http://localhost:{self.port}/themes/")

    def stop(self):
        self.running = False
        try:
            self.sock.close()
        except Exception:
            pass
        with _clients_lock:
            for c in list(_clients):
                try:
                    c.close()
                except Exception:
                    pass
            _clients.clear()
        print("🌐 Сервер оверлея остановлен")

    def _accept_loop(self):
        while self.running:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                break
            threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn):
        try:
            data = conn.recv(65536)
            if not data:
                return
            text = data.decode("utf-8", errors="replace")
            if "upgrade: websocket" in text.lower():
                if self._ws_handshake(conn, text):
                    self._ws_loop(conn)
            else:
                self._http_serve(conn, text)
        except Exception:
            pass
        finally:
            try:
                conn.close()
            except Exception:
                pass

    # ---------------- HTTP ----------------
    def _http_serve(self, conn, request_text):
        parts = request_text.split("\r\n")[0].split()
        if len(parts) < 2:
            return
        path = unquote(parts[1])

        if path == "/" or path == "":
            self._send_index(conn)
            return

        if path.startswith("/themes/"):
            rel = path[len("/themes/"):]
            full = os.path.normpath(os.path.join(THEMES_DIR, rel))
            if not full.startswith(THEMES_DIR):
                self._send_404(conn)
                return
        else:
            self._send_404(conn)
            return

        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        if not os.path.isfile(full):
            self._send_404(conn)
            return

        ext = os.path.splitext(full)[1].lower()
        ctype = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".svg": "image/svg+xml",
            ".json": "application/json",
            ".woff2": "font/woff2",
        }.get(ext, "application/octet-stream")

        with open(full, "rb") as f:
            body = f.read()
        head = (f"HTTP/1.1 200 OK\r\nContent-Type: {ctype}\r\n"
                f"Content-Length: {len(body)}\r\nCache-Control: no-store\r\n"
                f"Connection: close\r\n\r\n").encode()
        conn.sendall(head + body)

    def _send_index(self, conn):
        items = []
        if os.path.isdir(THEMES_DIR):
            for d in sorted(os.listdir(THEMES_DIR)):
                if os.path.isdir(os.path.join(THEMES_DIR, d)):
                    items.append(f'<li style="margin:6px 0"><a style="color:#238636" href="/themes/{d}/">{d}</a></li>')
        html = ("<html><body style='background:#0d1117;color:#e6edf3;font-family:sans-serif'>"
                "<h2>Chat AG — темы оверлея</h2><ul>" + "".join(items) + "</ul></body></html>")
        body = html.encode("utf-8")
        head = (f"HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n"
                f"Content-Length: {len(body)}\r\nConnection: close\r\n\r\n").encode()
        conn.sendall(head + body)

    def _send_404(self, conn):
        conn.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n"
                     b"Content-Length: 13\r\nConnection: close\r\n\r\n404 Not Found")

    # ---------------- WebSocket ----------------
    def _ws_handshake(self, conn, request_text) -> bool:
        key = None
        for line in request_text.split("\r\n"):
            if line.lower().startswith("sec-websocket-key:"):
                key = line.split(":", 1)[1].strip()
        if not key:
            return False
        accept = base64.b64encode(hashlib.sha1((key + WS_GUID).encode()).digest()).decode()
        conn.sendall(("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\n"
                      "Connection: Upgrade\r\n"
                      f"Sec-WebSocket-Accept: {accept}\r\n\r\n").encode())
        with _clients_lock:
            _clients.append(conn)
        return True

    def _ws_loop(self, conn):
        while self.running:
            frame = self._read_frame(conn)
            if frame is None:
                break
            opcode, payload = frame
            if opcode == 0x8:   # close
                break
            if opcode == 0x9:   # ping -> pong
                try:
                    _send_frame(conn, 0xA, payload)
                except Exception:
                    break
        with _clients_lock:
            if conn in _clients:
                _clients.remove(conn)

    def _recv_exact(self, conn, n):
        buf = b""
        while len(buf) < n:
            chunk = conn.recv(n - len(buf))
            if not chunk:
                return None
            buf += chunk
        return buf

    def _read_frame(self, conn):
        head = self._recv_exact(conn, 2)
        if not head:
            return None
        opcode = head[0] & 0x0F
        masked = head[1] & 0x80
        length = head[1] & 0x7F
        if length == 126:
            length = struct.unpack(">H", self._recv_exact(conn, 2))[0]
        elif length == 127:
            length = struct.unpack(">Q", self._recv_exact(conn, 8))[0]
        mask = self._recv_exact(conn, 4) if masked else None
        payload = self._recv_exact(conn, length) if length else b""
        if payload is None:
            return None
        if mask:
            payload = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        return opcode, payload


# ---------------- Управление сервером ----------------
def start_server(port: int = 8383):
    global _server_instance
    if _server_instance and _server_instance.running:
        if _server_instance.port == port:
            return _server_instance
        _server_instance.stop()
    _server_instance = OverlayServer(port)
    _server_instance.start()
    return _server_instance


def stop_server():
    global _server_instance
    if _server_instance:
        _server_instance.stop()
        _server_instance = None


def get_server():
    return _server_instance