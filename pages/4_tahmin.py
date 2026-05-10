import streamlit as st
import numpy as np
import plotly.graph_objects as go
from utils.style import inject_css, sidebar_header, plotly_cfg, CARD, BORDER, TEXT1, TEXT2, TEXT3, BLUE, GREEN, RED, ORANGE
from utils.data_loader import get_stock_data, get_stock_info, get_bist_hisseler
from utils.indicators import calculate_rsi, calculate_macd, calculate_bollinger
from utils.session import auto_login

st.set_page_config(page_title="Değer Analizi", page_icon="⚖️", layout="wide")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

# ── Başlık ────────────────────────────────────────────────────
col_t, col_controls = st.columns([3, 3])
with col_t:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <span style="font-size:1.6rem;">⚖️</span>
        <div>
            <h1 style="margin:0;font-size:1.75rem;font-weight:700;color:{TEXT1};
                -webkit-text-fill-color:{TEXT1};background:none;">Temel &amp; Teknik Değer Analizi</h1>
            <p style="color:{TEXT3};font-size:0.82rem;margin:2px 0 0 0;">
                Kurumsal çapraz analiz ve adil değer metrikleri
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Uyarı banneri ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:rgba(245,158,11,0.07);border:1px solid rgba(245,158,11,0.25);
    border-radius:8px;padding:12px 16px;margin:12px 0 16px 0;
    display:flex;align-items:flex-start;gap:10px;">
    <span style="color:{ORANGE};font-size:1rem;flex-shrink:0;">⚠</span>
    <span style="color:#fcd34d;font-size:0.82rem;line-height:1.5;">
        Bu sayfa yalnızca analiz amaçlıdır. Gösterilen değerler kesin bilgi değildir ve yatırım tavsiyesi
        niteliği taşımaz. Tüm yatırım kararlarınızı kendi araştırmanıza ve bir finansal danışmana danışarak alınız.
    </span>
</div>
""", unsafe_allow_html=True)

# ── Seçiciler ─────────────────────────────────────────────────
hisseler = get_bist_hisseler()
c1, c2, c3 = st.columns([3, 2, 1])
with c1:
    ticker = st.selectbox("Hisse Seç", hisseler, index=hisseler.index("THYAO"))
with c2:
    period = st.selectbox("Teknik Analiz Periyodu", ["3mo","6mo","1y"], index=2,
                          format_func=lambda x: {"3mo":"3 Ay","6mo":"6 Ay","1y":"1 Yıl"}[x])
with c3:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    analiz_btn = st.button("Analiz Et", type="primary", use_container_width=True)

if not analiz_btn:
    st.info("Hisse seçip 'Analiz Et' butonuna basın.")
    st.stop()

with st.spinner("Veriler çekiliyor..."):
    info = get_stock_info(ticker)
    df   = get_stock_data(ticker, period)

if df is None or df.empty or not info:
    st.error("Veri alınamadı.")
    st.stop()

close     = df["Close"].squeeze()
son_fiyat = float(close.iloc[-1])

# ─────────────────────────────────────────────────────────────
# TEMEL ANALİZ
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin:24px 0 14px 0;">
    <span style="font-size:1.1rem;">ℹ️</span>
    <span style="color:{TEXT1};font-weight:700;font-size:1rem;">Temel Analiz — Adil Değer Hesabı</span>
</div>
""", unsafe_allow_html=True)

hbk    = info.get("trailingEps")
defter = info.get("bookValue")
buyume = info.get("earningsGrowth")
temttu = info.get("dividendRate")
beta   = info.get("beta", 1.0) or 1.0
risksiz_faiz = 0.45
prim   = 0.06

adil_degerler = {}

if hbk and defter and hbk > 0 and defter > 0:
    adil_degerler["Graham Sayısı"] = np.sqrt(22.5 * hbk * defter)

if hbk and buyume and hbk > 0:
    g = min(buyume * 100, 25)
    adil_degerler["Graham Büyüme"] = hbk * (8.5 + 2 * g) * 4.4 / max(risksiz_faiz * 100, 1)

if hbk and hbk > 0:
    adil_degerler["F/K Bazlı (Sektör Ort.)"] = hbk * 10

