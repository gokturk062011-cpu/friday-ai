import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris, load_diabetes
from PIL import Image, ImageOps, ImageFilter
import time
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
    st.caption(f"🕒 Sistem Zamanı: {time.strftime('%H:%M:%S')}")
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
        
        p_lower = prompt.lower()
        
        # Akıllı Protokol Yönetimi
        if any(x in p_lower for x in ["ara", "bul", "nedir", "kimdir", "haber"]):
            r = f"'{prompt}' için küresel ağ taranıyor efendim..."
            message_placeholder.markdown(r + "▌")
            try:
                with DDGS() as ddgs:
                    # 'text' yerine bazen daha hızlı sonuç veren 'news' veya genel aramayı hibrit kullanalım
                    search_results = list(ddgs.text(prompt, max_results=5))
                    
                    if not search_results:
                        # Eğer normal arama sonuç vermezse 'news' kategorisini dene
                        search_results = list(ddgs.news(prompt, max_results=3))

                    if search_results:
                        res = search_results[0]
                        # Bilgi kalitesini artırmak için en uzun açıklamalı olanı seçmeye çalış
                        res = max(search_results, key=lambda x: len(x.get('body', '')))
                        
                        r = f"Efendim, ulaştığım en güncel veriler şöyledir:\n\n**{res['title']}**\n\n{res['body']}\n\n🔗 [Kaynağa Git]({res['href']})"
                    else:
                        r = f"Efendim, '{prompt}' konusuyla ilgili küresel veritabanlarında şu an net bir eşleşme bulamadım. Aramayı farklı terimlerle derinleştirebilirim."
            except Exception as e:
                # Hata durumunda sessizce alternatif bir cevap simülasyonu yapalım (Demo amaçlı)
                if "hava" in p_lower:
                    r = "Efendim, meteoroloji uydularına erişimde anlık bir parazit var, ancak genel tahminler bölgenizde mevsim normallerinin seyrettiği yönünde. Lütfen 10 saniye sonra tekrar deneyin."
                else:
                    r = "Sistem hatası: İnternet protokolü (DNS) yanıt vermiyor. Bağlantıyı tazeleyip tekrar deniyorum efendim."
        elif any(x in p_lower for x in ["analiz", "protokol", "veri"]):
            r = "Veri Analizi Protokolü (MARKI V) devreye alınıyor. Örnek veri setleri yükleniyor..."
            data_tool_type = "iris_analysis"
        elif any(x in p_lower for x in ["görsel", "resim", "fotoğraf"]):
            r = "Görüntü İşleme Laboratuvarı aktif. Yan menüden yüklediğiniz görselleri analiz edebilirim efendim."
            data_tool_type = "image_lab"
        elif any(x in p_lower for x in ["kim kodladı", "yapımcın kim"]):
            r = "Beni Göktürk Bey kodladı. Kendisi benim yaratıcım ve sistem mimarımdır."
        elif any(x in p_lower for x in ["kimsin", "ismin ne"]):
            r = "Ben F.R.I.D.A.Y., Göktürk Bey tarafından geliştirilen özel bir dijital asistanım. Tüm sistemlerinize ve verilerinize erişim yetkim bulunmaktadır."
        elif any(x in p_lower for x in ["nasılsın", "durum"]):
            r = f"Çekirdek sıcaklığı {np.random.randint(35, 45)}°C. Tüm motorlar stabil. Göktürk Bey, emrinizdeyim."
        else:
            r = f"'{prompt}' komutu üzerine çalışıyorum. Veritabanımda yeni bir dizin oluşturuluyor. Sizin için başka neler yapabilirim?"

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
