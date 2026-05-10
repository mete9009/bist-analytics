import streamlit as st
from utils.style import inject_css, sidebar_header, plotly_cfg, CARD, BORDER, TEXT1, TEXT2, TEXT3, BLUE, GREEN, RED, ORANGE
from utils.session import auto_login
from utils.data_loader import get_stock_data, get_bist_hisseler
from utils.indicators import calculate_rsi, calculate_macd, calculate_bollinger
from utils.charts import create_candlestick
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Teknik Analiz", page_icon="📊", layout="wide")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

hisseler = get_bist_hisseler()

# ── Başlık + Seçiciler ────────────────────────────────────────
col_title, col_ticker, col_period = st.columns([3, 2, 1])
with col_title:
    st.markdown(f"""
    <div style="margin-bottom:4px;">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:1.6rem;">📊</span>
            <div>
                <h1 style="margin:0;font-size:1.75rem;font-weight:700;color:{TEXT1};
                    -webkit-text-fill-color:{TEXT1};background:none;">Teknik Analiz</h1>
                <p style="color:{TEXT3};font-size:0.82rem;margin:2px 0 0 0;">
                    Gerçek zamanlı piyasa takibi ve gösterge analizi
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_ticker:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    ticker = st.selectbox("Hisse Seç", hisseler, index=hisseler.index("THYAO"), label_visibility="collapsed")

with col_period:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    period = st.selectbox("Periyot", ["1mo","3mo","6mo","1y","2y"], index=3,
                          format_func=lambda x: {"1mo":"1 Ay","3mo":"3 Ay","6mo":"6 Ay","1y":"1 Yıl","2y":"2 Yıl"}[x],
                          label_visibility="collapsed")

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Veri çek ─────────────────────────────────────────────────
with st.spinner("Veri çekiliyor..."):
    df = get_stock_data(ticker, period)

if df is None or df.empty:
    st.error(f"**{ticker}** için veri bulunamadı.")
    st.stop()

close  = df["Close"].squeeze()
rsi    = calculate_rsi(close)
macd, signal, histogram = calculate_macd(close)
upper, sma, lower = calculate_bollinger(close)

# ── Mum Grafiği ───────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:16px 20px;margin-bottom:4px;">
    <div style="color:{TEXT1};font-weight:700;font-size:0.95rem;margin-bottom:2px;">{ticker} Fiyat Grafiği</div>
    <div style="color:{TEXT3};font-size:0.78rem;">{ticker}.IS</div>
</div>
""", unsafe_allow_html=True)

fig_c = create_candlestick(df)
st.plotly_chart(fig_c, use_container_width=True, config={"displayModeBar": False})

# ── Bollinger ─────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
    padding:12px 20px 4px 20px;margin-bottom:0;">
    <span style="color:{TEXT1};font-weight:700;font-size:0.95rem;">Bollinger Bantları</span>
</div>
""", unsafe_allow_html=True)

cfg = plotly_cfg(height=280)
fig_bb = go.Figure()
fig_bb.add_trace(go.Scatter(x=df.index, y=lower, name="Alt Bant",
    line=dict(color="#334155", width=1, dash="dot"), showlegend=True))
fig_bb.add_trace(go.Scatter(x=df.index, y=sma,   name="Orta (SMA)",
    line=dict(color="#94a3b8", width=1.5), showlegend=True))
fig_bb.add_trace(go.Scatter(x=df.index, y=upper, name="Üst Bant",
    line=dict(color="#334155", width=1, dash="dot"),
    fill="tonexty", fillcolor="rgba(59,130,246,0.04)", showlegend=True))
fig_bb.add_trace(go.Scatter(x=df.index, y=close, name="Kapanış",
    line=dict(color=BLUE, width=1.5), showlegend=False))
fig_bb.update_layout(**cfg)
st.plotly_chart(fig_bb, use_container_width=True, config={"displayModeBar": False})

# ── RSI & MACD ────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
    padding:12px 20px 4px 20px;margin-bottom:0;">
    <span style="color:{TEXT1};font-weight:700;font-size:0.95rem;">RSI &amp; MACD</span>
</div>
""", unsafe_allow_html=True)

fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True,
                     subplot_titles=("RSI (14)", "MACD (12/26/9)"),
                     row_heights=[0.5, 0.5], vertical_spacing=0.1)

fig2.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI",
    line=dict(color=GREEN, width=1.5)), row=1, col=1)
fig2.add_hline(y=70, line_color="#ef4444", line_dash="dot", line_width=1, row=1, col=1)
fig2.add_hline(y=30, line_color=GREEN,     line_dash="dot", line_width=1, row=1, col=1)
fig2.add_hrect(y0=30, y1=70, fillcolor="rgba(59,130,246,0.03)", line_width=0, row=1, col=1)

bar_colors = [GREEN if v >= 0 else RED for v in histogram]
fig2.add_trace(go.Bar(x=df.index, y=histogram, name="Histogram",
    marker_color=bar_colors, opacity=0.6), row=2, col=1)
fig2.add_trace(go.Scatter(x=df.index, y=macd,   name="MACD",
    line=dict(color=BLUE,   width=1.5)), row=2, col=1)
fig2.add_trace(go.Scatter(x=df.index, y=signal, name="Sinyal",
    line=dict(color=ORANGE, width=1.5)), row=2, col=1)

layout2 = plotly_cfg(height=460)
layout2["yaxis2"] = dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=TEXT3), zeroline=False)
layout2["annotations"] = [
    dict(text="RSI (14)",     x=0, xref="paper", y=1.02,   yref="paper",
         font=dict(color=TEXT2, size=11), showarrow=False, xanchor="left"),
    dict(text="MACD (12/26/9)", x=0, xref="paper", y=0.46, yref="paper",
         font=dict(color=TEXT2, size=11), showarrow=False, xanchor="left"),
]
fig2.update_layout(**layout2)
st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# ── Son Değerler ──────────────────────────────────────────────
son   = float(close.iloc[-1])
prev  = float(close.iloc[-2])
degisim = (son - prev) / prev * 100
rsi_son   = float(rsi.iloc[-1])
macd_son  = float(macd.iloc[-1])
signal_son= float(signal.iloc[-1])

chg_color = GREEN if degisim >= 0 else RED
rsi_color = GREEN if rsi_son < 40 else (RED if rsi_son > 65 else ORANGE)

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 24px;margin-top:8px;">
    <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;text-transform:uppercase;
        letter-spacing:0.08em;margin-bottom:16px;">Son Değerler</div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:24px;">
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;font-weight:500;margin-bottom:4px;">Kapanış Fiyatı</div>
            <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{son:.2f} ₺</div>
            <div style="color:{chg_color};font-size:0.8rem;font-weight:500;">{degisim:+.2f}%</div>
        </div>
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;font-weight:500;margin-bottom:4px;">RSI (14)</div>
            <div style="color:{rsi_color};font-size:1.4rem;font-weight:700;">{rsi_son:.1f}</div>
            <div style="color:{TEXT3};font-size:0.78rem;">{'Aşırı Satım' if rsi_son<30 else ('Aşırı Alım' if rsi_son>70 else 'Nötr')}</div>
        </div>
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;font-weight:500;margin-bottom:4px;">MACD</div>
            <div style="color:{ORANGE};font-size:1.4rem;font-weight:700;">{macd_son:.3f}</div>
            <div style="color:{TEXT3};font-size:0.78rem;">{'Yükseliş' if macd_son > signal_son else 'Düşüş'}</div>
        </div>
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;font-weight:500;margin-bottom:4px;">Sinyal</div>
            <div style="color:{BLUE};font-size:1.4rem;font-weight:700;">{signal_son:.3f}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Gösterge Analizi ──────────────────────────────────────────
bb_upper_son = float(upper.iloc[-1])
bb_lower_son = float(lower.iloc[-1])

