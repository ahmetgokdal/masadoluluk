"""
ESP32-CAM Proxy - Kameranızı internete açar
KULLANIM: python camera_proxy.py
"""
from flask import Flask, Response
import requests

app = Flask(__name__)

# ESP32-CAM'in yerel IP'si
ESP32_CAM_URL = "http://192.168.3.210/capture"

@app.route('/capture')
def camera_stream():
    """Kamera görüntüsünü proxy et"""
    try:
        response = requests.get(ESP32_CAM_URL, timeout=5)
        return Response(response.content, mimetype='image/jpeg')
    except Exception as e:
        return f"Kamera hatası: {e}", 500

@app.route('/')
def home():
    return """
    <html>
    <body style="text-align:center; font-family:Arial; padding:50px;">
        <h1>📹 Kamera Proxy Çalışıyor!</h1>
        <p>Kamera görüntüsü: <a href="/capture">/capture</a></p>
        <img src="/capture" style="max-width:80%; border:2px solid #ccc;">
    </body>
    </html>
    """

if __name__ == '__main__':
    print("="*60)
    print("🚀 Kamera Proxy Başlatılıyor...")
    print("="*60)
    print("\n📹 Yerel Kamera: http://192.168.3.210/capture")
    print("🌐 Public URL: http://127.0.0.1:5000/capture")
    print("\n⚠️  Bu pencereyi kapatmayın!\n")
    
    # Flask'ı başlat
    app.run(host='0.0.0.0', port=5000, debug=False)
