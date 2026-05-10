import mysql.connector
import hashlib
import json
import os
import streamlit as st

CONFIG_DOSYA = os.path.join(os.path.dirname(__file__), "..", "db_config.json")

def config_oku():
    if os.path.exists(CONFIG_DOSYA):
        with open(CONFIG_DOSYA, "r") as f:
            return json.load(f)
    return None

def config_kaydet(host, user, password, database):
    with open(CONFIG_DOSYA, "w") as f:
        json.dump({"host": host, "user": user, "password": password, "database": database}, f)

def baglanti():
    cfg = config_oku()
    if not cfg:
        raise ConnectionError("VT_YAPILANDIRILMADI")
    try:
        return mysql.connector.connect(**cfg)
    except mysql.connector.Error as e:
        if e.errno == 1045:
            raise ConnectionError("MySQL şifresi hatalı.")
        elif e.errno == 1049:
            raise ConnectionError(f"'{cfg['database']}' veritabanı bulunamadı.")
        elif e.errno == 2003:
            raise ConnectionError("MySQL sunucusuna bağlanılamadı. MySQL'in çalıştığından emin olun.")
        else:
            raise ConnectionError(f"Bağlantı hatası: {e.msg}")

def baglanti_test_et(host, user, password, database):
    try:
        con = mysql.connector.connect(host=host, user=user, password=password)
        cur = con.cursor()
        cur.execute(f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci")
        con.commit()
        con.close()
        return True, None
    except mysql.connector.Error as e:
        if e.errno == 1045:
            return False, "Kullanıcı adı veya şifre hatalı."
        elif e.errno == 2003:
            return False, "MySQL sunucusuna bağlanılamadı. MySQL'in çalıştığından emin olun."
        else:
            return False, str(e.msg)

def sifre_hashle(sifre: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        sifre.encode("utf-8"),
        b"bist_salt_2025",
        200_000
    ).hex()

def tablolari_olustur():
    try:
        con = baglanti()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kullanicilar (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                kullanici_adi   VARCHAR(50)  UNIQUE NOT NULL,
                email           VARCHAR(100) UNIQUE NOT NULL,
                sifre_hash      VARCHAR(255) NOT NULL,
                olusturma       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS portfoyler (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                kullanici_id    INT NOT NULL,
                ad              VARCHAR(100) NOT NULL,
                olusturma       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (kullanici_id) REFERENCES kullanicilar(id) ON DELETE CASCADE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS portfoy_hisseler (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                portfoy_id      INT NOT NULL,
                hisse           VARCHAR(20)    NOT NULL,
                adet            DECIMAL(12,2)  NOT NULL,
                alis_fiyati     DECIMAL(12,2)  NOT NULL,
                alis_tarihi     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (portfoy_id) REFERENCES portfoyler(id) ON DELETE CASCADE
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS satislar (
                id              INT AUTO_INCREMENT PRIMARY KEY,
                portfoy_id      INT NOT NULL,
                hisse           VARCHAR(20)    NOT NULL,
                adet            DECIMAL(12,2)  NOT NULL,
                alis_fiyati     DECIMAL(12,2)  NOT NULL,
                satis_fiyati    DECIMAL(12,2)  NOT NULL,
                kar_zarar       DECIMAL(12,2)  NOT NULL,
                satis_tarihi    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (portfoy_id) REFERENCES portfoyler(id) ON DELETE CASCADE
            )
        """)
        con.commit()
        con.close()
        return True, None
    except ConnectionError as e:
        return False, str(e)
    except Exception:
        return False, "Tablolar oluşturulamadı."

# ── Kullanıcı işlemleri ───────────────────────────────────────

def kullanici_kaydet(kullanici_adi, email, sifre):
    try:
        con = baglanti()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO kullanicilar (kullanici_adi, email, sifre_hash) VALUES (%s, %s, %s)",
            (kullanici_adi, email, sifre_hashle(sifre))
        )
        kullanici_id = cur.lastrowid
        cur.execute(
            "INSERT INTO portfoyler (kullanici_id, ad) VALUES (%s, %s)",
            (kullanici_id, "Ana Portföyüm")
        )
        con.commit()
        con.close()
        return True, "Kayıt başarılı."
    except mysql.connector.IntegrityError:
        return False, "Bu kullanıcı adı veya e-posta zaten kayıtlı."
    except ConnectionError as e:
        return False, str(e)
    except Exception:
        return False, "Kayıt sırasında bir hata oluştu."

def kullanici_giris(kullanici_adi, sifre):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM kullanicilar WHERE kullanici_adi=%s AND sifre_hash=%s",
            (kullanici_adi, sifre_hashle(sifre))
        )
        kullanici = cur.fetchone()
        con.close()
        return kullanici
    except Exception:
        return None

# ── Portföy işlemleri ─────────────────────────────────────────

def portfoyleri_getir(kullanici_id):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM portfoyler WHERE kullanici_id=%s ORDER BY olusturma", (kullanici_id,))
        sonuc = cur.fetchall()
        con.close()
        return sonuc
    except Exception:
        return []

def portfoy_olustur(kullanici_id, ad):
    try:
        con = baglanti()
        cur = con.cursor()
        cur.execute("INSERT INTO portfoyler (kullanici_id, ad) VALUES (%s, %s)", (kullanici_id, ad))
        con.commit()
        con.close()
        return True
    except Exception:
        return False

def portfoy_sil(portfoy_id):
    try:
        con = baglanti()
        cur = con.cursor()
        cur.execute("DELETE FROM portfoyler WHERE id=%s", (portfoy_id,))
        con.commit()
        con.close()
        return True
    except Exception:
        return False

def hisse_ekle(portfoy_id, hisse, adet, alis_fiyati):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM portfoy_hisseler WHERE portfoy_id=%s AND hisse=%s",
            (portfoy_id, hisse)
        )
        mevcut = cur.fetchone()
        if mevcut:
            yeni_adet    = float(mevcut["adet"]) + adet
            yeni_maliyet = (float(mevcut["alis_fiyati"]) * float(mevcut["adet"]) + alis_fiyati * adet) / yeni_adet
            cur.execute(
                "UPDATE portfoy_hisseler SET adet=%s, alis_fiyati=%s WHERE id=%s",
                (yeni_adet, round(yeni_maliyet, 2), mevcut["id"])
            )
        else:
            cur.execute(
                "INSERT INTO portfoy_hisseler (portfoy_id, hisse, adet, alis_fiyati) VALUES (%s,%s,%s,%s)",
                (portfoy_id, hisse, adet, alis_fiyati)
            )
        con.commit()
        con.close()
        return True
    except Exception:
        return False

def hisse_sil(portfoy_id, hisse):
    try:
        con = baglanti()
        cur = con.cursor()
        cur.execute("DELETE FROM portfoy_hisseler WHERE portfoy_id=%s AND hisse=%s", (portfoy_id, hisse))
        con.commit()
        con.close()
        return True
    except Exception:
        return False

def hisse_sat(portfoy_id, hisse, satis_adet, satis_fiyati):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM portfoy_hisseler WHERE portfoy_id=%s AND hisse=%s", (portfoy_id, hisse))
        mevcut = cur.fetchone()
        if not mevcut:
            con.close()
            return False, "Hisse portföyde bulunamadı."
        mevcut_adet = float(mevcut["adet"])
        if satis_adet > mevcut_adet:
            con.close()
            return False, f"Maksimum {mevcut_adet:.0f} adet satabilirsiniz."
        alis_fiyati = float(mevcut["alis_fiyati"])
        kar_zarar = (satis_fiyati - alis_fiyati) * satis_adet
        cur.execute(
            "INSERT INTO satislar (portfoy_id, hisse, adet, alis_fiyati, satis_fiyati, kar_zarar) VALUES (%s,%s,%s,%s,%s,%s)",
            (portfoy_id, hisse, satis_adet, alis_fiyati, satis_fiyati, round(kar_zarar, 2))
        )
        if satis_adet >= mevcut_adet:
            cur.execute("DELETE FROM portfoy_hisseler WHERE id=%s", (mevcut["id"],))
        else:
            cur.execute("UPDATE portfoy_hisseler SET adet=%s WHERE id=%s", (mevcut_adet - satis_adet, mevcut["id"]))
        con.commit()
        con.close()
        return True, f"Satış kaydedildi. Gerçekleşen K/Z: {kar_zarar:+.2f} ₺"
    except Exception as e:
        return False, str(e)

def satis_gecmisini_getir(portfoy_id):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM satislar WHERE portfoy_id=%s ORDER BY satis_tarihi DESC LIMIT 100",
            (portfoy_id,)
        )
        sonuc = cur.fetchall()
        con.close()
        return sonuc
    except Exception:
        return []

def portfoy_hisselerini_getir(portfoy_id):
    try:
        con = baglanti()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM portfoy_hisseler WHERE portfoy_id=%s ORDER BY alis_tarihi", (portfoy_id,))
        sonuc = cur.fetchall()
        con.close()
        return sonuc
    except Exception:
        return []
