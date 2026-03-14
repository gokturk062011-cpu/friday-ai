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
from utils import get_ai_greeting, calculate_text_complexity
from duckduckgo_search import DDGS

# --- SES MOTORU (TTS) BAŞLATMA ---
def speak(text):
    def run_speech():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160) # Konuşma hızı
            engine.setProperty('volume', 1.0)
            engine.say(text)
            engine.runAndWait()
        except:
            pass 
    threading.Thread(target=run_speech).start()

# Sayfa Yapılandırması
st.set_page_config(
    page_title="A.S.E.N.A. | Digital Assistant",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #00d2ff;
        color: #0e1117;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #3182ce;
        color: white;
        box-shadow: 0 0 15px #00d2ff;
    }
    h1, h2, h3 {
        color: #00d2ff;
        font-family: 'Orbitron', sans-serif;
    }
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar Navigasyon
st.sidebar.title("💠 A.S.E.N.A. OS")
st.sidebar.markdown("*Central Intelligence Hub*")
st.sidebar.info("Sistem Durumu: OPTİMİZE EDİLDİ")

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler hazır. Ben A.S.E.N.A., dijital asistanınız. Bugün hangi protokolü çalıştıralım, Göktürk Bey?"}]

if st.sidebar.button("Terminali Sıfırla"):
    st.session_state.messages = [{"role": "assistant", "content": "Tam sıfırlama yapıldı. Hazırım efendim."}]
    st.rerun()

# --- MERKEZİ TERMİNAL (CHAT) ---
st.title("💠 A.S.E.N.A. Terminal")

col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌐 Bağlantı: Global Cloud")
with col2:
    now = datetime.datetime.now()
    st.caption(f"🕒 Sistem Zamanı: {now.strftime('%H:%M:%S')}")
with col3:
    st.caption("🛡️ Güvenlik: Aktif")

st.markdown("---")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data_tool" in message:
            if message["data_tool"] == "iris_analysis":
                iris = load_iris()
                df = pd.DataFrame(iris.data, columns=iris.feature_names)
                st.dataframe(df.head(5))
                st.line_chart(df.iloc[:, :2])
            elif message["data_tool"] == "image_lab":
                st.info("Görsel Analiz Modülü Aktif. Lütfen yukarıdaki dosyayı işleme koyun.")

with st.sidebar.expander("📁 Veri/Görsel Yükleme Paneli"):
    uploaded_file = st.file_uploader("A.S.E.N.A.'ya dosya verin:", type=["jpg", "png", "csv", "txt"])
    if uploaded_file:
        st.success(f"Analiz ediliyor: {uploaded_file.name}")

