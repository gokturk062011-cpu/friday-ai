import datetime

def get_ai_greeting():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Günaydın! Yapay zeka sisteminiz güne hazır."
    elif 12 <= hour < 18:
        return "Tünaydın! Analizlere devam edelim mi?"
    elif 18 <= hour < 22:
        return "İyi akşamlar! Bugün harika veriler işledik."
    else:
        return "İyi geceler! Gece mesaisi için buradayım."

def calculate_text_complexity(text):
    words = text.split()
    if not words:
        return 0
    avg_len = sum(len(word) for word in words) / len(words)
    return round(avg_len, 2)