if defter and defter > 0:
    adil_degerler["PD/DD Bazlı (Sektör Ort.)"] = defter * 1.5

if temttu and temttu > 0 and buyume:
    g_oran = min(buyume, 0.08)
    r_oran = risksiz_faiz + beta * prim
    if r_oran > g_oran:
        adil_degerler["Temettü İskonto (DDM)"] = temttu / (r_oran - g_oran)

if adil_degerler:
    ort_adil = np.mean(list(adil_degerler.values()))
    sapma    = (son_fiyat - ort_adil) / ort_adil * 100

    if sapma < -15:
        temel_skor = 2
        temel_renk = GREEN
        temel_etiket = "Ucuz"
    elif sapma < 10:
        temel_skor = 1
        temel_renk = ORANGE
        temel_etiket = "Adil Değerde"
    else:
        temel_skor = 0
        temel_renk = RED
        temel_etiket = "Pahalı"

    # Temel metrikler kartı
    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
        padding:20px 24px;margin-bottom:12px;">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:24px;">
            <div>
                <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Güncel Fiyat</div>
                <div style="display:flex;align-items:center;gap:6px;">
                    <span style="width:8px;height:8px;border-radius:50%;background:{ORANGE};display:inline-block;"></span>
                    <span style="color:{TEXT1};font-size:1.5rem;font-weight:700;">{son_fiyat:.2f} ₺</span>
                </div>
            </div>
            <div>
                <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Ort. Adil Değer</div>
                <div style="color:{TEXT1};font-size:1.5rem;font-weight:700;">{ort_adil:.2f} ₺</div>
            </div>
            <div>
                <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Temel Durum</div>
                <div style="display:flex;align-items:center;gap:8px;">
                    <span style="width:8px;height:8px;border-radius:50%;background:{temel_renk};display:inline-block;"></span>
                    <span style="color:{temel_renk};font-size:1.1rem;font-weight:700;">{temel_etiket}</span>
                    <span style="color:{temel_renk};font-size:0.8rem;font-weight:500;">{sapma:+.1f}%</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bar grafik
    fig_temel = go.Figure()
    fig_temel.add_trace(go.Bar(
        x=list(adil_degerler.keys()),
        y=list(adil_degerler.values()),
        marker_color=BLUE, marker_opacity=0.8,
        text=[f"{v:.2f} ₺" for v in adil_degerler.values()],
        textposition="outside",
        textfont=dict(color=TEXT2, size=11),
    ))
    fig_temel.add_hline(y=son_fiyat, line_color=ORANGE, line_dash="dash", line_width=1.5,
                        annotation_text=f"Güncel: {son_fiyat:.2f} ₺",
                        annotation_font_color=ORANGE)
    layout_t = plotly_cfg(height=300)
    layout_t["yaxis"]["title"] = "Fiyat (₺)"
    fig_temel.update_layout(**layout_t)
    st.plotly_chart(fig_temel, use_container_width=True, config={"displayModeBar": False})

    with st.expander("Formül Bazlı Adil Değerler"):
        for isim, deger in adil_degerler.items():
            fark = (son_fiyat - deger) / deger * 100
            renk = GREEN if fark < -10 else (ORANGE if fark < 10 else RED)
            dot = "🟢" if fark < -10 else ("🟡" if fark < 10 else "🔴")
            st.markdown(f"**{isim}:** `{deger:.2f} ₺` &nbsp;&nbsp; {dot} Güncel fiyat `{fark:+.1f}%`")
else:
    st.warning("Yeterli temel veri bulunamadı.")
    temel_skor = 1
    ort_adil   = son_fiyat

# ─────────────────────────────────────────────────────────────
# TEKNİK ANALİZ
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin:24px 0 14px 0;">
    <span style="font-size:1.1rem;">📡</span>
    <span style="color:{TEXT1};font-weight:700;font-size:1rem;">Teknik Analiz — Sinyal Değerlendirmesi</span>
