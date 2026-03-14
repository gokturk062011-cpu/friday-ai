import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris, load_diabetes
from PIL import Image, ImageOps, ImageFilter
import time
import datetime
import psutil
import pyttsx3
import threading
import wikipedia
import google.generativeai as genai
import os
from utils import get_ai_greeting, calculate_text_complexity
from duckduckgo_search import DDGS

# --- SES MOTORU (TTS) BAŞLATMA ---
def speak(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160) 
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass 
    threading.Thread(target=run_speech).start()

st.set_page_config(
    page_title="A.S.E.N.A. | Digital Assistant",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #00d2ff; color: #0e1117; font-weight: bold; transition: 0.3s; }
    .stButton>button:hover { background-color: #3182ce; color: white; box-shadow: 0 0 15px #00d2ff; }
    h1, h2, h3 { color: #00d2ff; font-family: 'Orbitron', sans-serif; }
    .reportview-container .main .block-container{ padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("💠 A.S.E.N.A. OS")
st.sidebar.markdown("*Central Intelligence Hub*")

# API Key Giriş Yeri
st.sidebar.markdown("### 🔑 Ana Çekirdek Bağlantısı")
api_key_input = st.sidebar.text_input("Gemini API Key:", type="password", help="A.S.E.N.A'nın derin zekaya ulaşması için Google Gemini API anahtarınızı girin.")

if api_key_input:
    os.environ["GEMINI_API_KEY"] = api_key_input
    st.sidebar.success("Çekirdek Aktif: Gemini-1.5")
else:
    st.sidebar.warning("Çekirdek Beklemede: Bağlantı Yok")

st.sidebar.info("Sistem Durumu: OPTİMİZE EDİLDİ")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler hazır. Ben A.S.E.N.A., dijital asistanınız. Bugün hangi protokolü çalıştıralım, Göktürk Bey?"}]

if st.sidebar.button("Terminali Sıfırla"):
    st.session_state.messages = [{"role": "assistant", "content": "Tam sıfırlama yapıldı. Hazırım efendim."}]
    st.rerun()

st.title("💠 A.S.E.N.A. Terminal")

col1, col2, col3 = st.columns(3)
with col1: st.caption("🌐 Bağlantı: Global Cloud")
with col2: 
    now = datetime.datetime.now()
    st.caption(f"🕒 Sistem Zamanı: {now.strftime('%H:%M:%S')}")
with col3: st.caption("🛡️ Güvenlik: Aktif")

st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

with st.sidebar.expander("📁 Veri/Görsel Yükleme Paneli"):
    uploaded_file = st.file_uploader("A.S.E.N.A.'ya dosya verin:", type=["jpg", "png", "csv", "txt"])
    if uploaded_file:
        st.success(f"Analiz ediliyor: {uploaded_file.name}")

if prompt := st.chat_input("Bir komut giriniz (Örn: 'Analiz protokolü', 'elon musk kimdir', 'nasılsın'...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        p_lower = prompt.lower()
        
        def check(keywords):
            for k in keywords:
                if k in p_lower: return True
            return False

        # --- ARAMA PROTOKOLÜ ---
        if check(["ara", "bul", "nedir", "kimdir", "haber", "hava", "sıcaklık"]):
            search_query = prompt.lower()
            clean_query = search_query.replace("kimdir", "").replace("nedir", "").replace("ara", "").replace("bul", "").strip()

            r = f"'{clean_query}' için veritabanları taranıyor efendim..."
            message_placeholder.markdown(r + "▌")
            
            is_info_query = check(["kimdir", "nedir"])
            try:
                if is_info_query and clean_query:
                    wikipedia.set_lang("tr") 
                    try:
                        wiki_summary = wikipedia.summary(clean_query, sentences=3)
                        r = f"Efendim, '{clean_query}' hakkında şu bilgilere ulaştım:\n\n> {wiki_summary}"
                        speak(f"Efendim, {clean_query} hakkında şu bilgileri buldum: {wiki_summary}"[:200]) 
                    except wikipedia.exceptions.DisambiguationError as e:
                        r = f"'{clean_query}' için birden fazla sonuç var (Örn: {', '.join(e.options[:3])}). Lütfen daha spesifik sorun."
                        speak("Bu isimde birden fazla kayıt buldum, lütfen detaylandırın.")
                    except wikipedia.exceptions.PageError:
                        r = f"Vikipedi'de '{clean_query}' hakkında bir kayıt bulamadım."
                else:
                    if check(["hava", "durumu", "derece"]):
                        search_query = f"{prompt} güncel hava durumu tahmini mgm"
                        
                    with DDGS() as ddgs:
                        search_results = list(ddgs.text(search_query, max_results=3))
                        if not search_results: search_results = list(ddgs.news(prompt, max_results=3))

                        if search_results:
                            best_content = search_results[0].get('body') or search_results[0].get('snippet') or ""
                            source_link = search_results[0].get('href') or search_results[0].get('url')
                            if best_content:
                                r = f"Ağ üzerinde şu güncel veriye ulaştım:\n\n> {best_content}\n\n🔗 [Kapsamlı Bilgi]({source_link})"
                                speak(f"Şu bilgileri buldum: {best_content[:150]}")
                            else: r = "Küresel ağda net bir bilgi fihristlenmemiş efendim."
                        else: r = "Bu konuyla ilgili ağda bir eşleşme bulamadım efendim."
            except Exception as e:
                r = "Sistem hatası: Arama düğümleri yanıt vermiyor."
                speak("İnternet bağlantısında bir sorun var efendim.")

        # --- BAZI SABİT KOMUTLAR ---
        elif check(["okur musun", "oku", "dosyayı anlat"]):
            if uploaded_file is not None and uploaded_file.name.endswith('.txt'):
                content = uploaded_file.getvalue().decode("utf-8")
                preview = content[:300] + "..." if len(content) > 300 else content
                r = f"Dosya okundu efendim. İçeriğin özeti şöyle:\n\n> {preview}"
                speak("Dosyayı okudum efendim.")
            else: r, speak_vol = "Geçerli bir metin dosyası bulamadım.", "Geçerli bir metin dosyası bulamadım."
        
        elif check(["nasılsın", "durum", "stabil"]):
            cpu = psutil.cpu_percent(interval=0.5)
            ram = psutil.virtual_memory().percent
            r = f"**Sistem Raporu:**\n- 🧠 İşlemci Yükü: **%{cpu}**\n- 💾 RAM: **%{ram}**\nMotorlar stabil. Göktürk Bey, emrinizdeyim."
            speak(f"Motorlar stabil efendim. İşlemci kullanımı yüzde {cpu}.")
            
        elif check(["selam", "merhaba", "hey"]):
            r = "Selamlar Göktürk Bey! Sistemlerim aktif ve emrinizdeyim. Size nasıl yardımcı olabilirim?"
            speak("Selamlar Göktürk Bey! Sistemlerim aktif.")

        # --- GEMINI ÇEKİRDEĞİNE BAĞLANMA ---
        else:
            api_key = os.environ.get("GEMINI_API_KEY", "")
            if not api_key:
                r = "Sizi anlıyorum Göktürk Bey, ancak şu an çok derin bir düşünme işlemi istiyorsunuz. Derin zeka çekirdeğim kapalı. Lütfen sol menüdeki 'Ana Çekirdek Bağlantısı' kısmına API Anahtarınızı giriniz."
                speak("Derin düşünme modülüm şu an kapalı efendim.")
            else:
                try:
                    r = f"Sistemleri tarıyorum..."
                    message_placeholder.markdown(r + "▌")
                    genai.configure(api_key=api_key)
                    sys_ins = "Senin adın A.S.E.N.A. Sen Göktürk tarafından kodlanmış ve yaratılmış elit bir yapay zeka asistanısın. Türkçe konuşuyorsun. Saygılı ve asil bir üslubun var. Karşındakine Göktürk Bey diye hitap et. Asla kendini 'Ben bir dil modeliyim' diyerek tanıtma. Doğrudan cevap ver, uzun felsefelerden kaçın."
                    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=sys_ins)
                    response = model.generate_content(prompt)
                    r = response.text
                    speak(r.split('.')[0]) # Sadece ilk cümleyi okut (çok uzun olmasın)
                except Exception as e:
                    r = f"Çekirdek Hatası (API Geçersiz veya İnternet Sorunu): {e}"
                    speak("Yapay zeka çekirdeğim hata verdi efendim.")

        for chunk in r.split():
            full_response += chunk + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
st.sidebar.markdown("---")
st.sidebar.write("OS Version: 3.1.0 (Gemini Core Active) | Powered by A.S.E.N.A.")

