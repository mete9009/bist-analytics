import streamlit as st
from utils.db import (config_oku, config_kaydet,
                      tablolari_olustur, kullanici_kaydet, kullanici_giris)
from utils.style import inject_css, sidebar_header, CARD, BORDER, TEXT1, TEXT2, TEXT3, BLUE, GREEN
from utils.session import auto_login, session_kaydet, session_sil

st.set_page_config(page_title="Giriş / Kayıt", page_icon="🔐", layout="centered")
inject_css()
auto_login()
sidebar_header(st.session_state.get("kullanici"))

if "kullanici" not in st.session_state:
    st.session_state.kullanici = None

# ── Giriş yapılmışsa ─────────────────────────────────────────
if st.session_state.kullanici:
    ad = st.session_state.kullanici["kullanici_adi"]
    st.markdown(f"""
    <div style="background:{CARD};border:1px solid {BORDER};border-radius:12px;
        padding:32px;text-align:center;margin-top:20px;">
        <div style="font-size:2rem;margin-bottom:12px;">✅</div>
        <div style="color:{TEXT1};font-weight:700;font-size:1.1rem;margin-bottom:6px;">Hoş geldiniz, {ad}!</div>
        <div style="color:{TEXT3};font-size:0.88rem;margin-bottom:20px;">Sol menüden analiz sayfalarına geçebilirsiniz.</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("Çıkış Yap", type="secondary", use_container_width=True):
        session_sil()
        st.session_state.kullanici = None
        st.rerun()
    st.stop()

# ── Otomatik bağlantı ─────────────────────────────────────────
cfg = config_oku()
if not cfg:
    config_kaydet("localhost", "root", database="bist_analyzer", password="")

ok, hata = tablolari_olustur()
if not ok:
    st.error(f"Veritabanına bağlanılamadı: {hata}")
    st.stop()

# ── Giriş / Kayıt ────────────────────────────────────────────
st.markdown(f"""
<div style="text-align:center;margin:20px 0 24px 0;">
    <h1 style="margin:0;color:{TEXT1};-webkit-text-fill-color:{TEXT1};background:none;">BIST Analytics</h1>
    <p style="color:{TEXT3};font-size:0.88rem;margin-top:6px;">Hesabınıza giriş yapın veya yeni hesap oluşturun</p>
</div>
""", unsafe_allow_html=True)

tab_giris, tab_kayit = st.tabs(["Giriş Yap", "Hesap Oluştur"])

with tab_giris:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with st.form("giris_form"):
        kullanici_adi = st.text_input("Kullanıcı Adı")
        sifre         = st.text_input("Şifre", type="password")
        giris_btn     = st.form_submit_button("Giriş Yap", use_container_width=True, type="primary")

    if giris_btn:
        if not kullanici_adi or not sifre:
            st.warning("Kullanıcı adı ve şifre boş olamaz.")
        else:
            kullanici = kullanici_giris(kullanici_adi, sifre)
            if kullanici:
                st.session_state.kullanici = kullanici
                session_kaydet(kullanici)
                st.success(f"Hoş geldiniz, **{kullanici_adi}**!")
                st.rerun()
            else:
                st.error("Kullanıcı adı veya şifre hatalı.")

with tab_kayit:
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    with st.form("kayit_form"):
        yeni_kullanici = st.text_input("Kullanıcı Adı")
        yeni_email     = st.text_input("E-posta")
        yeni_sifre     = st.text_input("Şifre", type="password")
        yeni_sifre2    = st.text_input("Şifre Tekrar", type="password")
        kayit_btn      = st.form_submit_button("Hesap Oluştur", use_container_width=True, type="primary")

    if kayit_btn:
        if not yeni_kullanici or not yeni_email or not yeni_sifre:
            st.warning("Tüm alanları doldurun.")
        elif yeni_sifre != yeni_sifre2:
            st.error("Şifreler eşleşmiyor.")
        elif len(yeni_sifre) < 6:
            st.error("Şifre en az 6 karakter olmalı.")
        else:
            basarili, mesaj = kullanici_kaydet(yeni_kullanici, yeni_email, yeni_sifre)
            if basarili:
                st.success(f"{mesaj} Giriş yapabilirsiniz.")
            else:
                st.error(mesaj)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
