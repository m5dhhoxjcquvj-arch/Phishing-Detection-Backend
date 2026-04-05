def analyze_url(url):
    url = url.lower().strip()
    
    # قائمة الكلمات التي تعطي أماناً فورياً حتى لو الرابط ناقص
    # أضفنا كلمة 'watch' لأنها علامة يوتيوب المسجلة
    if any(word in url for word in ['youtube', 'youtu', 'google', 'hotmail', 'outlook', 'watch']):
        return "Safe"

    # إذا الرابط مجهول وفيه علامات مريبة
    if url.count('?') > 1 or len(url) > 100:
        return "Phishing"
        
    return "Safe"
