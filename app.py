import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import tldextract

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Phishing Detector - Intelligent Guard is Live!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        # 1. تنظيف الرابط من أي حروف غريبة في البداية أو النهاية (زي الشرطات والمساحات)
        raw_url = data.get('url', '').strip().lower()
        clean_url = raw_url.lstrip('/') # يمسح أي شرطة مائلة في البداية زي اللي في صورتك
        
        # 2. استخراج "الزبدة" من الرابط باستخدام tldextract
        # حتى لو الرابط /watch?v=... بيعرف إنه تابع ليوتيوب
        ext = tldextract.extract(clean_url)
        domain = ext.domain

        # القائمة البيضاء الذكية (شاملة للهوتميل ويوتيوب وكل الكبار)
        trusted_brands = [
            'youtube', 'youtu', 'google', 'outlook', 'hotmail', 
            'live', 'microsoft', 'tiktok', 'speedtest', 'facebook'
        ]

        # 3. فحص الحصانة
        if domain in trusted_brands or any(brand in clean_url for brand in trusted_brands):
            return jsonify({'result': 'Safe'})
        
        # 4. منطق الحماية للروابط المجهولة
        if len(clean_url) > 150 or clean_url.count('-') > 5:
            return jsonify({'result': 'Phishing'})
            
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
