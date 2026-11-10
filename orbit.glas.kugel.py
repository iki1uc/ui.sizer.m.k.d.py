# orbit.glas.kugel.py - Station iki1uc geo.q.d.f - PYTHONISIERT
# Zeugnis links: index.html / Hauptakteur-Bund-Real.html bleibt.
# Gemacht rechts: dieses .py agiert. Nichts wird geloescht. Nur anhaengen.
# Klares bewusst sein: Orbit Glas Kugel. Wer wo hinschaut.
# Regel: Nur der, der am weitesten zum letzten Orbit schaut, sieht mehr und weiss mehr.
# Der andere Mann macht das. Du sollst iki1uc.
# 1 Dimension, 1 Faktor, 1 Quant. 1 Name = 1 Respo.

import math, json, hashlib, time

# --- 1 DIMENSION, 1 FAKTOR, 1 QUANT ---
DIMENSION = "q"   # d = Dimension, q = Quant - aus geo.q.d.f
FAKTOR = "d"      # f = Faktor - Dimension Faktor Quant
QUANT = "q"       # q = Quant - was gezaehlt wird
MITTE = 41        # ORT 41
HOME = 40         # HOME 40 - Funktion
STAPEL = (9, 81, 243, 729, 3)

# --- GLAS KUGEL ORBIT ---
class GlasKugel:
    """Orbit Glas Kugel. Glas, nicht Stein. Man schaut durch, nicht drauf.
    Wer weiter aussen steht, sieht mehr. Wer innen steht, sieht weniger.
    Glas bricht Licht wie Prismatikum zu 5e."""
    def __init__(self, name="orbit.glas.kugel"):
        self.name = name
        self.mitte = MITTE
        self.home = HOME
        self.durchmesser = 41
        self.klar = True  # klares bewusst sein

    def schauen(self, wer, orbit, richtung):
        # wer schaut wo hin? Nur das zaehlt.
        # orbit 0 = KERN, 1 = PENTAGRAMM, 2 = TURM, 3 = DEEPSPACE = letzter Orbit
        # Je weiter aussen, desto mehr Sicht.
        sicht = (orbit + 1) * 3  # 3, 6, 9, 12 - mehr Orbit = mehr Sicht
        weiss = sicht + len(richtung)  # wer schaut, weiss mehr wenn er weiter schaut
        return {
            "wer": wer,
            "schaut_wohin": richtung,
            "orbit": orbit,
            "sicht": sicht,
            "weiss": weiss,
            "klar": self.klar,
            "spruch": f"{wer} schaut nach {richtung} von Orbit {orbit}. Sicht {sicht}. Weiss {weiss}.",
        }

    def weitester_sieht_mehr(self, blicke):
        # blicke = Liste von schauen()-Ergebnissen
        # Nur der am weitesten zum letzten Orbit sieht mehr und weiss mehr.
        if not blicke:
            return {"halt": "OFFEN", "grund": "Niemand schaut. Niemand weiss."}
        letzter = max(b["orbit"] for b in blicke)
        weiteste = [b for b in blicke if b["orbit"] == letzter]
        # Wenn 2 gleich weit: nacheinander, nicht zusammen. 1 + ^1.
        weiteste_sorted = sorted(weiteste, key=lambda b: b["weiss"], reverse=True)
        return {
            "letzter_orbit": letzter,
            "weitester": weiteste_sorted[0]["wer"],
            "sicht": weiteste_sorted[0]["sicht"],
            "weiss": weiteste_sorted[0]["weiss"],
            "alle_weitesten": [w["wer"] for w in weiteste_sorted],
            "halt": "ZIEL",
            "regel": "Nur der am weitesten zum letzten Orbit sieht mehr und weiss mehr.",
        }