# RSI yorumu
if rsi_son < 30:
    rsi_tag, rsi_tc, rsi_yorum = "AŞIRI SATIM", GREEN, "Hisse son 14 günde sert düştü, alıcılar devreye girebilir."
elif rsi_son > 70:
    rsi_tag, rsi_tc, rsi_yorum = "AŞIRI ALIM", RED, "Hisse kısa sürede çok yükseldi, kar realizasyonu baskısı oluşabilir."
elif rsi_son < 45:
    rsi_tag, rsi_tc, rsi_yorum = "ZAYIF MOMENTUM", ORANGE, "Satış baskısı hafif ağır basıyor, trend henüz güçlenmiyor."
elif rsi_son > 55:
    rsi_tag, rsi_tc, rsi_yorum = "GÜÇLÜ MOMENTUM", GREEN, "Alıcılar kontrolde, yükseliş trendi devam edebilir."
else:
    rsi_tag, rsi_tc, rsi_yorum = "NÖTR", TEXT2, "Belirgin bir alış ya da satış baskısı yok, yön bekleniyor."

# MACD yorumu
hist_son = float(histogram.iloc[-1])
hist_prev = float(histogram.iloc[-2]) if len(histogram) > 1 else hist_son
if macd_son > signal_son and hist_son > hist_prev:
    macd_tag, macd_tc, macd_yorum = "YUKARI KESİŞİM ↑", GREEN, "MACD sinyal çizgisini yukarı kesti ve ivme artıyor — güçlü yükseliş sinyali."
elif macd_son > signal_son:
    macd_tag, macd_tc, macd_yorum = "POZİTİF BÖLGE", GREEN, "MACD sinyalin üzerinde ama ivme yavaşlıyor, takip et."
elif macd_son < signal_son and hist_son < hist_prev:
    macd_tag, macd_tc, macd_yorum = "AŞAĞI KESİŞİM ↓", RED, "MACD sinyal çizgisini aşağı kesti ve ivme artıyor — güçlü düşüş sinyali."
else:
    macd_tag, macd_tc, macd_yorum = "NEGATİF BÖLGE", RED, "MACD sinyalin altında, düşüş baskısı sürüyor."

# Bollinger yorumu
bb_range = max(bb_upper_son - bb_lower_son, 0.001)
bb_pct = (son - bb_lower_son) / bb_range * 100
if son > bb_upper_son:
    bb_tag, bb_tc, bb_yorum = "ÜST BAND ÜSTÜNDE", RED, "Fiyat Bollinger üst bandını aştı — aşırı uzama, geri çekilme olası."
elif son < bb_lower_son:
    bb_tag, bb_tc, bb_yorum = "ALT BAND ALTINDA", GREEN, "Fiyat alt bandın altında — tarihi olarak güçlü dönüş bölgesi."
elif bb_pct > 70:
    bb_tag, bb_tc, bb_yorum = f"ÜST YARIDA (%{bb_pct:.0f})", ORANGE, "Bant içinde üst yarıda seyrediyor, yükseliş ivmesi mevcut."
else:
    bb_tag, bb_tc, bb_yorum = f"ALT YARIDA (%{bb_pct:.0f})", ORANGE, "Bant içinde alt yarıda, konsolidasyon veya zayıf seyir."

# Genel sinyal skoru (3 göstergeden)
puan = 0
if rsi_son < 50: puan += 1
else: puan -= 1
if macd_son > signal_son: puan += 1
else: puan -= 1
if son < (bb_upper_son + bb_lower_son) / 2: puan += 1
else: puan -= 1

if puan >= 2:
    genel_tag, genel_col, genel_yorum = "AL", GREEN, "Göstergelerin çoğunluğu yükseliş yönünde."
elif puan <= -2:
    genel_tag, genel_col, genel_yorum = "SAT", RED, "Göstergelerin çoğunluğu düşüş yönünde."
