# 💠 F.R.I.D.A.Y. OS (Digital Assistant)

Bu proje, Python'un en güçlü kütüphanelerini kullanarak oluşturulmuş, yüksek teknolojili bir dijital asistan ve veri bilimi paneline dönüştürülmüştür.

## 🚀 Özellikler
1.  **💬 AI Chatbot**: Sizinle Türkçe sohbet eden ve projeyi tanıtan etkileşimli asistan.
2.  **📊 Gelişmiş Makine Öğrenmesi (Sınıflandırma)**: Iris veri seti ile gerçek zamanlı çiçek türü tahmini.
2.  **Veri Analizi (Regresyon)**: Diyabet veri seti üzerinden görselleştirme ve tahmin simülasyonu.
3.  **Doğal Dil İşleme (NLP)**: Metin analizi, kelime sayımı ve temel duygu analizi.
4.  **Bilgisayarlı Görü (Computer Vision)**: Görsel yükleme, gri tonlama, kenar belirleme ve AI filtreleme.
5.  **Dinamik Görselleştirme**: Plotly ile etkileşimli grafikler.

---

## 🛠️ Nasıl Çalıştırılır? (Adım Adım)

Bu uygulamayı bilgisayarınızda çalıştırmak için şu adımları izleyin:

### 1. Dosya Yoluna Gidin
Terminalinizi (CMD veya PowerShell) açın ve projenin olduğu klasöre gidin:
```powershell
cd c:\Users\Gktrk\Desktop\pythongktrk
```

### 2. Gerekli Kütüphaneleri Yükleyin
Uygulamanın çalışması için gerekli olan paketleri şu komutla yükleyin:
```powershell
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
Her şey hazır olduğunda şu komutu çalıştırın:
```powershell
streamlit run app.py
```

### 4. Tarayıcıda Açın
Komutu çalıştırdıktan sonra otomatik olarak bir tarayıcı sekmesi açılacaktır. Eğer açılmazsa, terminalde yazan `Local URL` (genellikle `http://localhost:8501`) adresini kopyalayıp tarayıcınıza yapıştırın.

---

## 🌐 Uygulamayı Dünyaya Açma (Başkaları Nasıl Girer?)

Uygulamayı sadece kendi bilgisayarınızda değil, başkalarının da görmesini istiyorsanız şu yöntemleri kullanabilirsiniz:

### A. Yerel Ağ (Aynı Wi-Fi)
Uygulamayı başlattığınızda terminalde yazan **Network URL** adresini arkadaşınıza gönderin. Aynı Wi-Fi'ye bağlı olduğunuz sürece girebilir.

### B. Ngrok ile Geçici Paylaşım (Kolay)
1. `ngrok http 8501` komutunu kullanarak geçici bir internet linki oluşturun.
2. Oluşan adresi herkese gönderebilirsiniz.

### C. Streamlit Cloud (Kalıcı ve Ücretsiz)
1. Kodları bir **GitHub** deposuna yükleyin.
2. [Streamlit Cloud](https://share.streamlit.io/) üzerinden bu depoyu bağlayın.
3. Uygulamanız `adiniz.streamlit.app` şeklinde kalıcı olarak yayına alınacaktır.
