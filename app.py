import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '').lower() # نحول الرابط لحروف صغيرة عشان الفحص
    
    # 1. القائمة البيضاء (الروابط الموثوقة 100%)
    trusted_domains = ["youtube.com", "google.com", "gmail.com", "outlook.com", "microsoft.com", "apple.com"]
    
    # فحص إذا كان الرابط يحتوي على أي دومين موثوق
    is_trusted = any(domain in url for domain in trusted_domains)

    if is_trusted:
        result = "Safe"
    else:
        # 2. هنا "منطق" الفحص للروابط الثانية (مؤقتاً للبروجكت)
        # إذا الرابط طويل جداً أو فيه رموز غريبة نعتبره مشبوه
        if len(url) > 50 or url.count('@') > 0 or url.count('-') > 3:
            result = "Phishing"
        else:
            result = "Safe"

    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
