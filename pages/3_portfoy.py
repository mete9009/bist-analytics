import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.style import inject_css, sidebar_header, plotly_cfg, CARD, BORDER, TEXT1, TEXT2, TEXT3, BLUE, GREEN, RED, ORANGE, BG
from utils.data_loader import get_stock_data, get_bist_hisseler
from utils.db import (portfoyleri_getir, portfoy_olustur, portfoy_sil,
                      hisse_ekle, hisse_sat, portfoy_hisselerini_getir,
                      satis_gecmisini_getir)
from utils.session import auto_login

st.set_page_config(page_title="Portföy Takibi", page_icon="💼", layout="wide")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

# ── Giriş kontrolü ────────────────────────────────────────────
if not st.session_state.get("kullanici"):
    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
        padding:40px;text-align:center;margin-top:40px;">
        <div style="font-size:2.5rem;margin-bottom:16px;">🔐</div>
        <div style="color:{TEXT1};font-weight:700;font-size:1.1rem;margin-bottom:8px;">Giriş Gerekiyor</div>
        <div style="color:{TEXT3};font-size:0.88rem;">Bu sayfayı kullanmak için hesabınıza giriş yapmanız gerekiyor.</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/0_giris.py", label="Giriş Yap / Kayıt Ol", icon="🔐")
    st.stop()

kullanici    = st.session_state.kullanici
kullanici_id = kullanici["id"]
hisseler     = get_bist_hisseler()

# ── Başlık ────────────────────────────────────────────────────
st.markdown(f"""
<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
    <span style="font-size:1.6rem;">💼</span>
    <h1 style="margin:0;font-size:1.75rem;font-weight:700;color:{TEXT1};
        -webkit-text-fill-color:{TEXT1};background:none;">Portföy Takibi</h1>
</div>
""", unsafe_allow_html=True)

# ── Portföy Seçimi ────────────────────────────────────────────
portfoyler = portfoyleri_getir(kullanici_id)

if not portfoyler:
    st.info("Henüz portföyünüz yok.")
    portfoy_adi = st.text_input("İlk portföyünüzün adı")
    if st.button("Oluştur", type="primary"):
        portfoy_olustur(kullanici_id, portfoy_adi.strip() or "Portföyüm")
        st.rerun()
    st.stop()

col_p1, col_p2, col_p3 = st.columns([2, 2, 2])
with col_p1:
    st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Aktif Portföy</div>', unsafe_allow_html=True)
    secim_idx = st.selectbox("Portföy", range(len(portfoyler)),
                              format_func=lambda i: portfoyler[i]["ad"],
                              label_visibility="collapsed")
    aktif_portfoy = portfoyler[secim_idx]
with col_p2:
    st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Yeni Portföy Adı</div>', unsafe_allow_html=True)
    yeni_isim = st.text_input("Ad", placeholder="Örn: Temettü Portföyüm", label_visibility="collapsed")
with col_p3:
    st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">&nbsp;</div>', unsafe_allow_html=True)
    if st.button("＋ Portföy Oluştur", type="primary", use_container_width=True):
        isim = yeni_isim.strip()
        if not isim:
            st.warning("Ad boş olamaz.")
        elif isim in [p["ad"] for p in portfoyler]:
            st.warning("Bu isim zaten var.")
        else:
            portfoy_olustur(kullanici_id, isim)
            st.rerun()

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

# ── Hisse Ekle ────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;margin-bottom:16px;">
    <div style="color:{TEXT1};font-weight:700;font-size:0.95rem;margin-bottom:14px;">
        📥 {aktif_portfoy['ad']} — Hisse Ekle
    </div>
