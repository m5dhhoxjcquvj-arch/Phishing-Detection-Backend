import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Final Guard is Online!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # القائمة البيضاء - فحص مباشر بالكلمة (أضمن شي في العالم)
        safe_list = ['youtube', 'youtu.be', 'google', 'hotmail', 'outlook', 'live', 'tiktok', 'speedtest']
        
        if any(word in url for word in safe_list):
            return jsonify({'result': 'Safe'})
        
        # فحص الروابط الطويلة جداً (بدون المواقع الموثوقة)
        if len(url) > 150:
            return jsonify({'result': 'Phishing'})
            
        return jsonify({'result': 'Safe'})

    except Exception as e:
        return jsonify({'result': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
