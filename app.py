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
from utils import get_ai_greeting, calculate_text_complexity
from duckduckgo_search import DDGS

# Sayfa Yapılandırması
st.set_page_config(
    page_title="F.R.I.D.A.Y. | Digital Assistant",
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

# Sidebar Navigasyon (Minimalist)
st.sidebar.title("💠 F.R.I.D.A.Y. OS")
st.sidebar.markdown("*Central Intelligence Hub*")
st.sidebar.info("Sistem Durumu: OPTİMİZE EDİLDİ")

# Sohbet Geçmişi Başlatma
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Sistemler hazır. Ben F.R.I.D.A.Y., dijital asistanınız. Bugün hangi protokolü çalıştıralım, Göktürk Bey?"}]

if st.sidebar.button("Terminali Sıfırla"):
    st.session_state.messages = [{"role": "assistant", "content": "Tam sıfırlama yapıldı. Hazırım efendim."}]
    st.rerun()

# --- MERKEZİ TERMİNAL (CHAT) ---
st.title("💠 F.R.I.D.A.Y. Terminal")

# Sistem Bilgileri (Küçük ve şık)
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("🌐 Bağlantı: Global Cloud")
with col2:
    # Yerel saate göre düzeltme
    now = datetime.datetime.now()
    st.caption(f"🕒 Sistem Zamanı: {now.strftime('%H:%M:%S')}")
with col3:
    st.caption("🛡️ Güvenlik: Aktif")

st.markdown("---")

# Mesajları Görüntüle
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

# Dosya Yükleme (AI'nın her şeye erişimi için bir köprü)
with st.sidebar.expander("📁 Veri/Görsel Yükleme Paneli"):
    uploaded_file = st.file_uploader("F.R.I.D.A.Y.'a dosya verin:", type=["jpg", "png", "csv", "txt"])
    if uploaded_file:
        st.success(f"Analiz ediliyor: {uploaded_file.name}")

# Chat Girdisi
if prompt := st.chat_input("Bir komut giriniz (Örn: 'Analiz protokolünü başlat', 'Dosya özetle'...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        data_tool_type = None
        
        # Akıllı Protokol Yönetimi & Yazım Hatası Toleransı
        p_lower = prompt.lower()
        
        # Kelime bazlı esnek eşleşme (typo protection)
        def check(keywords):
            # Eğer anahtar kelimelerden biri kullanıcı girişinde geçiyorsa veya 
            # kullanıcı girişi çok yakınsa (basit typo kontrolü)
            for k in keywords:
                if k in p_lower: return True
            return False

        # --- ARAMA PROTOKOLÜ (HAVA DURUMU ÖNCELİKLİ) ---
        if check(["ara", "bul", "nedir", "kimdir", "haber", "hava", "sıcaklık"]):
            # Eğer hava durumu soruluyorsa sorguyu daha spesifik hale getir (MGM veya Accuweather önceliği için)
            search_query = prompt
            if check(["hava", "durumu", "derece"]):
                search_query = f"{prompt} güncel hava durumu tahmini mgm"
                
            r = f"'{prompt}' için küresel ağ taranıyor efendim..."
            message_placeholder.markdown(r + "▌")
            try:
                with DDGS() as ddgs:
                    # Spesifik konu araması
                    search_results = list(ddgs.text(search_query, max_results=5))
                    
                    if not search_results:
                        search_results = list(ddgs.news(prompt, max_results=3))

                    if search_results:
                        # Wikipedia dışı daha güncel siteleri önceliklendir (hava durumu vb için)
                        res = search_results[0]
                        for s in search_results:
                            # Hava durumu ise wikipedia istemiyoruz, daha güncel haber/hava sitesi istiyoruz
                            if check(["hava", "sicaklik"]):
                                if not "wikipedia" in s['href'].lower():
                                    res = s
                                    break
                            else:
                                if len(s.get('body', '')) > len(res.get('body', '')):
                                    res = s
                        
                        def get_content(item):
                            return item.get('body') or item.get('excerpt') or item.get('snippet') or ""
                        
                        r = f"Efendim, ulaştığım en güncel veriler şöyledir:\n\n**{res['title']}**\n\n{get_content(res)}\n\n🔗 [Kaynağa Git]({res.get('href') or res.get('url')})"
                    else:
                        r = f"Efendim, '{prompt}' konusuyla ilgili küresel veritabanlarında şu an net bir eşleşme bulamadım."
            except Exception as e:
                r = "Sistem hatası: İnternet protokolü (DNS) yanıt vermiyor. Lütfen tekrar deneyin."

        # --- DİĞER PROTOKOLLER (TYPO KORUMALI) ---
        elif check(["analiz", "anlat", "protokol", "veri", "tablo"]):
            r = "Veri Analizi Protokolü (MARKI V) devreye alınıyor. Örnek veri setleri yükleniyor..."
            data_tool_type = "iris_analysis"
        elif check(["görsel", "resim", "foto", "kamera", "lab"]):
            r = "Görüntü İşleme Laboratuvarı aktif. Yan menüden yüklediğiniz görselleri analiz edebilirim efendim."
            data_tool_type = "image_lab"
        elif check(["kodladı", "yaratıcın", "sahibin"]):
            r = "Beni Göktürk Bey kodladı. Kendisi benim yaratıcım ve sistem mimarımdır."
        elif check(["kimsin", "nesin", "adın"]):
            r = "Ben F.R.I.D.A.Y., Göktürk Bey tarafından geliştirilen özel bir dijital asistanım."
        elif check(["nasılsın", "durum", "stabil"]):
            r = f"Çekirdek sıcaklığı {np.random.randint(35, 45)}°C. Tüm motorlar stabil. Göktürk Bey, emrinizdeyim."
        else:
            r = f"'{prompt}' komutu üzerine çalışıyorum efendim. Sizin için başka neler yapabilirim?"

        # Yazma Efekti
        for chunk in r.split():
            full_response += chunk + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
        # Yanıtı ve tool bilgisini kaydet
        st.session_state.messages.append({
            "role": "assistant", 
            "content": full_response,
            "data_tool": data_tool_type
        })
    
# Footer
st.sidebar.markdown("---")
st.sidebar.write("OS Version: 2.0.4 | Powered by F.R.I.D.A.Y.")
