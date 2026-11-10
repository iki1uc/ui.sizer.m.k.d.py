# geo.bio.tel.mainboard.py - geo + bio.tel angenehm konstelliert, ver-mainboardet, mehr Logik
# Zeugnis links: README.md aWAKE bleibt. Gemacht rechts: dieses .py agiert.
# Nichts wird geloescht. Nur angehaengt.
# 1 Name = 1 Respo. 1 Chip = 1 Platz. 1 Modul = 1 Aufgabe.
# geo.q.d.f + bio.tel + aWAKE + Mainboard = 1 Sache: Aufenthaltsort.

import json, hashlib, time

MITTE = 41
HOME = 40
STAPEL = (9, 81, 243, 729, 3)

# --- GEO: geo.q.d.f ---
class Geo:
    """GEO - q.d.f - Dimension Faktor Quant.
    GEO sagt WO. Wo schaut wer hin? Wo sitzt Chip? Wo ist Orbit?"""
    def __init__(self):
        self.dimension = "q"
        self.faktor = "d"
        self.quant = "q"
        self.mitte = MITTE
        self.home = HOME
    def wo(self, wer, orbit, richtung):
        return {
            "modul": "GEO",
            "wer": wer,
            "wo": richtung,
            "orbit": orbit,
            "dimension": self.dimension,
            "faktor": self.faktor,
            "quant": self.quant,
            "mitte": self.mitte,
            "home": self.home,
            "spruch": f"GEO: {wer} schaut von Orbit {orbit} nach {richtung}. Mitte {self.mitte}. Home {self.home}.",
            "halt": "ZIEL",
        }

# --- BIO.TEL: bio.teln - Bio Telefon ---
class BioTel:
    """BIO.TEL - bio.teln - Bio Telefon.
    BIO.TEL sagt WER lebt und WER ruft.
    BIO = Leben, Koerper, Atmen. TEL = Rufen, Hoeren, Antworten.
    BIO.TEL ist nicht Handy. BIO.TEL ist: Koerper ruft, Station hoert, Station antwortet.
    Angenehm heisst: Nicht laut, nicht drueckend, nicht Overflow. Leise, klar, nacheinander."""
    def __init__(self):
        self.atem = "ein_aus"
        self.laut = "leise"  # angenehm = leise, nicht laut
        self.status = "wach"
    def rufen(self, wer, was, an_wen):
        # 1 Ruf = 1 Aufgabe. 1 Anruf = 1 Antwort. Nacheinander.
        return {
            "modul": "BIO.TEL",
            "wer_ruft": wer,
            "was": was,
            "an_wen": an_wen,
            "atem": self.atem,
            "laut": self.laut,
            "status": self.status,
            "spruch": f"BIO.TEL: {wer} ruft {an_wen}: '{was}'. Leise. Atmen {self.atem}.",
            "halt": "ZIEL",
        }
    def antworten(self, wer, antwort):
        return {
            "modul": "BIO.TEL",
            "wer_antwortet": wer,
            "antwort": antwort,
            "laut": "leise",
            "spruch": f"BIO.TEL: {wer} antwortet leise: '{antwort}'.",
            "halt": "ZIEL",
        }
    def angenehm(self):
        # Angenehm konstellieren heisst: Laut runter, Tempo runter, HALT rauf.
        self.laut = "leise"
        self.atem = "ein_aus"
        return {"angenehm": True, "laut": "leise", "atem": "ein_aus", "regel": "Leise, klar, nacheinander. Kein Overflow."}

