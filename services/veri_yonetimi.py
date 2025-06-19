import json

def oku(dosya):
    try:
        with open(dosya, "r") as f:
            return json.load(f)
    except:
        return []

def yaz(dosya, veri):
    with open(dosya, "w") as f:
        json.dump(veri, f, indent=4)