else:
    genel_tag, genel_col, genel_yorum = "BEKLE", ORANGE, "Göstergeler karışık sinyal veriyor, netleşmeyi bekle."

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 24px;margin-top:12px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;">
        <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">
            Gösterge Analizi
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
            <span style="color:{TEXT3};font-size:0.78rem;">Genel Sinyal:</span>
            <span style="background:rgba(0,0,0,0.3);border:1px solid {genel_col};color:{genel_col};
                font-size:0.8rem;font-weight:700;padding:3px 12px;border-radius:20px;
                letter-spacing:0.06em;">{genel_tag}</span>
        </div>
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
        <div style="border:1px solid {BORDER};border-radius:10px;padding:16px 18px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                <span style="color:{TEXT2};font-size:0.8rem;font-weight:600;">RSI (14)</span>
                <span style="background:rgba(0,0,0,0.3);border:1px solid {rsi_tc};color:{rsi_tc};
                    font-size:0.68rem;font-weight:700;padding:2px 8px;border-radius:12px;">{rsi_tag}</span>
            </div>
            <div style="color:{TEXT3};font-size:0.72rem;margin-bottom:10px;line-height:1.5;">
                Son 14 günde fiyat hareketinin hız ve büyüklüğünü ölçer.
                0–100 arasında değer alır; <span style="color:{GREEN};">30 altı</span> aşırı satım,
                <span style="color:{RED};">70 üstü</span> aşırı alım bölgesidir.
            </div>
            <div style="color:{rsi_tc};font-size:0.8rem;font-weight:500;border-top:1px solid {BORDER};padding-top:10px;">
                {rsi_yorum}
            </div>
        </div>
        <div style="border:1px solid {BORDER};border-radius:10px;padding:16px 18px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                <span style="color:{TEXT2};font-size:0.8rem;font-weight:600;">MACD (12/26/9)</span>
                <span style="background:rgba(0,0,0,0.3);border:1px solid {macd_tc};color:{macd_tc};
                    font-size:0.68rem;font-weight:700;padding:2px 8px;border-radius:12px;">{macd_tag}</span>
            </div>
            <div style="color:{TEXT3};font-size:0.72rem;margin-bottom:10px;line-height:1.5;">
                İki üssel hareketli ortalama (12 ve 26 günlük) farkından üretilir.
                MACD sinyal çizgisini <span style="color:{GREEN};">yukarı</span> kestiğinde alış,
                <span style="color:{RED};">aşağı</span> kestiğinde satış sinyali olarak yorumlanır.
            </div>
            <div style="color:{macd_tc};font-size:0.8rem;font-weight:500;border-top:1px solid {BORDER};padding-top:10px;">
                {macd_yorum}
            </div>
        </div>
        <div style="border:1px solid {BORDER};border-radius:10px;padding:16px 18px;">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px;">
                <span style="color:{TEXT2};font-size:0.8rem;font-weight:600;">Bollinger Bantları</span>
                <span style="background:rgba(0,0,0,0.3);border:1px solid {bb_tc};color:{bb_tc};
                    font-size:0.68rem;font-weight:700;padding:2px 8px;border-radius:12px;">{bb_tag}</span>
            </div>
            <div style="color:{TEXT3};font-size:0.72rem;margin-bottom:10px;line-height:1.5;">
                20 günlük SMA etrafında ±2 standart sapma mesafesinde çizilen bantlardır.
                Bantlar <span style="color:{GREEN};">daraldığında</span> düşük volatilite,
                <span style="color:{RED};">genişlediğinde</span> yüksek volatilite sinyali verir.
            </div>
            <div style="color:{bb_tc};font-size:0.8rem;font-weight:500;border-top:1px solid {BORDER};padding-top:10px;">
                {bb_yorum}
            </div>
        </div>
    </div>
    <div style="color:{TEXT3};font-size:0.68rem;margin-top:14px;padding-top:12px;border-top:1px solid {BORDER};">
        ⚠ Teknik göstergeler geçmiş fiyat hareketine dayanır; yatırım tavsiyesi niteliği taşımaz.
    </div>
</div>
""", unsafe_allow_html=True)
