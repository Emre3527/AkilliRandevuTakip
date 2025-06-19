class Kullanici:
    def __init__(self, id, ad, soyad):
        self.id = id
        self.ad = ad
        self.soyad = soyad

    def tam_ad(self):
        return f"{self.ad} {self.soyad}"