</div>
""", unsafe_allow_html=True)

rsi             = calculate_rsi(close, 14)
macd, signal, _ = calculate_macd(close)
upper, sma20, lower = calculate_bollinger(close, 20)
ma50  = close.rolling(50).mean()
ma200 = close.rolling(200).mean()

rsi_son  = float(rsi.iloc[-1])
macd_son = float(macd.iloc[-1])
sig_son  = float(signal.iloc[-1])
bb_b     = float((close.iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1] + 1e-9))

sinyaller = {}

if rsi_son < 30:
    sinyaller["RSI"] = (GREEN, "Aşırı Satım (Al)", 2, f"{rsi_son:.1f}")
elif rsi_son < 50:
    sinyaller["RSI"] = (ORANGE, "Nötr-Negatif", 1, f"+ {rsi_son:.1f}")
elif rsi_son < 70:
    sinyaller["RSI"] = (ORANGE, "Nötr-Pozitif", 1, f"{rsi_son:.1f}")
else:
    sinyaller["RSI"] = (RED, "Aşırı Alım (Sat)", 0, f"{rsi_son:.1f}")

if macd_son > sig_son:
    sinyaller["MACD"] = (GREEN, "Yükseliş", 2, f"{macd_son:.3f} > {sig_son:.3f}")
else:
    sinyaller["MACD"] = (RED, "Düşüş", 0, f"{macd_son:.3f} < {sig_son:.3f}")

if bb_b < 0.2:
    sinyaller["Bollinger"] = (GREEN, "Alt Bantta (Al)", 2, f"+ %B={bb_b:.2f}")
elif bb_b > 0.8:
    sinyaller["Bollinger"] = (RED, "Üst Bantta (Sat)", 0, f"%B={bb_b:.2f}")
else:
    sinyaller["Bollinger"] = (ORANGE, "Bant İçi", 1, f"+ %{bb_b*100:.2f}")

if ma50.notna().sum() >= 1 and ma200.notna().sum() >= 1:
    ma50_son  = float(ma50.dropna().iloc[-1])
    ma200_son = float(ma200.dropna().iloc[-1])
    if ma50_son > ma200_son:
        sinyaller["MA50/200"] = (GREEN, "Golden Cross", 2,
                                 f"MA50={ma50_son:.2f} > MA200={ma200_son:.2f}")
    else:
        sinyaller["MA50/200"] = (RED, "Death Cross", 0,
                                 f"MA50={ma50_son:.2f} < MA200={ma200_son:.2f}")

sma20_son = float(sma20.dropna().iloc[-1])
if son_fiyat > sma20_son:
    sinyaller["Fiyat/MA20"] = (GREEN, "MA20 Üstü", 2,
                               f"{son_fiyat:.2f} > {sma20_son:.2f}")
else:
    sinyaller["Fiyat/MA20"] = (RED, "MA20 Altı", 0,
                               f"{son_fiyat:.2f} < {sma20_son:.2f}")

# Sinyal kartları
cols = st.columns(len(sinyaller))
for i, (gosterge, (renk, durum, puan, detay)) in enumerate(sinyaller.items()):
    cols[i].markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-left:3px solid {renk};
        border-radius:8px;padding:16px;height:120px;">
        <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;
            text-transform:uppercase;letter-spacing:0.07em;margin-bottom:8px;">{gosterge}</div>
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;">
            <span style="width:6px;height:6px;border-radius:50%;background:{renk};
                display:inline-block;flex-shrink:0;"></span>
            <span style="color:{TEXT1};font-weight:600;font-size:0.85rem;">{durum}</span>
        </div>
        <div style="color:{TEXT3};font-size:0.75rem;">{detay}</div>
    </div>
    """, unsafe_allow_html=True)

# Teknik genel durum
teknik_puan = sum(v[2] for v in sinyaller.values())
teknik_max  = len(sinyaller) * 2
teknik_oran = teknik_puan / teknik_max

if teknik_oran >= 0.75:
    teknik_skor  = 2; teknik_renk = GREEN;  teknik_durum = "Güçlü Pozitif"
elif teknik_oran >= 0.50:
    teknik_skor  = 1; teknik_renk = ORANGE; teknik_durum = "Nötr"
