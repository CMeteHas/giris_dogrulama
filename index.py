import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

# Kullanıcı adı ve parola
username = "admin"
password = "password"

# Hoşgeldiniz sayfası HTML içeriği
welcome_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Hosgeldiniz</title>
</head>
<body>
    <h1>Hosgeldiniz!</h1>
    <p>Yerel web sitesine basari ile giris yaptiniz.</p>
</body>
</html>
"""

# Parola doğrulama fonksiyonu
def authenticate(credentials):
    auth_info = credentials.split(' ')[1]
    auth_info = base64.b64decode(auth_info).decode('utf-8')
    username_password = auth_info.split(':')
    if username_password[0] == username and username_password[1] == password:
        return True
    else:
        return False

# HTTP request handler
class RequestHandler(BaseHTTPRequestHandler):
    # GET isteği işleme
    def do_GET(self):
        if self.authenticate_user():
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(welcome_page.encode())
        else:
            self.send_authenticate_header()

    # Kullanıcı doğrulama
    def authenticate_user(self):
        if 'Authorization' in self.headers:
            return authenticate(self.headers['Authorization'])
        else:
            return False

    # Yetkilendirme hatası gönderme
    def send_authenticate_header(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Authentication Required"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'401 Unauthorized')

# Sunucu ayarları
host = 'localhost'
port = 8080

# HTTP sunucusu oluşturma ve çalıştırma
try:
    server = HTTPServer((host, port), RequestHandler)
    print('HTTP server başlatıldı - http://{}:{}'.format(host, port))
    server.serve_forever()
except KeyboardInterrupt:
    print('^C ile durduruldu')
    server.socket.close()
