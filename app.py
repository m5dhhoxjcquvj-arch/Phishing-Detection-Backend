@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        url = str(data.get('url', '')).lower().strip()
        
        # 1. قائمة الحصانة (يوتيوب وجوجل وغيرهم)
        if any(word in url for word in ['youtube', 'youtu', 'watch', 'google', 'hotmail', 'outlook', 'mail']):
            return jsonify({'result': 'Safe'})

        # 2. إذا مو موقع مشهور، نخليه يفحص بالنموذج (Model)
        if model:
            features = np.array([[len(url)]]) # الفحص بناءً على الطول
            prediction = model.predict(features)
            result = "Phishing" if prediction[0] == 1 else "Safe"
        else:
            result = "Error: Model not loaded"
            
        return jsonify({'result': result})
    except:
        return jsonify({'result': 'Safe'})
