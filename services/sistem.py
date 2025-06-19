from models.hasta import Hasta
from models.veteriner import Veteriner
from services.veri_yonetimi import oku, yaz

def hasta_bul(id):
    for h in oku("data/kullanicilar.json"):
        if h["id"] == id and h["rol"] == "Hasta":
            return Hasta(h["id"], h["ad"], h["soyad"], h["tc"])
    return None

def veteriner_bul(id):
    for v in oku("data/kullanicilar.json"):
        if v["id"] == id and v["rol"] == "Veteriner":
            return Veteriner(v["id"], v["ad"], v["soyad"], v["brans"])
    return None

def kullanici_giris(id):
    for k in oku("data/kullanicilar.json"):
        if k["id"] == id:
            return k
    return None

def kullanici_kaydet(rol, id, ad, soyad, ekstra):
    veri = oku("data/kullanicilar.json")
    if any(k["id"] == id for k in veri):
        return False  # aynı ID varsa kayıt yapma
    veri.append({
        "rol": rol,
        "id": id,
        "ad": ad,
        "soyad": soyad,
        **ekstra
    })
    yaz("data/kullanicilar.json", veri)
    return True
