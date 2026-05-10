# BIST Analytics 📈

Borsa İstanbul hisseleri için teknik analiz, temel analiz, portföy takibi ve tahmin platformu.

## Özellikler

- **Teknik Analiz** — Mum grafiği, RSI, MACD, Bollinger Bantları ve gösterge yorumları
- **Temel Analiz** — F/K, PD/DD, EV/FAVÖK, kârlılık oranları ve değerleme yorumları
- **Portföy Takibi** — Gerçek zamanlı kâr/zarar, varlık dağılımı ve satış geçmişi
- **Tahmin** — Makine öğrenmesi destekli fiyat tahmini

## Kurulum

```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Not:** Portföy ve giriş özellikleri için yerel bir MySQL (XAMPP) bağlantısı gereklidir.

## Kullanılan Teknolojiler

- [Streamlit](https://streamlit.io)
- [yfinance](https://github.com/ranaroussi/yfinance)
- [Plotly](https://plotly.com)
- MySQL

## ⚠️ Yasal Uyarı

Bu uygulama **yalnızca bilgi ve analiz amaçlıdır**. Burada yer alan hiçbir içerik, grafik, gösterge veya sinyal **yatırım tavsiyesi niteliği taşımaz**. Geçmiş fiyat hareketleri gelecekteki performansın garantisi değildir. Yatırım kararı vermeden önce mutlaka lisanslı bir finansal danışmana başvurunuz. Uygulamayı kullananlar, bu uyarıyı okuduğunu ve kabul ettiğini beyan etmiş sayılır.
