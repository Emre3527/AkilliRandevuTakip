from models.kullanici import Kullanici

class Hasta(Kullanici):
    def __init__(self, id, ad, soyad, tc):
        super().__init__(id, ad, soyad)
        self.tc = tc
