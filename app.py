from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# تحميل النموذج الحقيقي حقك
try:
    model = joblib.load('phishing_model.pkl')
    print("✅ Model Loaded Successfully")
except Exception as e:
    model = None
    print(f"❌ Error loading model: {e}")

@app.route('/')
def home():
    return "Phishing Detection API is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data.get('url', '')
    
    if model:
        # هنا الذكاء الاصطناعي يحلل طول الرابط وخصائصه
        # بنعطيه رقم تجريبي بناءً على طول النص (كمثال للربط)
        features = np.array([[len(url)]]) 
        prediction = model.predict(features)
        
        # إذا النتيجة 1 يعني phishing، وإذا 0 يعني Safe (حسب تدريبك)
        result = "Phishing" if prediction[0] == 1 else "Safe"
    else:
        result = "Error: Model not loaded"
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