""", unsafe_allow_html=True)

with st.form("hisse_ekle", clear_on_submit=True):
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Hisse</div>', unsafe_allow_html=True)
        secilen = st.selectbox("Hisse", hisseler, label_visibility="collapsed")
    with c2:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Adet</div>', unsafe_allow_html=True)
        adet = st.number_input("Adet", min_value=1, value=100, step=1, label_visibility="collapsed")
    with c3:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Alış Fiyatı (₺)</div>', unsafe_allow_html=True)
        maliyet = st.number_input("Fiyat", min_value=0.01, value=10.0, step=0.01, format="%.2f", label_visibility="collapsed")
    with c4:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:500;margin-bottom:4px;">&nbsp;</div>', unsafe_allow_html=True)
        ekle_btn = st.form_submit_button("Ekle", type="primary", use_container_width=True)

    if ekle_btn:
        if hisse_ekle(aktif_portfoy["id"], secilen, adet, maliyet):
            st.success(f"{secilen} eklendi.")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ── Portföy Hesapla ───────────────────────────────────────────
hisseler_db = portfoy_hisselerini_getir(aktif_portfoy["id"])

if not hisseler_db:
    st.info("Bu portföyde hisse yok. Yukarıdan ekleyin.")
    st.stop()

satirlar = []
with st.spinner("Güncel fiyatlar çekiliyor..."):
    for satir in hisseler_db:
        df_h = get_stock_data(satir["hisse"], "5d")
        guncel = (float(df_h["Close"].squeeze().iloc[-1])
                  if df_h is not None and not df_h.empty
                  else float(satir["alis_fiyati"]))

        toplam_maliyet = float(satir["alis_fiyati"]) * float(satir["adet"])
        guncel_deger   = guncel * float(satir["adet"])
        kar_zarar      = guncel_deger - toplam_maliyet
        yuzde          = (kar_zarar / toplam_maliyet) * 100

        satirlar.append({
            "Hisse":         satir["hisse"],
            "Adet":          float(satir["adet"]),
            "Alış (₺)":     float(satir["alis_fiyati"]),
            "Güncel (₺)":   round(guncel, 2),
            "Maliyet (₺)":  round(toplam_maliyet, 2),
            "Güncel Değer": round(guncel_deger, 2),
            "K/Z (₺)":      round(kar_zarar, 2),
            "K/Z (%)":      round(yuzde, 2),
        })

sonuc = pd.DataFrame(satirlar)

# ── Özet Metrikler ────────────────────────────────────────────
toplam_maliyet_t = sonuc["Maliyet (₺)"].sum()
toplam_deger_t   = sonuc["Güncel Değer"].sum()
toplam_kz_t      = toplam_deger_t - toplam_maliyet_t
toplam_yuzde_t   = (toplam_kz_t / toplam_maliyet_t) * 100
kz_color         = GREEN if toplam_kz_t >= 0 else RED

satislar_db       = satis_gecmisini_getir(aktif_portfoy["id"])
toplam_gerceklesen = sum(float(s["kar_zarar"]) for s in satislar_db)
gkz_color         = GREEN if toplam_gerceklesen >= 0 else RED

st.markdown(f"""
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:12px;">
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 22px;">
        <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Toplam Maliyet</div>
        <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{toplam_maliyet_t:,.2f} ₺</div>
    </div>
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 22px;">
        <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Güncel Değer</div>
        <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{toplam_deger_t:,.2f} ₺</div>
    </div>
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 22px;">
        <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Açık K/Z</div>
        <div style="color:{kz_color};font-size:1.4rem;font-weight:700;">{toplam_kz_t:+,.2f} ₺</div>
        <div style="color:{kz_color};font-size:0.8rem;font-weight:500;">{toplam_yuzde_t:+.2f}%</div>
    </div>
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:20px 22px;">
        <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px;">Hisse Çeşidi</div>
        <div style="color:{TEXT1};font-size:1.4rem;font-weight:700;">{len(sonuc)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

if satislar_db:
    st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:16px 22px;margin-bottom:16px;display:flex;align-items:center;gap:32px;">
    <div>
        <div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Gerçekleşen K/Z</div>
        <div style="color:{gkz_color};font-size:1.4rem;font-weight:700;">{toplam_gerceklesen:+,.2f} ₺</div>
    </div>
    <div style="color:{TEXT3};font-size:0.82rem;">{len(satislar_db)} satış işlemi</div>
</div>
""", unsafe_allow_html=True)
else:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ── Portföy Tablosu ───────────────────────────────────────────
rows_html = ""
for _, row in sonuc.iterrows():
    kz_c = GREEN if row["K/Z (₺)"] >= 0 else RED
    sign = "+" if row["K/Z (%)"] >= 0 else ""
    rows_html += f"""
    <tr style="border-bottom:1px solid {BORDER};">
        <td style="padding:12px 20px;color:{BLUE};font-weight:600;font-size:0.88rem;">{row['Hisse']}</td>
        <td style="padding:12px 16px;text-align:right;color:{TEXT1};font-size:0.88rem;">{row['Adet']:,.0f}</td>
        <td style="padding:12px 16px;text-align:right;color:{TEXT2};font-size:0.88rem;">{row['Alış (₺)']:,.2f}</td>
        <td style="padding:12px 16px;text-align:right;color:{TEXT1};font-size:0.88rem;">{row['Güncel (₺)']:,.2f}</td>
        <td style="padding:12px 16px;text-align:right;color:{TEXT2};font-size:0.88rem;">{row['Maliyet (₺)']:,.2f}</td>
        <td style="padding:12px 16px;text-align:right;color:{TEXT1};font-size:0.88rem;">{row['Güncel Değer']:,.2f}</td>
        <td style="padding:12px 16px;text-align:right;color:{kz_c};font-weight:600;font-size:0.88rem;">{row['K/Z (₺)']:+,.2f}</td>
        <td style="padding:12px 20px;text-align:right;color:{kz_c};font-weight:600;font-size:0.88rem;">{sign}{row['K/Z (%)']:.2f}%</td>
    </tr>"""

st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;margin-bottom:16px;">
    <div style="display:flex;align-items:center;justify-content:space-between;
        padding:16px 20px;border-bottom:1px solid {BORDER};">
        <span style="color:{TEXT1};font-weight:700;font-size:0.95rem;">Portföy Detayı</span>
    </div>
    <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;">
    <thead>
    <tr style="border-bottom:1px solid {BORDER};">
        <th style="padding:10px 20px;text-align:left;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Hisse</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Adet</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Alış (₺)</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Güncel (₺)</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Maliyet (₺)</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Güncel Değer</th>
        <th style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">K/Z (₺)</th>
        <th style="padding:10px 20px;text-align:right;color:{TEXT2};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">K/Z (%)</th>
    </tr>
    </thead>
    <tbody>{rows_html}</tbody>
    </table></div>
</div>
""", unsafe_allow_html=True)