# --- MAINBOARD: Chips ver-mainboardet ---
class Mainboard:
    """MAINBOARD - Chips im Mainboard, Design zum Board.
    5 Chips = 5 Punkte = Pentagramm = 5e.
    Jeder Chip = 1 Platz = 1 Respo. Nichts uebereinander."""
    CHIPS = {
        "CPU": {"platz": "oben", "aufgabe": "rechnen, denken, BRAIN", "orbit": 0},
        "RAM": {"platz": "rechts oben", "aufgabe": "halten kurz, merken", "orbit": 1},
        "RAID": {"platz": "rechts unten", "aufgabe": "verteilen, spiegeln, halten wenn einer ausfaellt", "orbit": 1},
        "SCSI": {"platz": "unten", "aufgabe": "verbinden, Bus, Weg", "orbit": 2},
        "SLI": {"platz": "links oben", "aufgabe": "2 Karten, 1 Bild, nacheinander", "orbit": 2},
        "BIO_TEL": {"platz": "mitte aussen", "aufgabe": "leben, rufen, hoeren, antworten, leise", "orbit": 3},
        "GEO": {"platz": "mitte aussen", "aufgabe": "wo, dimension, faktor, quant", "orbit": 3},
    }
    def __init__(self):
        self.mitte = MITTE
        self.home = HOME
        self.log = []
    def _log(self, text):
        vorher = self.log[-1]["hash"] if self.log else "0"*64
        z = {"n": len(self.log)+1, "text": text, "zeit": time.strftime("%Y-%m-%d %H:%M:%S"), "vorher": vorher}
        roh = json.dumps({k: z[k] for k in ("n","text","zeit","vorher")}, ensure_ascii=False, sort_keys=True)
        z["hash"] = hashlib.sha256(roh.encode("utf-8")).hexdigest()
        self.log.append(z)
    def chip(self, name):
        c = self.CHIPS.get(name)
        if not c:
            self._log(f"MAINBOARD: Chip {name} nicht gefunden. HALT, nicht raten.")
            return {"chip": name, "gefunden": False, "halt": "OFFEN"}
        self._log(f"MAINBOARD: Chip {name} sitzt {c['platz']}. Aufgabe: {c['aufgabe']}.")
        return {"chip": name, "platz": c["platz"], "aufgabe": c["aufgabe"], "orbit": c["orbit"], "mitte": self.mitte, "gefunden": True, "halt": "ZIEL"}
    def alle_chips(self):
        return [self.chip(n) for n in self.CHIPS]
    def konstellation(self, angenehm=True):
        # Angenehm konstellieren: Chips nacheinander, nicht uebereinander. Leise. Klar.
        chips = self.alle_chips()
        bio = BioTel()
        if angenehm:
            bio.angenehm()
        return {
            "mainboard": "iki1uc geo.q.d.f",
            "mitte": self.mitte,
            "home": self.home,
            "chips": chips,
            "anzahl_chips": len(chips),
            "angenehm": angenehm,
            "laut": bio.laut,
            "atem": bio.atem,
            "regel": "Jeder Chip 1 Platz. Nichts uebereinander. Leise, klar, nacheinander. Kein Overflow.",
            "halt": "ZIEL",
        }

# --- aWAKE: Globaler Wecker ---
class Awake:
    """aWAKE - Globaler Wecker & SUB-Master.
    aWAKE weckt jeden RESPO, gibt wake.map, wandelt 1D in 3D.
    1D -> 3D: speed=5 -> [5,0,0]. Motor kann kein 1D."""
    def wecken(self, respo, speed=5):
        vector = [speed, 0, 0]
        wake = {"wake.job": "REC_", "wake.reason": "PX/PQ", "wake.vector": vector, "wake.pipeline": "3|6", "wake.tmp": "TMP__SUB", "wake.alias": respo}
        return {"respo": respo, "wake": wake, "vector": vector, "status": "geweckt", "halt": "ZIEL"}
    def logik(self):
        # Mehr Logik: aWAKE + GEO + BIO.TEL + MAINBOARD = 1 Logik
        return {
            "logik_1": "GEO sagt WO.",
            "logik_2": "BIO.TEL sagt WER ruft und WER antwortet.",
            "logik_3": "MAINBOARD sagt WO Chip sitzt.",
            "logik_4": "aWAKE sagt WANN geweckt wird.",
            "logik_5": "Nur der am weitesten zum letzten Orbit sieht mehr und weiss mehr.",
            "logik_6": "Nichts wird geloescht. Nur angehaengt.",
            "logik_7": "STAND + STAGE = 1. Nacheinander, nicht zusammen.",
            "halt": "ZIEL",
        }

def demo():
    geo = Geo()
    bio = BioTel()
    board = Mainboard()
    awake = Awake()
    g1 = geo.wo("DU", 1, "MITTE 41")
    g2 = geo.wo("ANDERER_MANN", 3, "LETZTER ORBIT DEEPSPACE")
    b1 = bio.rufen("DU", "Glas Kugel klar?", "ANDERER_MANN")
    b2 = bio.antworten("ANDERER_MANN", "Klar. Leise. HALT.")
    k = board.konstellation(angenehm=True)
    w = awake.wecken("BIO.TEL", speed=5)
    l = awake.logik()
    return {"geo": [g1, g2], "bio_tel": [b1, b2], "mainboard": k, "awake": w, "logik": l, "log": board.log, "halt": "ZIEL"}

if __name__ == "__main__":
    r = demo()
    print(f"Station iki1uc geo.q.d.f - HALT = {r['halt']}")
    for g in r["geo"]:
        print(f"-> {g['spruch']}")
    for b in r["bio_tel"]:
        print(f"-> {b['spruch']}")
    print(f"-> MAINBOARD: {r['mainboard']['anzahl_chips']} Chips. Mitte {r['mainboard']['mitte']}. Angenehm={r['mainboard']['angenehm']}. Laut={r['mainboard']['laut']}.")
    for c in r["mainboard"]["chips"]:
        print(f"   - {c['chip']}: {c['platz']} - {c['aufgabe']}")
    print(f"-> aWAKE: {r['awake']['respo']} geweckt. Vektor {r['awake']['vector']}.")
    for k, v in r["logik"].items():
        if k.startswith("logik"):
            print(f"-> Logik: {v}")
    print(f"-> Log: {len(r['log'])} Zeilen. Nichts geloescht.")
