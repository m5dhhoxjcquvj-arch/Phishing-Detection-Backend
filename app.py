import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "System is Online"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # قائمة الحماية الفورية
        safe_list = ['youtube', 'youtu', 'google', 'hotmail', 'outlook', 'microsoft', 'watch']
        
        if any(word in url for word in safe_list):
            return jsonify({'result': 'Safe'})
        
        if len(url) > 120:
            return jsonify({'result': 'Phishing'})
            
        return jsonify({'result': 'Safe'})
    except Exception as e:
        return jsonify({'result': 'Error'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
