from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open("contacts.html", "r", encoding="utf-8") as file:
            self.wfile.write(bytes(file.read().encode("utf-8")))

    def do_POST(self):
        # Считаем длину тела
        content_length = int(self.headers['Content-Length'])
        # Читаем тело запроса
        post_data = self.rfile.read(content_length).decode('utf-8')
        # Преобразуем в словарь
        data = parse_qs(post_data)
        name = data.get('name', [''])[0]
        email = data.get('email', [''])[0]

        # Обработка данных
        print(f"Получены данные: Имя={name}, Email={email}")

        # Ответ пользователю
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        response = f"<html><head><meta charset='UTF-8'></head><body><h1>Данные получены</h1></body></html>"
        self.wfile.write(bytes(response.encode('utf-8')))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()