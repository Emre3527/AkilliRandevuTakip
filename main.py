import streamlit as st
from services.veri_yonetimi import oku, yaz
from services.sistem import hasta_bul, veteriner_bul, kullanici_giris, kullanici_kaydet
from models.randevu import Randevu
from models.tedavi import Tedavi

st.set_page_config(page_title="Akıllı Randevu ve Tedavi Sistemi", layout="centered")
st.title("🔬 Akıllı Randevu ve Tedavi Takip Sistemi")

# Kayıt bölümü
st.sidebar.subheader("🆕 Yeni Kayıt")
rol_k = st.sidebar.selectbox("Rol", ["Hasta", "Veteriner"])
id_k = st.sidebar.text_input("Yeni Kullanıcı ID")
ad_k = st.sidebar.text_input("Ad")
soyad_k = st.sidebar.text_input("Soyad")
ekstra_k = st.sidebar.text_input("TC No" if rol_k == "Hasta" else "Branş")

if st.sidebar.button("Kayıt Ol"):
    ekstra_dict = {"tc": ekstra_k} if rol_k == "Hasta" else {"brans": ekstra_k}
    if kullanici_kaydet(rol_k, id_k, ad_k, soyad_k, ekstra_dict):
        st.sidebar.success("Kayıt başarılı! Giriş yapabilirsiniz.")
    else:
        st.sidebar.error("Bu ID ile kayıtlı kullanıcı zaten var.")

# Giriş bölümü
st.sidebar.subheader("🔐 Giriş Yap")
rol = st.sidebar.selectbox("Giriş Rolü", ["Hasta", "Veteriner"])
kullanici_id = st.sidebar.text_input("Kullanıcı ID")

if st.sidebar.button("Giriş"):
    if rol == "Hasta":
        hasta = hasta_bul(kullanici_id)
        if hasta:
            st.success(f"Hoşgeldiniz, {hasta.tam_ad()}")
            st.subheader("📅 Randevu Oluştur")
            veriler = oku("data/kullanicilar.json")
            vet_ids = [v["id"] for v in veriler if v["rol"] == "Veteriner"]
            vet_id = st.selectbox("Veteriner Seçin", vet_ids)
            tarih = st.date_input("Tarih")
            if st.button("Randevu Al"):
                yeni = Randevu(hasta.id, vet_id, str(tarih)).__dict__
                veri = oku("data/randevular.json")
                veri.append(yeni)
                yaz("data/randevular.json", veri)
                st.success("Randevu alındı.")
            st.subheader("📋 Randevularım")
            for r in oku("data/randevular.json"):
                if r["hasta_id"] == hasta.id:
                    v = veteriner_bul(r["veteriner_id"])
                    st.info(f"{r['tarih']} - {v.tam_ad()}")
        else:
            st.error("Hasta bulunamadı.")
    elif rol == "Veteriner":
        vet = veteriner_bul(kullanici_id)
        if vet:
            st.success(f"Hoşgeldiniz, {vet.tam_ad()}")
            st.subheader("📋 Bugünkü Randevular")
            for r in oku("data/randevular.json"):
                if r["veteriner_id"] == vet.id:
                    h = hasta_bul(r["hasta_id"])
                    st.info(f"{r['tarih']} - {h.tam_ad()}")
            st.subheader("💊 Tedavi Kaydı")
            h_id = st.selectbox("Hasta Seç", [h["id"] for h in oku("data/kullanicilar.json") if h["rol"] == "Hasta"])
            aciklama = st.text_area("Tedavi Açıklaması")
            if st.button("Kaydet"):
                yeni = Tedavi(h_id, vet.id, aciklama).__dict__
                veri = oku("data/tedaviler.json")
                veri.append(yeni)
                yaz("data/tedaviler.json", veri)
                st.success("Tedavi kaydedildi.")
            st.subheader("📖 Tedavi Geçmişi")
            for t in oku("data/tedaviler.json"):
                if t["veteriner_id"] == vet.id:
                    h = hasta_bul(t["hasta_id"])
                    st.info(f"{h.tam_ad()}: {t['aciklama']}")
        else:
            st.error("Veteriner bulunamadı.")
