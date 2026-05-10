import json
import os
import streamlit as st

_SESSION_FILE = os.path.join(os.path.dirname(__file__), "..", ".session.json")


def session_kaydet(kullanici):
    data = {"id": kullanici["id"], "kullanici_adi": kullanici["kullanici_adi"]}
    with open(_SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)


def session_sil():
    if os.path.exists(_SESSION_FILE):
        os.remove(_SESSION_FILE)


def auto_login():
    """Her sayfa açılışında çağrılır; session yoksa dosyadan geri yükler."""
    if st.session_state.get("kullanici"):
        return
    if os.path.exists(_SESSION_FILE):
        try:
            with open(_SESSION_FILE, "r", encoding="utf-8") as f:
                kullanici = json.load(f)
            if kullanici.get("id") and kullanici.get("kullanici_adi"):
                st.session_state.kullanici = kullanici
        except Exception:
            session_sil()
