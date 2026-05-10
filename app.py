import streamlit as st
from utils.style import inject_css, sidebar_header, BLUE, CARD, BORDER, TEXT1, TEXT2, TEXT3, GREEN, RED
from utils.session import auto_login

st.set_page_config(page_title="BIST Analytics", page_icon="📈", layout="wide")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

# ── Hero ──────────────────────────────────────────────────────
st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #0d1b35 0%, #111827 60%, #0d1b35 100%);
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 48px 40px;
    margin-bottom: 28px;
    text-align: center;
    position: relative;
    overflow: hidden;
">
    <div style="position:absolute;top:0;left:0;right:0;bottom:0;opacity:0.04;
        background: repeating-linear-gradient(45deg,{BLUE},transparent 1px,transparent 20px);"></div>
    <div style="font-size:2.2rem;font-weight:800;color:{TEXT1};margin-bottom:12px;
        background:none;-webkit-text-fill-color:{TEXT1};text-align:center;">
        BIST Akıllı Hisse Analizi
    </div>
    <div style="color:{TEXT2};font-size:1rem;max-width:600px;margin:0 auto 28px auto;text-align:center;">
        Borsa İstanbul hisseleri için kurumsal düzeyde teknik analiz, temel analiz,
        portföy takibi ve değer analizi platformu.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Feature kartları ──────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

def feature_card(col, icon, title, desc):
    col.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
        padding:24px 20px;height:160px;transition:border-color 0.15s;">
        <div style="width:44px;height:44px;border-radius:10px;
            background:rgba(59,130,246,0.1);border:1px solid rgba(59,130,246,0.2);
            display:flex;align-items:center;justify-content:center;
            font-size:1.3rem;margin-bottom:14px;">{icon}</div>
        <div style="color:{TEXT1};font-weight:700;font-size:0.95rem;margin-bottom:6px;">{title}</div>
        <div style="color:{TEXT3};font-size:0.8rem;line-height:1.4;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

feature_card(c1, "📊", "Teknik Analiz",
             "RSI, MACD, Bollinger Bantları ve gelişmiş grafik araçları.")
feature_card(c2, "🏦", "Temel Analiz",
             "F/K, PD/DD, bilanço rasyoları ve finansal tablolar.")
feature_card(c3, "💼", "Portföy Takibi",
             "Gerçek zamanlı kâr/zarar durumu ve varlık dağılımı.")
feature_card(c4, "⚖️", "Değer Analizi",
             "Graham, DDM ve özel skorlama modelleri ile hedef fiyat.")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── Piyasa Trendleri ──────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;margin:8px 0 16px 0;">
    <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;
        text-transform:uppercase;letter-spacing:0.08em;">Piyasa Trendleri (BIST 30)</div>
</div>
""", unsafe_allow_html=True)

with st.spinner("Piyasa verileri yükleniyor..."):
    try:
        import yfinance as yf
        import pandas as pd

        @st.cache_data(ttl=300)
        def get_overview():
            bist30 = ["THYAO","EREGL","TUPRS","ASELS","KCHOL",
                      "GARAN","AKBNK","SAHOL","BIMAS","TCELL",
                      "SISE","FROTO","TOASO","ARCLK","PGSUS"]
            tickers_is = [f"{t}.IS" for t in bist30]
            try:
                df = yf.download(tickers_is, period="5d", auto_adjust=True, progress=False)
                close = df["Close"] if isinstance(df.columns, pd.MultiIndex) else df[["Close"]]
                rows = []
                for sym, sym_is in zip(bist30, tickers_is):
                    try:
                        prices = close[sym_is].dropna()
                        if len(prices) >= 2:
                            son  = float(prices.iloc[-1])
                            prev = float(prices.iloc[-2])
                            chg  = (son - prev) / prev * 100
                            rows.append({"Ticker": sym, "son": son, "chg": chg})
                    except Exception:
                        pass
                return rows
            except Exception:
                return []

        rows = get_overview()
    except Exception:
        rows = []

if rows:
    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;">
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
            padding:10px 20px;border-bottom:1px solid {BORDER};gap:8px;">
            <span style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Ticker</span>
            <span style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Son Fiyat</span>
            <span style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Günlük Değişim</span>
        </div>
    """, unsafe_allow_html=True)

    for i, r in enumerate(rows):
        chg_color = GREEN if r["chg"] >= 0 else RED
        sign = "+" if r["chg"] >= 0 else ""
        bg = "rgba(255,255,255,0.01)" if i % 2 == 0 else "transparent"
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;
            padding:12px 20px;background:{bg};border-bottom:1px solid {BORDER};gap:8px;
            transition:background 0.1s;" onmouseover="this.style.background='rgba(59,130,246,0.04)'"
            onmouseout="this.style.background='{bg}'">
            <span style="color:{BLUE};font-weight:600;font-size:0.88rem;">{r['Ticker']}</span>
            <span style="color:{TEXT1};font-weight:600;font-size:0.88rem;">{r['son']:,.2f} ₺</span>
            <span style="color:{chg_color};font-weight:600;font-size:0.88rem;">{sign}{r['chg']:.2f}%</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Piyasa verileri yüklenemedi. İnternet bağlantınızı veya yfinance'i kontrol edin.")

# ── Yasal uyarı ───────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin-top:32px;padding:16px;
    border-top:1px solid {BORDER};">
    <div style="color:#f59e0b;font-size:0.72rem;font-weight:600;
        text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">⚠ Yasal Uyarı</div>
    <div style="color:{TEXT3};font-size:0.78rem;max-width:640px;margin:0 auto;line-height:1.6;text-align:center;">
        Bu uygulama sadece analiz amaçlıdır. Verilen bilgiler yatırım tavsiyesi niteliği taşımaz.
        Yatırım kararlarınızı vermeden önce mutlaka lisanslı bir finansal danışmana danışınız.
    </div>
</div>
""", unsafe_allow_html=True)
