import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Active and Smart!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # تنظيف الرابط من المسافات والحروف الكبيرة
        url = data.get('url', '').lower().strip()
        
        print(f"Checking URL: {url}") # هذا بيظهر لك في الـ Logs حقت Render

        # 1. القاعدة الذهبية: إذا الكلمة موجودة، الرابط آمن فوراً
        # هذي الحركة تضمن إن يوتيوب وتيك توك وكل الكبار يضبطون
        safe_keywords = ['youtube', 'youtu.be', 'google', 'tiktok', 'speedtest', 'instagram', 'facebook']
        
        is_safe_keyword = any(keyword in url for keyword in safe_keywords)

        if is_safe_keyword:
            result = "Safe"
        # 2. فحص الروابط المشبوهة (المنطق الأمني)
        elif len(url) > 80 or url.count('-') > 4 or url.count('.') > 4:
            result = "Phishing"
        else:
            result = "Safe"

        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