else:
    teknik_skor  = 0; teknik_renk = RED;    teknik_durum = "Negatif"

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:8px;
    padding:14px 20px;margin-top:12px;display:flex;align-items:center;gap:16px;">
    <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;
        text-transform:uppercase;letter-spacing:0.07em;">Teknik Genel Durum</div>
    <div style="display:flex;align-items:center;gap:8px;">
        <span style="width:8px;height:8px;border-radius:50%;background:{teknik_renk};
            display:inline-block;"></span>
        <span style="color:{teknik_renk};font-weight:700;font-size:0.95rem;">{teknik_durum}</span>
        <span style="background:rgba(255,255,255,0.06);color:{TEXT2};font-size:0.75rem;
            font-weight:600;padding:2px 8px;border-radius:4px;">{teknik_puan}/{teknik_max} puan</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# KOMBİNE KARAR
# ─────────────────────────────────────────────────────────────
toplam = temel_skor + teknik_skor

if toplam >= 4:
    karar = "GÜÇLÜ AL";  karar_renk = GREEN;  karar_yildiz = "⭐⭐⭐⭐⭐"
elif toplam == 3:
    karar = "AL";        karar_renk = GREEN;  karar_yildiz = "⭐⭐⭐⭐"
elif toplam == 2:
    karar = "NÖTR / İZLE"; karar_renk = ORANGE; karar_yildiz = "⭐⭐⭐"
elif toplam == 1:
    karar = "SAT";       karar_renk = RED;    karar_yildiz = "⭐⭐"
else:
    karar = "GÜÇLÜ SAT"; karar_renk = RED;   karar_yildiz = "⭐"

st.markdown(f"""
<div style="display:flex;align-items:center;gap:8px;margin:24px 0 14px 0;">
    <span style="font-size:1.1rem;">🎯</span>
    <span style="color:{TEXT1};font-weight:700;font-size:1rem;">Genel Değerlendirme</span>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-left:4px solid {karar_renk};
    border-radius:12px;padding:24px;margin-bottom:12px;">
    <div style="display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:24px;align-items:center;">
        <div>
            <div style="color:{TEXT2};font-size:0.88rem;font-weight:500;margin-bottom:6px;">
                {ticker} — {son_fiyat:.2f} ₺
            </div>
            <div style="color:{TEXT3};font-size:0.8rem;margin-bottom:10px;">
                Adil Değer (Ort.): <span style="color:{TEXT2};font-weight:600;">{ort_adil:.2f} ₺</span>
            </div>
            <div style="color:{TEXT3};font-size:0.82rem;">
                Sonuç: <span style="color:{karar_renk};font-size:1.2rem;font-weight:800;">
                    {karar_yildiz} {karar}</span>
            </div>
        </div>
        <div style="text-align:center;">
            <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">Temel Analiz Skoru</div>
            <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{temel_skor}/2</div>
        </div>
        <div style="text-align:center;">
            <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">Teknik Analiz Skoru</div>
            <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{teknik_skor}/2</div>
        </div>
        <div style="text-align:center;">
            <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;margin-bottom:6px;">Toplam Skor</div>
            <div style="color:{karar_renk};font-size:1.4rem;font-weight:700;">{toplam}/4</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Alt uyarı
st.markdown(f"""
<div style="background:rgba(59,130,246,0.04);border:1px solid {BORDER};border-radius:8px;
    padding:14px 16px;display:flex;gap:10px;align-items:flex-start;">
    <span style="color:{BLUE};flex-shrink:0;">ℹ</span>
    <p style="color:{TEXT3};font-size:0.78rem;line-height:1.6;margin:0;">
        <strong style="color:{TEXT2};">Önemli Not:</strong> Bu sayfada gösterilen tüm değerler,
        formüllere ve geçmiş verilere dayanan analiz çıktılarıdır. Kesin bilgi niteliği taşımaz ve
        yatırım tavsiyesi değildir. Piyasa koşulları, haberler ve makroekonomik faktörler bu
        analizlere yansımayabilir. Yatırım kararlarınızı kendi araştırmanıza ve lisanslı bir
        finansal danışmana danışarak alınız.
    </p>
</div>
""", unsafe_allow_html=True)
