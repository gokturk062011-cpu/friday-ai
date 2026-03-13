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

# Sidebar Navigasyon
st.sidebar.title("💠 F.R.I.D.A.Y. OS")
st.sidebar.markdown("*Female Replacement Intelligent Digital Assistant Youth*")
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Erişim Seviyesi:",
    ["💬 F.R.I.D.A.Y. Sohbet", "🏠 Ana Terminal", "📊 Veri Analizi: Sınıflandırma", "📈 Veri Analizi: Regresyon", "📝 NLP: Dil İşleme", "📷 Görsel Analiz Lab"],
    index=0
)

# --- ANA SAYFA ---
if page == "🏠 Ana Terminal":
    st.title("F.R.I.D.A.Y. Sistemine Bağlanıldı")
    st.subheader(get_ai_greeting())
    st.markdown("""
    Bu uygulama, modern yapay zeka tekniklerini tek bir çatı altında toplayan gelişmiş bir platformdur. 
    Aşağıdaki modülleri keşfedebilirsiniz:
    
    *   **Chatbot**: Sizinle sohbet eden ve sorularınızı yanıtlayan yapay zeka.
    *   **Sınıflandırma**: Verileri kategorilere ayırma (Örn: Çiçek türleri).
    *   **Regresyon**: Sayısal değer tahmin etme (Örn: Fiyat tahmini).
    *   **Metin Analizi**: Duygu analizi ve kelime istatistikleri.
    *   **Görüntü İşleme Lab**: Görsel veriler üzerinde AI filtreleme.
    """)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Model Doğruluğu", "98.5%", "+1.2%")
    col2.metric("İşlem Hızı", "12ms", "-2ms")
    col3.metric("Öğrenilen Veri", "1.2M", "+50k")

    st.subheader("Sistem Durumu")
    st.info("Tüm yapay zeka motorları aktif ve optimize edildi. Chatbot modülü çevrimiçi.")
    
