from models.kullanici import Kullanici

class Veteriner(Kullanici):
    def __init__(self, id, ad, soyad, brans):
        super().__init__(id, ad, soyad)
        self.brans = brans