# ── Hisse Sat ─────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;margin-bottom:16px;">
    <div style="color:{TEXT1};font-weight:700;font-size:0.95rem;margin-bottom:14px;">
        💸 Hisse Sat
    </div>
""", unsafe_allow_html=True)

with st.form("hisse_sat_form", clear_on_submit=True):
    s1, s2, s3, s4 = st.columns([3, 2, 2, 1])
    with s1:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Hisse</div>', unsafe_allow_html=True)
        sat_hisse = st.selectbox("Sat Hisse", [s["hisse"] for s in hisseler_db], label_visibility="collapsed")
    with s2:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Adet</div>', unsafe_allow_html=True)
        sat_adet = st.number_input("Sat Adet", min_value=1, value=1, step=1, label_visibility="collapsed")
    with s3:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;">Satış Fiyatı (₺)</div>', unsafe_allow_html=True)
        sat_fiyat = st.number_input("Sat Fiyat", min_value=0.01, value=10.0, step=0.01, format="%.2f", label_visibility="collapsed")
    with s4:
        st.markdown(f'<div style="color:{TEXT3};font-size:0.68rem;font-weight:500;margin-bottom:4px;">&nbsp;</div>', unsafe_allow_html=True)
        sat_btn = st.form_submit_button("Sat", type="primary", use_container_width=True)

    if sat_btn:
        ok, msg = hisse_sat(aktif_portfoy["id"], sat_hisse, sat_adet, sat_fiyat)
        if ok:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

st.markdown("</div>", unsafe_allow_html=True)

# ── Satış Geçmişi ─────────────────────────────────────────────
if satislar_db:
    satis_rows_html = ""
    for s in satislar_db:
        kz = float(s["kar_zarar"])
        kz_c = GREEN if kz >= 0 else RED
        tarih = s["satis_tarihi"]
        tarih_str = tarih.strftime("%d.%m.%Y") if hasattr(tarih, "strftime") else str(tarih)[:10]
        satis_rows_html += f"""
        <tr style="border-bottom:1px solid {BORDER};">
            <td style="padding:10px 20px;color:{BLUE};font-weight:600;font-size:0.85rem;">{s['hisse']}</td>
            <td style="padding:10px 16px;text-align:right;color:{TEXT1};font-size:0.85rem;">{float(s['adet']):,.0f}</td>
            <td style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.85rem;">{float(s['alis_fiyati']):,.2f}</td>
            <td style="padding:10px 16px;text-align:right;color:{TEXT2};font-size:0.85rem;">{float(s['satis_fiyati']):,.2f}</td>
            <td style="padding:10px 16px;text-align:right;color:{kz_c};font-weight:600;font-size:0.85rem;">{kz:+,.2f} ₺</td>
            <td style="padding:10px 20px;text-align:right;color:{TEXT3};font-size:0.82rem;">{tarih_str}</td>
        </tr>"""

    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;overflow:hidden;margin-bottom:16px;">
        <div style="display:flex;align-items:center;justify-content:space-between;
            padding:16px 20px;border-bottom:1px solid {BORDER};">
            <span style="color:{TEXT1};font-weight:700;font-size:0.95rem;">📈 Satış Geçmişi</span>
            <span style="color:{gkz_color};font-weight:700;font-size:0.95rem;">Toplam: {toplam_gerceklesen:+,.2f} ₺</span>
        </div>
        <div style="overflow-x:auto;">
        <table style="width:100%;border-collapse:collapse;">
        <thead><tr style="border-bottom:1px solid {BORDER};">
            <th style="padding:8px 20px;text-align:left;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Hisse</th>
            <th style="padding:8px 16px;text-align:right;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Adet</th>
            <th style="padding:8px 16px;text-align:right;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Alış (₺)</th>
            <th style="padding:8px 16px;text-align:right;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Satış (₺)</th>
            <th style="padding:8px 16px;text-align:right;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">K/Z (₺)</th>
            <th style="padding:8px 20px;text-align:right;color:{TEXT2};font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:0.07em;">Tarih</th>
        </tr></thead>
        <tbody>{satis_rows_html}</tbody>
        </table></div>
    </div>
    """, unsafe_allow_html=True)