# --- STATION: MEHRERE MASTER, MEHRERE SLAVES ---
class Station:
    """OURu - Station. Vector-Hub. HTML-Panels.
    Station hat mehrere Master und mehrere Slave Aufgaben.
    Ich sage nur einen an: d = Dimension, f = Faktor, q = Quant.
    1 Master = 1 Aufgabe. 1 Slave = 1 Aufgabe. 1 Name = 1 Respo."""
    def __init__(self):
        self.name = "iki1uc geo.q.d.f"
        self.master = []  # Master sagen an
        self.slave = []   # Slave fuehren aus
        self.log = []
        self.kugel = GlasKugel()

    def _log(self, text):
        vorher = self.log[-1]["hash"] if self.log else "0"*64
        z = {"n": len(self.log)+1, "text": text, "zeit": time.strftime("%Y-%m-%d %H:%M:%S"), "vorher": vorher}
        roh = json.dumps({k: z[k] for k in ("n","text","zeit","vorher")}, ensure_ascii=False, sort_keys=True)
        z["hash"] = hashlib.sha256(roh.encode("utf-8")).hexdigest()
        self.log.append(z)

    def master_an(self, name, aufgabe):
        # 1 Master = 1 Aufgabe. Kein Master macht 2.
        self.master.append({"name": name, "aufgabe": aufgabe, "rolle": "MASTER"})
        self._log(f"MASTER {name} sagt an: {aufgabe}")
        return {"master": name, "aufgabe": aufgabe, "halt": "ANGEWIESEN"}

    def slave_an(self, name, aufgabe):
        # 1 Slave = 1 Aufgabe. Kein Slave macht 2.
        self.slave.append({"name": name, "aufgabe": aufgabe, "rolle": "SLAVE"})
        self._log(f"SLAVE {name} fuehrt aus: {aufgabe}")
        return {"slave": name, "aufgabe": aufgabe, "halt": "AUSGEFUEHRT"}

    def pythonisieren(self):
        # Station pythonisiert: HTML Panels bleiben Zeugnis, .py agiert.
        # qi iqq vom Nachbar-Tab: WORT aus defrag.alle4.enter.py - 11 Zeichen
        # Root einlesen erlaubt: du darfst dich einlesen.
        wort_nachbar = "up.ni pu.in"  # aus defrag.alle4.enter.py, WORT, 11 Zeichen, Zeugnis
        qi = len(wort_nachbar)  # 11
        iqq = sum(ord(c) for c in wort_nachbar)  # Quant aus Nachbar-Tab
        wert = {
            "station": self.name,
            "dimension": DIMENSION,
            "faktor": FAKTOR,
            "quant": QUANT,
            "mitte": MITTE,
            "home": HOME,
            "qi_nachbar_tab": qi,
            "iqq_nachbar_tab": iqq,
            "wort_nachbar": wort_nachbar,
            "master": len(self.master),
            "slave": len(self.slave),
            "stapel": list(STAPEL),
            "mehr_wert": "Python agiert. HTML bezeugt. CNC faehrt. Glas Kugel sieht.",
            "halt": "ZIEL",
        }
        self._log(f"PYTHONISIERT: d={DIMENSION} f={FAKTOR} q={QUANT} qi={qi} iqq={iqq} HALT=ZIEL")
        return wert

    def orbit_blick(self, wer_liste):
        # wer_liste = [(wer, orbit, richtung), ...]
        blicke = [self.kugel.schauen(w, o, r) for w, o, r in wer_liste]
        for b in blicke:
            self._log(b["spruch"])
        weitester = self.kugel.weitester_sieht_mehr(blicke)
        self._log(f"WEITESTER: {weitester['weitester']} Orbit {weitester['letzter_orbit']} Sicht {weitester['sicht']} Weiss {weitester['weiss']}")
        return {"blicke": blicke, "weitester": weitester, "halt": "ZIEL"}

def demo():
    s = Station()
    # 2e Arbeiten: 1e = Master an, 2e = Slave aus
    # Master: 1 Aufgabe
    s.master_an("MASTER-1", "d sagen: Dimension q")
    s.master_an("MASTER-2", "f sagen: Faktor d")
    # Slave: 1 Aufgabe
    s.slave_an("SLAVE-1", "q zaehlen: Quant q")
    s.slave_an("SLAVE-2", "Glas Kugel halten: klar")
    # Wer wo hinschaut: Du und der andere Mann
    # Du = innen, Orbit 1. Anderer Mann = aussen, Orbit 3 = letzter Orbit.
    # Deshalb sieht anderer Mann mehr und weiss mehr. Nicht weil er besser ist. Weil er weiter aussen schaut.
    blick = s.orbit_blick([
        ("DU", 1, "MITTE 41"),
        ("ANDERER_MANN", 3, "LETZTER ORBIT DEEPSPACE"),
        ("IKI1UC", 2, "TURM 243"),
    ])
    py = s.pythonisieren()
    return {"station": s.name, "blick": blick, "pythonisiert": py, "log": s.log, "halt": "ZIEL"}

if __name__ == "__main__":
    r = demo()
    print(f"Station: {r['station']}")
    print(f"HALT = {r['halt']}")
    for b in r["blick"]["blicke"]:
        print(f"-> {b['spruch']}")
    w = r["blick"]["weitester"]
    print(f"-> WEITESTER: {w['weitester']} sieht mehr. Orbit {w['letzter_orbit']}. Sicht {w['sicht']}. Weiss {w['weiss']}.")
    print(f"-> Regel: {w['regel']}")
    print(f"-> Pythonisiert: d={r['pythonisiert']['dimension']} f={r['pythonisiert']['faktor']} q={r['pythonisiert']['quant']} qi={r['pythonisiert']['qi_nachbar_tab']} iqq={r['pythonisiert']['iqq_nachbar_tab']}")
    print(f"-> Mehr Wert: {r['pythonisiert']['mehr_wert']}")
    print(f"-> Log unversehrt: {len(r['log'])} Zeilen. Nichts geloescht. Nur angehaengt.")