# --- CHATBOT ---
elif page == "💬 F.R.I.D.A.Y. Sohbet":
    st.header("💬 F.R.I.D.A.Y. Dijital Asistan")
    st.write("Sistem çevrimiçi. Size nasıl yardımcı olabilirim, efendim?")

    # Sohbet Geçmişi Başlatma
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Sistemler hazır. Ben F.R.I.D.A.Y., dijital asistanınız. Bugün hangi protokolü çalıştıralım?"}]

    # Geçmişi temizle butonu
    if st.sidebar.button("Sohbet Geçmişini Sıfırla"):
        st.session_state.messages = [{"role": "assistant", "content": "Sohbet geçmişi temizlendi. Hazırım."}]
        st.rerun()

    # Geçmiş mesajları görüntüle
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcıdan girdi al
    if prompt := st.chat_input("Komutunuzu bekliyorum..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Gelişmiş Kişilik Mantığı
            p_lower = prompt.lower()
            if any(x in p_lower for x in ["merhaba", "selam", "hey"]):
                r = "Merhaba efendim. Tüm sistemler %100 kapasiteyle çalışıyor. Size nasıl yardımcı olabilirim?"
            elif any(x in p_lower for x in ["nasılsın", "durumun ne"]):
                r = "Çekirdek sıcaklığım normal, işlemci yüküm düşük. Sizin için hizmete hazırım."
            elif any(x in p_lower for x in ["kim kodladı", "yapımcın kim", "seni kim yarattı"]):
                r = "Beni Göktürk Bey kodladı. Kendisi benim yaratıcım ve sistem mimarımdır."
            elif any(x in p_lower for x in ["kimsin", "ismin ne"]):
                r = "Ben F.R.I.D.A.Y. (Female Replacement Intelligent Digital Assistant Youth). Göktürk Bey tarafından geliştirilen özel bir dijital asistanım."
            elif any(x in p_lower for x in ["hava", "saat"]):
                r = f"Şu anki sistem zamanı: {time.strftime('%H:%M:%S')}. Hava verilerine erişim protokolü henüz simülasyon aşamasında."
            elif any(x in p_lower for x in ["teşekkür", "sağol"]):
                r = "Rica ederim efendim. Protokollerim size yardımcı olmak için tasarlandı."
            elif any(x in p_lower for x in ["şaka", "komik"]):
                r = "Bir gün bir yapay zeka bara girmiş... Devamını getiremiyorum çünkü işlemcim mantık hatası verdi."
            else:
                r = f"'{prompt}' kodunu analiz ettim. Şu anki veritabanımda bu komutun tam karşılığı yok ancak üzerinde çalışabilirim. Diğer modülleri (Veri Analizi veya Görsel İşleme) denemek ister misiniz?"

            # Yazma efekti
            for chunk in r.split():
                full_response += chunk + " "
                time.sleep(0.04)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
# --- SINIFLANDIRMA LAB ---
elif page == "📊 ML Lab: Sınıflandırma":
    st.header("📊 Sınıflandırma (Classification) Modülü")
    st.write("Bu modül, ünlü Iris veri setini kullanarak çiçek türlerini tahmin eder.")
    
    # Veri Yükleme
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['target'] = iris.target
    
    with st.expander("Veri Setini İncele"):
        st.dataframe(df.head())

    # Model Eğitimi
    X = iris.data
    y = iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    
    st.sidebar.subheader("Model Parametreleri")
    n_estimators = st.sidebar.slider("Ağaç Sayısı (Estimators)", 10, 200, 100)
    
    # Kullanıcı Girdisi ile Tahmin
    st.subheader("Kendi Verinle Tahmin Yap")
    col1, col2, col3, col4 = st.columns(4)
    s_len = col1.number_input("Çanak Yaprak Uzunluğu", 4.0, 8.0, 5.4)
    s_wid = col2.number_input("Çanak Yaprak Genişliği", 2.0, 4.5, 3.9)
    p_len = col3.number_input("Taç Yaprak Uzunluğu", 1.0, 7.0, 1.7)
    p_wid = col4.number_input("Taç Yaprak Genişliği", 0.1, 2.5, 0.4)
    
    if st.button("Tür Tahmin Et"):
        prediction = clf.predict([[s_len, s_wid, p_len, p_wid]])
        st.success(f"Tahmin Edilen Tür: **{iris.target_names[prediction[0]].upper()}**")
        st.balloons()

# --- REGRESYON LAB ---
elif page == "📈 ML Lab: Tahmin (Regresyon)":
    st.header("📈 Sayısal Tahmin (Regression) Modülü")
    st.write("Veri setindeki değişkenlere dayanarak sürekli bir değer tahmin eder.")
    
    data = load_diabetes()
    df_reg = pd.DataFrame(data.data, columns=data.feature_names)
    
    st.subheader("Veri İlişkileri Analizi")
    fig = px.scatter(df_reg, x="bmi", y="s5", color="age", title="BMI - Kan Değeri İlişkisi")
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Bu model, hastaların diyabet gelişim değerlerini tahmin etmek için eğitilmiştir.")

# --- NLP LAB ---
elif page == "📝 NLP: Metin Analizi":
    st.header("📝 Doğal Dil İşleme (NLP)")
    text_input = st.text_area("Analiz edilecek metni buraya yazın:", "Bu yapay zeka harika çalışıyor! Çok mutluyum.")
    
    if st.button("Metni Analiz Et"):
        with st.spinner("Analiz ediliyor..."):
            time.sleep(1)
            word_count = len(text_input.split())
            char_count = len(text_input)
            
            # Simple Sentiment Logic (Mockup for Demo)
            positive_words = ["harika", "iyi", "mutlu", "başarılı", "süper", "güzel"]
            score = sum(1 for word in text_input.lower().split() if word in positive_words)
            
            st.subheader("Analiz Sonuçları")
            c1, c2, c3 = st.columns(3)
            c1.metric("Kelime Sayısı", word_count)
            c2.metric("Karakter Sayısı", char_count)
            c3.metric("Ort. Kelime Uzunluğu", calculate_text_complexity(text_input))
            
            if score > 0:
                st.success("Pozitif bir metin algılandı! 😊")
            else:
                st.warning("Metin nötr veya analiz edilemedi.")

# --- GÖRSEL İŞLEME LAB ---
elif page == "📷 Görsel İşleme Lab":
    st.header("📷 Görüntü Analizi ve Filtreleme")
    uploaded_file = st.file_uploader("Bir görsel yükle (PNG, JPG)", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Orijinal Görsel", use_column_width=True)
        
        filter_type = st.selectbox("Uygulanacak AI Filtresi:", ["Yok", "Gri Tonlama", "Kenar Belirleme", "Bulanıklaştırma"])
        
        if st.button("Filtreyi Uygula"):
            if filter_type == "Gri Tonlama":
                processed_img = ImageOps.grayscale(image)
            elif filter_type == "Kenar Belirleme":
                processed_img = image.filter(ImageFilter.FIND_EDGES)
            elif filter_type == "Bulanıklaştırma":
                processed_img = image.filter(ImageFilter.BLUR)
            else:
                processed_img = image
                
            st.image(processed_img, caption="İşlenmiş Görsel", use_column_width=True)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("OS Version: 2.0.4 | Powered by F.R.I.D.A.Y.")
