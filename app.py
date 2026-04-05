import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Security Engine is Active!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    raw_url = data.get('url', '').lower().strip()
    
    # 1. تنظيف الرابط واستخراج اسم الموقع (Domain)
    # هذي الخطوة تحول https://www.youtube.com/watch إلى youtube.com فقط
    try:
        if not raw_url.startswith(('http://', 'https://')):
            url_to_parse = 'http://' + raw_url
        else:
            url_to_parse = raw_url
        
        domain = urlparse(url_to_parse).netloc
        if domain.startswith('www.'):
            domain = domain[4:]
    except:
        domain = raw_url

    # 2. القائمة البيضاء الذكية (WhilteList)
    # أي موقع ينتهي بهذي الدومينات يعتبر آمن فوراً
    safe_list = ['youtube.com', 'google.com', 'google.sa', 'speedtest.net', 'microsoft.com', 'apple.com', 'twitter.com', 'x.com', 'facebook.com', 'instagram.com']
    
    is_safe = any(domain == s or domain.endswith('.' + s) for s in safe_list)

    if is_safe:
        result = "Safe"
    else:
        # 3. منطق الفحص للروابط المجهولة (Heuristics)
        # هنا السيرفر يشغل حواسه الأمنية
        if len(raw_url) > 100 or raw_url.count('.') > 4 or "@" in raw_url:
            result = "Phishing"
        else:
            result = "Safe"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