# ── Grafikler ─────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    fig_pie = go.Figure(go.Pie(
        labels=sonuc["Hisse"], values=sonuc["Güncel Değer"],
        hole=0.55,
        marker=dict(colors=["#3b82f6","#60a5fa","#93c5fd","#bfdbfe","#2563eb","#1d4ed8"]),
        textinfo="label+percent",
        textfont=dict(color=TEXT1, size=11),
    ))
    pie_layout = plotly_cfg(height=320)
    pie_layout["title"] = dict(
        text="Portföy Dağılımı",
        font=dict(color=TEXT1, size=14, family="Inter, sans-serif"),
        x=0.02
    )
    pie_layout["margin"] = dict(l=8, r=8, t=52, b=8)
    pie_layout["showlegend"] = False
    pie_layout["annotations"] = [dict(
        text=f"TOPLAM<br><b>{toplam_deger_t/1000:.1f}k ₺</b>",
        x=0.5, y=0.5, font=dict(size=12, color=TEXT1), showarrow=False
    )]
    fig_pie.update_layout(**pie_layout)
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

with col_b:
    bar_colors = [GREEN if v >= 0 else "#f97316" for v in sonuc["K/Z (%)"]]
    fig_bar = go.Figure(go.Bar(
        x=sonuc["Hisse"], y=sonuc["K/Z (%)"],
        marker_color=bar_colors,
        marker_opacity=0.85,
    ))
    bar_layout = plotly_cfg(height=320)
    bar_layout["title"] = dict(
        text="K/Z Karşılaştırması",
        font=dict(color=TEXT1, size=14, family="Inter, sans-serif"),
        x=0.02
    )
    bar_layout["margin"] = dict(l=8, r=8, t=52, b=8)
    fig_bar.update_layout(**bar_layout)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# ── Portföy Sil ───────────────────────────────────────────────
if len(portfoyler) > 1:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if st.button("❌ Bu Portföyü Tamamen Sil", type="secondary"):
        portfoy_sil(aktif_portfoy["id"])
        st.rerun()