if prompt := st.chat_input("Bir komut giriniz (Örn: 'Analiz protokolünü başlat', 'Dosya özetle'...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        data_tool_type = None
        p_lower = prompt.lower()
        
        def check(keywords):
            for k in keywords:
                if k in p_lower: return True
            return False

        # --- ARAMA PROTOKOLÜ ---
        if check(["ara", "bul", "nedir", "kimdir", "haber", "hava", "sıcaklık"]):
            search_query = prompt
            if check(["hava", "durumu", "derece"]):
                search_query = f"{prompt} güncel hava durumu tahmini mgm"
                
            r = f"'{prompt}' için küresel ağ taranıyor efendim..."
            message_placeholder.markdown(r + "▌")
            try:
                with DDGS() as ddgs:
                    search_results = list(ddgs.text(search_query, max_results=5))
                    if not search_results:
                        search_results = list(ddgs.news(prompt, max_results=3))

                    if search_results:
                        best_content = ""
                        source_link = ""
                        
                        for res in search_results:
                            link = (res.get('href') or res.get('url') or "").lower()
                            if "wikipedia.org" in link:
                                best_content = res.get('body') or res.get('excerpt') or res.get('snippet') or ""
                                source_link = res.get('href') or res.get('url')
                                break
                        
                        if not best_content:
                            for res in search_results:
                                content = res.get('body') or res.get('excerpt') or res.get('snippet') or ""
                                if len(content) > 50:
                                    best_content = content
                                    source_link = res.get('href') or res.get('url')
                                    break
                                    
                        if best_content:
                            best_content = best_content.replace('...', '').strip()
                            r = f"Efendim, '{prompt}' hakkında şu bilgilere ulaştım:\n\n> {best_content}\n\n🔗 [Kapsamlı Bilgi İçin Tıklayın]({source_link})"
                            speak_text = f"Efendim, '{prompt}' hakkında şu bilgilere ulaştım. {best_content}"
                            speak(speak_text[:200]) 
                        else:
                             r = f"Efendim, '{prompt}' konusu hakkında net ve özet bir bilgi bulamadım."
                             speak(r)
                    else:
                        r = f"Efendim, '{prompt}' konusuyla ilgili küresel veritabanlarında şu an net bir eşleşme bulamadım."
                        speak(r)
            except Exception as e:
                r = "Sistem hatası: İnternet protokolü (DNS) yanıt vermiyor. Lütfen tekrar deneyin."
                speak("İnternet bağlantısında bir sorun var efendim.")

        # --- DİĞER PROTOKOLLER ---
        elif check(["okur musun", "oku", "dosyayı anlat", "dosyada ne var"]):
            if uploaded_file is not None:
                if uploaded_file.name.endswith('.txt'):
                    content = uploaded_file.getvalue().decode("utf-8")
                    preview = content[:300] + "..." if len(content) > 300 else content
                    r = f"Dosya okundu efendim. İçeriğin özeti şöyle:\n\n> {preview}"
                    speak(f"Dosyayı okudum efendim. İçinde şunlar yazıyor: {preview}")
                elif uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                    r = f"CSV dosyası analiz edildi. {df.shape[0]} satır ve {df.shape[1]} sütundan oluşuyor. Sütun isimleri: {', '.join(df.columns.tolist()[:5])}"
                    speak(f"Veri tablosunu inceledim. Toplam {df.shape[0]} satır veri içeriyor.")
                else:
                    r = "Bu dosya formatını henüz metin olarak okuyamıyorum efendim. Sadece TXT veya CSV verebilirsiniz."
                    speak(r)
            else:
                r = "Şu anda okuyabileceğim bir dosya yok efendim. Lütfen sol panelden bir dosya yükleyin."
                speak(r)
        
        elif check(["analiz", "anlat", "protokol", "veri", "tablo"]):
            r = "Veri Analizi Protokolü (MARKI V) devreye alınıyor. Örnek veri setleri yükleniyor..."
            speak("Veri analiz protokolü başlatılıyor.")
            data_tool_type = "iris_analysis"
        elif check(["görsel", "resim", "foto", "kamera", "lab"]):
            r = "Görüntü İşleme Laboratuvarı aktif. Yan menüden yüklediğiniz görselleri analiz edebilirim efendim."
            speak("Görüntü işleme modülü devrede.")
            data_tool_type = "image_lab"
        elif check(["kodladı", "yaratıcın", "sahibin"]):
            r = "Beni Göktürk Bey kodladı. Kendisi benim yaratıcım ve sistem mimarımdır."
            speak(r)
        elif check(["kimsin", "nesin", "adın"]):
            r = "Ben A.S.E.N.A., Göktürk Bey tarafından geliştirilen özel bir dijital asistanım."
            speak("Ben Asena. Sizin için geliştirilmiş dijital bir asistanım.")
        elif check(["nasılsın", "durum", "stabil"]):
            cpu = psutil.cpu_percent(interval=0.5)
            ram_percent = psutil.virtual_memory().percent
            ram_gb = round(psutil.virtual_memory().used / (1024**3), 1)
            
            r = f"**Sistem Raporu:**\n- 🧠 İşlemci Yükü: **%{cpu}**\n- 💾 RAM Kullanımı: **%{ram_percent}** ({ram_gb} GB)\n- 🌡️ Motorlar stabil. Göktürk Bey, emrinizdeyim."
            speak(f"Motorlar stabil efendim. İşlemci kullanımı yüzde {cpu}. RAM kullanımı yüzde {ram_percent}. Emrinizdeyim.")
        elif check(["selam", "merhaba", "günaydın", "iyi akşamlar", "hey"]):
            r = "Selamlar Göktürk Bey! Sistemlerim aktif ve emrinizdeyim. Size nasıl yardımcı olabilirim?"
            speak("Selamlar Göktürk Bey! Sistemlerim aktif. Size nasıl yardımcı olabilirim?")
        else:
            r = f"Özür dilerim Göktürk Bey, '{prompt}' komutunun karşılığını sistemimde bulamadım. İsterseniz bu konuyu internette arayabilirim, komudun başına 'ara' kelimesini eklemeniz yeterli."
            speak("Bu komutu anlayamadım efendim. İsterseniz sizin için internette arayabilirim.")

        for chunk in r.split():
            full_response += chunk + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "data_tool": data_tool_type
        })
    
st.sidebar.markdown("---")
st.sidebar.write("OS Version: 2.0.4 | Powered by A.S.E.N.A.")

