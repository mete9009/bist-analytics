import streamlit as st
from utils.style import inject_css, sidebar_header, plotly_cfg, CARD, BORDER, TEXT1, TEXT2, TEXT3, BLUE, GREEN, RED, ORANGE
from utils.session import auto_login
from utils.data_loader import get_stock_info, get_stock_data, get_bist_hisseler
import plotly.graph_objects as go

st.set_page_config(page_title="Temel Analiz", page_icon="🏦", layout="wide")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

hisseler = get_bist_hisseler()

# ── Seçiciler ─────────────────────────────────────────────────
col_t, col_ticker, col_period = st.columns([3, 2, 1])
with col_t:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
        <span style="font-size:1.6rem;">🏦</span>
        <div>
            <h1 style="margin:0;font-size:1.75rem;font-weight:700;color:{TEXT1};
                -webkit-text-fill-color:{TEXT1};background:none;">Temel Analiz</h1>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_ticker:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    ticker = st.selectbox("Hisse", hisseler, index=hisseler.index("THYAO"), label_visibility="collapsed")
with col_period:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    period = st.selectbox("Periyot", ["1mo","3mo","6mo","1y","2y"], index=3,
                          format_func=lambda x: {"1mo":"1 Ay","3mo":"3 Ay","6mo":"6 Ay","1y":"1 Yıl","2y":"2 Yıl"}[x],
                          label_visibility="collapsed")

with st.spinner("Veriler yükleniyor..."):
    info = get_stock_info(ticker)
    df   = get_stock_data(ticker, period)

if not info or df is None or df.empty:
    st.error(f"**{ticker}** için veri bulunamadı.")
    st.stop()

close = df["Close"].squeeze()

# ── Şirket Bilgisi ────────────────────────────────────────────
isim    = info.get("longName", ticker)
sektor  = info.get("sector", "-")
endustri= info.get("industry", "-")

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 24px;margin-bottom:8px;">
    <div style="color:{TEXT1};font-size:0.68rem;font-weight:600;text-transform:uppercase;
        letter-spacing:0.08em;margin-bottom:14px;">Şirket Bilgisi</div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;margin-bottom:4px;">Şirket</div>
            <div style="color:{TEXT1};font-weight:600;font-size:0.9rem;">{isim}</div>
        </div>
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;margin-bottom:4px;">Sektör</div>
            <div style="color:{TEXT1};font-weight:600;font-size:0.9rem;">{sektor}</div>
        </div>
        <div>
            <div style="color:{TEXT1};font-size:0.72rem;margin-bottom:4px;">Endüstri</div>
            <div style="color:{TEXT1};font-weight:600;font-size:0.9rem;">{endustri}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if info.get("longBusinessSummary"):
    with st.expander("Şirket Açıklaması"):
        st.write(info["longBusinessSummary"])

# ── Yardımcı fonksiyonlar ─────────────────────────────────────
def fmt(val, milyar=True):
    if not isinstance(val, (int, float)):
        return "-"
    return f"{val/1e9:.2f} Mr ₺" if milyar else f"{val/1e6:.0f} Mn ₺"

def pct(val):
    if not isinstance(val, float):
        return "-"
    color = GREEN if val > 0 else RED
    return f'<span style="color:{color};font-weight:700;">%{val*100:.1f}</span>'

def num(val, decimals=2):
    if not isinstance(val, (int, float)):
        return "-"
    return f"{val:.{decimals}f}"

def metric_card_html(label, value, colored_val=None):
    val_html = colored_val if colored_val else f'<span style="color:{TEXT1};font-weight:700;font-size:1.4rem;">{value}</span>'
    return f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:10px;padding:18px 20px;">
        <div style="color:{TEXT3};font-size:0.72rem;font-weight:500;margin-bottom:8px;">{label}</div>
        <div style="font-size:1.4rem;font-weight:700;color:{TEXT1};">{value}</div>
    </div>"""

# ── Değerleme ─────────────────────────────────────────────────
st.markdown(f'<div style="color:{TEXT1};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin:20px 0 10px 0;">Değerleme</div>', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("F/K Oranı",   num(info.get("trailingPE")))
c2.metric("PD/DD Oranı", num(info.get("priceToBook")))
c3.metric("F/S Oranı",   num(info.get("priceToSalesTrailing12Months")))
c4.metric("EV/EBITDA",   num(info.get("enterpriseToEbitda")))

# ── Finansal Göstergeler ──────────────────────────────────────
st.markdown(f'<div style="color:{TEXT1};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin:20px 0 10px 0;">Finansal Göstergeler</div>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns(4)
f1.metric("Piyasa Değeri", fmt(info.get("marketCap")))
f2.metric("Ciro (TTM)",    fmt(info.get("totalRevenue")))

net_kar = info.get("netIncomeToCommon")
net_str = fmt(net_kar)
f3.metric("Net Kâr (TTM)", net_str)
f4.metric("FAVÖK",         fmt(info.get("ebitda")))

# ── Kârlılık ─────────────────────────────────────────────────
st.markdown(f'<div style="color:{TEXT1};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin:20px 0 10px 0;">Kârlılık &amp; Büyüme</div>', unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)

def pct_metric(val):
    if not isinstance(val, float): return "-"
    return f"%{val*100:.1f}"

k1.metric("Brüt Kâr Marjı",  pct_metric(info.get("grossMargins")))
k2.metric("Net Kâr Marjı",   pct_metric(info.get("profitMargins")))
k3.metric("Öz Kaynak Kârl.", pct_metric(info.get("returnOnEquity")))
k4.metric("Aktif Kârl.",     pct_metric(info.get("returnOnAssets")))

# ── Fiyat Bilgisi ─────────────────────────────────────────────
st.markdown(f'<div style="color:{TEXT1};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin:20px 0 10px 0;">Fiyat Bilgisi</div>', unsafe_allow_html=True)
p1, p2, p3, p4 = st.columns(4)
son_kapanis = float(close.iloc[-1])
prev_kapanis = float(close.iloc[-2]) if len(close) > 1 else son_kapanis
degisim = (son_kapanis - prev_kapanis) / prev_kapanis * 100

p1.metric("Son Kapanış",   f"{son_kapanis:.2f} ₺", f"{degisim:+.1f}% bugün")
p2.metric("52H En Yüksek", str(info.get("fiftyTwoWeekHigh", "-")))
p3.metric("52H En Düşük",  str(info.get("fiftyTwoWeekLow", "-")))
p4.metric("Temettü Verimi", pct_metric(info.get("dividendYield")))

# ── Fiyat Grafiği ─────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
    padding:16px 20px 4px 20px;margin-top:8px;">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;">
        <span style="color:{TEXT1};font-weight:700;font-size:0.95rem;">Fiyat Geçmişi</span>
        <div style="display:flex;gap:4px;">
            <span style="color:{GREEN};font-size:1.1rem;font-weight:700;">{son_kapanis:.2f}</span>
            <span style="color:{GREEN if degisim>=0 else RED};font-size:0.8rem;font-weight:500;
                padding:2px 6px;background:rgba(16,185,129,0.1);border-radius:4px;align-self:center;">
                {degisim:+.1f}% bugün</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

cfg = plotly_cfg(height=300)
fig = go.Figure()
fig.add_trace(go.Bar(
    x=df.index, y=close,
    name="Kapanış",
    marker_color=BLUE,
    marker_opacity=0.7,
))
fig.update_layout(**cfg)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ── Temel Gösterge Analizi ────────────────────────────────────
def oran_yorum(label, deger, aciklama, esikler):
    """
    esikler: [(ust_sinir, renk, etiket), ..., (None, renk, etiket)]
    """
    if not isinstance(deger, (int, float)):
        return None
    for sinir, renk, etiket in esikler:
        if sinir is None or deger < sinir:
            return (label, deger, renk, etiket, aciklama)
    return None

gosterge_kartlari = []

fk = info.get("trailingPE")
g = oran_yorum("F/K Oranı", fk,
    "Fiyat / Kazanç oranı. Yatırımcının 1 liralık kâr için kaç lira ödediğini gösterir. "
    "Düşük F/K ucuz, yüksek F/K pahalı hisseye işaret edebilir.",
    [(8, GREEN, "UCUZ"), (15, GREEN, "MAKUL"), (25, ORANGE, "YÜKSEKçE"), (None, RED, "PAHALI")])
if g: gosterge_kartlari.append(g)

pddd = info.get("priceToBook")
g = oran_yorum("PD/DD Oranı", pddd,
    "Piyasa Değeri / Defter Değeri. Şirketin piyasa değerinin öz kaynağına oranıdır. "
    "1'in altı varlık değerinin altında işlem görüldüğüne işaret edebilir.",
    [(1, GREEN, "DEĞER ALTI"), (2, GREEN, "UYGUN"), (4, ORANGE, "PRİMLİ"), (None, RED, "AŞIRI PRİMLİ")])
if g: gosterge_kartlari.append(g)

net_marj = info.get("profitMargins")
g = oran_yorum("Net Kâr Marjı", net_marj,
    "Net kârın ciroya oranı. Şirketin her 100 liralık satıştan ne kadar net kâr ettiğini gösterir. "
    "Yüksek marj operasyonel verimliliğe işaret eder.",
    [(0.0, RED, "ZARAR"), (0.05, ORANGE, "ZAYIF"), (0.15, GREEN, "ORTA"), (None, GREEN, "GÜÇLÜ")])
if g: gosterge_kartlari.append(g)

roe = info.get("returnOnEquity")
g = oran_yorum("Öz Kaynak Kârl. (ROE)", roe,
    "Net kârın öz kaynağa oranı. Şirketin hissedar sermayesini ne kadar verimli kullandığını ölçer. "
    "BIST'te %15 üstü güçlü kabul edilir.",
    [(0.0, RED, "ZARAR"), (0.08, ORANGE, "DÜŞÜK"), (0.15, ORANGE, "ORTA"), (None, GREEN, "YÜKSEK")])
if g: gosterge_kartlari.append(g)

ev_ebitda = info.get("enterpriseToEbitda")
g = oran_yorum("EV/FAVÖK", ev_ebitda,
    "Firma Değeri / FAVÖK. Borçlar dahil şirketin kaç yıllık FAVÖK'üne eşdeğer fiyatlandığını gösterir. "
    "Sektörden bağımsız karşılaştırma için idealdir.",
    [(5, GREEN, "UCUZ"), (10, GREEN, "MAKUL"), (15, ORANGE, "YÜKSEKçE"), (None, RED, "PAHALI")])
if g: gosterge_kartlari.append(g)

fs = info.get("priceToSalesTrailing12Months")
g = oran_yorum("F/S Oranı", fs,
    "Fiyat / Satış oranı. Kârsız ya da düşük kârlı şirketleri değerlemek için kullanılır. "
    "1'in altı genellikle ucuz sayılır.",
    [(1, GREEN, "UCUZ"), (3, GREEN, "MAKUL"), (6, ORANGE, "YÜKSEKçE"), (None, RED, "PAHALI")])
if g: gosterge_kartlari.append(g)

if gosterge_kartlari:
    st.markdown(f"""
    <div style="color:{TEXT3};font-size:0.72rem;font-weight:600;text-transform:uppercase;
        letter-spacing:0.08em;margin:24px 0 12px 0;">Temel Gösterge Analizi</div>
    """, unsafe_allow_html=True)

    for i in range(0, len(gosterge_kartlari), 2):
        grup = gosterge_kartlari[i:i+2]
        cols = st.columns(len(grup))
        for col, (label, deger, renk, etiket, aciklama) in zip(cols, grup):
            deger_str = f"%{deger*100:.1f}" if deger < 5 else f"{deger:.2f}"
            col.markdown(f"""
            <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;height:100%;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px;">
                    <span style="color:{TEXT1};font-size:0.85rem;font-weight:600;">{label}</span>
                    <span style="background:rgba(0,0,0,0.3);border:1px solid {renk};color:{renk};
                        font-size:0.68rem;font-weight:700;padding:2px 10px;border-radius:12px;">{etiket}</span>
                </div>
                <div style="color:{renk};font-size:1.6rem;font-weight:700;margin-bottom:10px;">{deger_str}</div>
                <div style="color:{TEXT3};font-size:0.75rem;line-height:1.55;">{aciklama}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="color:{TEXT3};font-size:0.68rem;padding:12px 16px;border:1px solid {BORDER};
        border-radius:8px;margin-top:4px;">
        ⚠ Oranlar yalnızca yfinance verilerine dayalıdır. Sektör ortalamaları ve makroekonomik koşullar
        dikkate alınmadan tek başına yatırım kararı vermek için kullanılmamalıdır.
    </div>
    """, unsafe_allow_html=True)
