# geo.bio.tel.mainboard.py - geo + bio.tel angenehm konstelliert, ver-mainboardet, mehr Logik
# Zeugnis links: README.md aWAKE bleibt. Gemacht rechts: dieses .py agiert.
# Nichts wird geloescht. Nur angehaengt. Dieses Skript schreibt keine Dateien.
# 1 Name = 1 Respo. 1 Chip = 1 Platz. 1 Modul = 1 Aufgabe.
# geo.q.d.f + bio.tel + aWAKE + Mainboard = 1 Sache: Aufenthaltsort.

import hashlib
import json
import math
import time
from collections import Counter

MITTE = (9 * 9 + 1) // 2        # Mitte eines 9x9-Feldes = 41
HOME = 40
STAPEL = (9, 81, 243, 729, 3)
ORBIT_MAX = 3                    # letzter Orbit
# q.d.f nach Anfangsbuchstaben: Quant, Dimension, Faktor (vorher stand dimension="q", faktor="d", quant="q", ein f fehlte)
QDF = {"quant": "q", "dimension": "d", "faktor": "f"}


class Zeuge:
    """Rueckschauendes Hash-Log: nur anhaengen. Jede Zeile traegt den Hash der vorigen."""

    def __init__(self):
        self._zeilen = []

    @staticmethod
    def _hash(z):
        roh = json.dumps({k: z[k] for k in ("n", "enter", "text", "zeit", "vorher")},
                         ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(roh.encode("utf-8")).hexdigest()

    def schreibe(self, enter, text):
        vorher = self._zeilen[-1]["hash"] if self._zeilen else "0" * 64
        z = {"n": len(self._zeilen) + 1, "enter": enter, "text": text,
             "zeit": time.strftime("%Y-%m-%d %H:%M:%S"), "vorher": vorher}
        z["hash"] = self._hash(z)
        self._zeilen.append(z)

    def zeilen(self):
        return [dict(z) for z in self._zeilen]

    def unversehrt(self):
        vorher = "0" * 64
        for z in self._zeilen:
            if z["vorher"] != vorher or z["hash"] != self._hash(z):
                return False
            vorher = z["hash"]
        return True


def _text(x):
    return isinstance(x, str) and bool(x.strip())


# --- GEO: geo.q.d.f ---
class Geo:
    """GEO - q.d.f - Quant Dimension Faktor.
    GEO sagt WO. Wo schaut wer hin? Wo sitzt Chip? Wo ist Orbit?"""

    def __init__(self):
        self.quant, self.dimension, self.faktor = QDF["quant"], QDF["dimension"], QDF["faktor"]
        self.mitte = MITTE
        self.home = HOME

    def wo(self, wer, orbit, richtung):
        if not (_text(wer) and _text(richtung)):
            return {"modul": "GEO", "fehler": "wer und richtung muessen Text sein", "halt": "OFFEN"}
        if not isinstance(orbit, int) or isinstance(orbit, bool) or not 0 <= orbit <= ORBIT_MAX:
            return {"modul": "GEO", "fehler": f"orbit {orbit!r} ungueltig, erlaubt 0 bis {ORBIT_MAX}", "halt": "OFFEN"}
        return {
            "modul": "GEO", "wer": wer, "wo": richtung, "orbit": orbit,
            "letzter_orbit": orbit == ORBIT_MAX,
            "sieht_chips": len(Mainboard.sichtbar(orbit)),
            "dimension": self.dimension, "faktor": self.faktor, "quant": self.quant,
            "mitte": self.mitte, "home": self.home,
            "spruch": f"GEO: {wer} schaut von Orbit {orbit} nach {richtung}. Mitte {self.mitte}. Home {self.home}.",
            "halt": "ZIEL",
        }


# --- BIO.TEL: bio.teln - Bio Telefon ---
class BioTel:
    """BIO.TEL - bio.teln - Bio Telefon.
    BIO.TEL sagt WER lebt und WER ruft.
    Koerper ruft, Station hoert, Station antwortet. Nacheinander: 1 Ruf = 1 Antwort.
    Angenehm heisst: Nicht laut, nicht drueckend, nicht Overflow. Leise, klar, nacheinander."""

    def __init__(self, laut="leise"):
        self.atem = "ein_aus"
        self.laut = laut
        self.status = "wach"
        self._offen = None   # der eine offene Ruf

    def _ablehnen(self, was, hinweis):
        return {"modul": "BIO.TEL", "aktion": was, "angenommen": False, "hinweis": hinweis, "halt": "OFFEN"}

    def rufen(self, wer, was, an_wen):
        if not (_text(wer) and _text(was) and _text(an_wen)):
            return self._ablehnen("rufen", "wer, was und an_wen muessen Text sein")
        if self._offen:
            return self._ablehnen("rufen", f"nacheinander: erst antwortet {self._offen['an_wen']}, dann der naechste Ruf")
        self._offen = {"wer": wer, "an_wen": an_wen, "was": was}
        return {
            "modul": "BIO.TEL", "angenommen": True, "wer_ruft": wer, "was": was, "an_wen": an_wen,
            "atem": self.atem, "laut": self.laut, "status": self.status,
            "spruch": f"BIO.TEL: {wer} ruft {an_wen}: '{was}'. {self.laut.capitalize()}. Atmen {self.atem}.",
            "halt": "ZIEL",
        }

    def antworten(self, wer, antwort):
        if not (_text(wer) and _text(antwort)):
            return self._ablehnen("antworten", "wer und antwort muessen Text sein")
        if not self._offen:
            return self._ablehnen("antworten", "kein offener Ruf")
        if wer != self._offen["an_wen"]:
            return self._ablehnen("antworten", f"nur {self._offen['an_wen']} darf antworten")
        auf = self._offen["was"]
        self._offen = None
        return {
            "modul": "BIO.TEL", "angenommen": True, "wer_antwortet": wer, "antwort": antwort, "auf": auf,
            "laut": self.laut,
            "spruch": f"BIO.TEL: {wer} antwortet {self.laut}: '{antwort}'.",
            "halt": "ZIEL",
        }

    def angenehm(self):
        # Angenehm konstellieren heisst: Laut runter, Tempo runter, HALT rauf.
        self.laut = "leise"
        self.atem = "ein_aus"
        return {"angenehm": True, "laut": "leise", "atem": "ein_aus",
                "regel": "Leise, klar, nacheinander. Kein Overflow."}


# --- MAINBOARD: Chips ver-mainboardet ---
class Mainboard:
    """MAINBOARD - Chips im Mainboard, Design zum Board.
    5 Chips = 5 Punkte = Pentagramm = 5e (dazu 2 Module: BIO_TEL und GEO).
    Jeder Chip = 1 Platz = 1 Respo. Nichts uebereinander."""
    CHIPS = {
        "CPU": {"art": "chip", "platz": "oben", "aufgabe": "rechnen, denken, BRAIN", "orbit": 0},
        "RAM": {"art": "chip", "platz": "rechts oben", "aufgabe": "halten kurz, merken", "orbit": 1},
        "RAID": {"art": "chip", "platz": "rechts unten", "aufgabe": "verteilen, spiegeln, halten wenn einer ausfaellt", "orbit": 1},
        "SCSI": {"art": "chip", "platz": "unten", "aufgabe": "verbinden, Bus, Weg", "orbit": 2},
        "SLI": {"art": "chip", "platz": "links oben", "aufgabe": "2 Karten, 1 Bild, nacheinander", "orbit": 2},
        # vorher hatten BIO_TEL und GEO beide "mitte aussen" und lagen damit uebereinander:
        "BIO_TEL": {"art": "modul", "platz": "mitte aussen links", "aufgabe": "leben, rufen, hoeren, antworten, leise", "orbit": 3},
        "GEO": {"art": "modul", "platz": "mitte aussen rechts", "aufgabe": "wo, dimension, faktor, quant", "orbit": 3},
    }

    def __init__(self):
        self.mitte = MITTE
        self.home = HOME
        self.zeuge = Zeuge()

    @property
    def log(self):
        return self.zeuge.zeilen()

    @staticmethod
    def _key(name):
        return name.strip().upper().replace(".", "_") if isinstance(name, str) else None

    @classmethod
    def plaetze_doppelt(cls):
        zaehler = Counter(c["platz"] for c in cls.CHIPS.values())
        return sorted(p for p, n in zaehler.items() if n > 1)

    @classmethod
    def sichtbar(cls, orbit):
        """Lesart von 'nur der am weitesten zum letzten Orbit sieht mehr': Orbit k sieht alle Chips mit Orbit <= k."""
        return [n for n, c in cls.CHIPS.items() if c["orbit"] <= orbit]

    def chip(self, name):
        c = self.CHIPS.get(self._key(name))
        if not c:
            self.zeuge.schreibe("MAINBOARD", f"Chip {name!r} nicht gefunden. HALT, nicht raten.")
            return {"chip": name, "gefunden": False, "halt": "OFFEN"}
        self.zeuge.schreibe("MAINBOARD", f"Chip {self._key(name)} sitzt {c['platz']}. Aufgabe: {c['aufgabe']}.")
        return {"chip": self._key(name), "art": c["art"], "platz": c["platz"], "aufgabe": c["aufgabe"],
                "orbit": c["orbit"], "mitte": self.mitte, "gefunden": True, "halt": "ZIEL"}

    def alle_chips(self):
        return [self.chip(n) for n in self.CHIPS]

    def konstellation(self, angenehm=True):
        # Angenehm konstellieren: Chips nacheinander, nicht uebereinander. Leise. Klar.
        chips = self.alle_chips()
        bio = BioTel(laut="leise" if angenehm else "normal")
        if angenehm:
            bio.angenehm()
        doppelt = self.plaetze_doppelt()
        n_chip = sum(c["art"] == "chip" for c in chips)
        n_modul = sum(c["art"] == "modul" for c in chips)
        ok = all(c["gefunden"] for c in chips) and not doppelt
        self.zeuge.schreibe("MAINBOARD", f"Konstellation: {n_chip} Chips + {n_modul} Module, "
                                         f"doppelte Plaetze: {doppelt or 'keine'}, angenehm={angenehm}")
        return {
            "mainboard": "iki1uc geo." + ".".join(QDF.values()),
            "mitte": self.mitte, "home": self.home, "chips": chips,
            "anzahl_chips": n_chip, "anzahl_module": n_modul, "plaetze_doppelt": doppelt,
            "angenehm": angenehm, "laut": bio.laut, "atem": bio.atem,
            "regel": "Jeder Chip 1 Platz. Nichts uebereinander. Leise, klar, nacheinander. Kein Overflow.",
            "halt": "ZIEL" if ok else "OFFEN",
        }


# --- aWAKE: Globaler Wecker ---
class Awake:
    """aWAKE - Globaler Wecker & SUB-Master.
    aWAKE weckt jeden RESPO, gibt wake.map, wandelt 1D in 3D.
    1D -> 3D: speed=5 -> [5,0,0]. Motor kann kein 1D."""

    def wecken(self, respo, speed=5):
        if not _text(respo):
            return {"fehler": "respo muss Text sein", "halt": "OFFEN"}
        if isinstance(speed, bool) or not isinstance(speed, (int, float)) or not math.isfinite(speed):
            return {"respo": respo, "fehler": f"speed {speed!r} ist keine endliche Zahl", "halt": "OFFEN"}
        vector = [speed, 0, 0]
        wake = {"wake.job": "REC_", "wake.reason": "PX/PQ", "wake.vector": vector, "wake.pipeline": "3|6",
                "wake.tmp": "TMP__SUB", "wake.alias": respo, "wake.wann": time.strftime("%Y-%m-%d %H:%M:%S")}
        return {"respo": respo, "wake": wake, "vector": vector, "status": "geweckt", "halt": "ZIEL"}

    def logik(self):
        # Mehr Logik: aWAKE + GEO + BIO.TEL + MAINBOARD = 1 Logik. Was davon der Code prueft, steht in pruefe().
        return {
            "logik_1": "GEO sagt WO.",
            "logik_2": "BIO.TEL sagt WER ruft und WER antwortet.",
            "logik_3": "MAINBOARD sagt WO Chip sitzt.",
            "logik_4": "aWAKE sagt WANN geweckt wird.",
            "logik_5": "Nur der am weitesten zum letzten Orbit sieht mehr und weiss mehr.",
            "logik_6": "Nichts wird geloescht. Nur angehaengt.",
            "logik_7": "STAND + STAGE = 1. Nacheinander, nicht zusammen.",
            "halt": "ZIEL" if all(pruefe().values()) else "OFFEN",
        }


def pruefe():
    """Selbsttest: jede Aussage auf frischen Objekten, ohne Dateien."""
    p = {}
    p["qdf_ergibt_q.d.f"] = ".".join(QDF.values()) == "q.d.f" and len(set(QDF.values())) == 3
    p["mitte_41_home_40"] = MITTE == 41 and HOME == 40
    chips = Mainboard.CHIPS
    p["5_chips_2_module"] = sum(c["art"] == "chip" for c in chips.values()) == 5 and \
        sum(c["art"] == "modul" for c in chips.values()) == 2
    p["jeder_chip_1_platz"] = Mainboard.plaetze_doppelt() == []
    zahlen = [len(Mainboard.sichtbar(o)) for o in range(ORBIT_MAX + 1)]
    p["sicht_waechst_mit_orbit"] = zahlen == sorted(zahlen) and zahlen[-1] == len(chips) and \
        Mainboard.sichtbar(0) == ["CPU"]
    b = BioTel()
    r1 = b.rufen("A", "hallo", "B")["angenommen"]
    r2 = b.rufen("C", "dazwischen", "B")["angenommen"]
    r3 = b.antworten("C", "falscher")["angenommen"]
    r4 = b.antworten("B", "ok")["angenommen"]
    r5 = b.rufen("C", "jetzt", "B")["angenommen"]
    p["ruf_nacheinander"] = (r1, r2, r3, r4, r5) == (True, False, False, True, True)
    p["angenehm_wirkt"] = Mainboard().konstellation(False)["laut"] == "normal" and \
        Mainboard().konstellation(True)["laut"] == "leise"
    a = Awake()
    p["wecken_1d_3d"] = a.wecken("X", 5)["vector"] == [5, 0, 0] and \
        a.wecken("X", "5")["halt"] == "OFFEN" and a.wecken("X", float("nan"))["halt"] == "OFFEN"
    g = Geo()
    p["geo_orbit_geprueft"] = g.wo("A", ORBIT_MAX, "x")["halt"] == "ZIEL" and g.wo("A", 9, "x")["halt"] == "OFFEN"
    m = Mainboard()
    m.chip("CPU")
    m.chip("nix")
    ok_vorher = m.zeuge.unversehrt()
    m.zeuge._zeilen[0]["text"] = "nachtraeglich"
    p["log_kette_haelt"] = ok_vorher and not m.zeuge.unversehrt()
    return p


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
    t = pruefe()
    l = awake.logik()
    halt = "ZIEL" if all(x["halt"] == "ZIEL" for x in (g1, g2, b1, b2, k, w)) and all(t.values()) else "OFFEN"
    return {"geo": [g1, g2], "bio_tel": [b1, b2], "mainboard": k, "awake": w, "logik": l,
            "selbsttest": t, "log": board.log, "log_unversehrt": board.zeuge.unversehrt(), "halt": halt}


if __name__ == "__main__":
    r = demo()
    print(f"Station iki1uc geo.{'.'.join(QDF.values())} - HALT = {r['halt']}")
    for g in r["geo"]:
        print(f"-> {g['spruch']} (sieht {g['sieht_chips']} Chips)")
    for b in r["bio_tel"]:
        print(f"-> {b['spruch']}")
    mb = r["mainboard"]
    print(f"-> MAINBOARD: {mb['anzahl_chips']} Chips + {mb['anzahl_module']} Module. Mitte {mb['mitte']}. "
          f"Angenehm={mb['angenehm']}. Laut={mb['laut']}. Doppelte Plaetze: {mb['plaetze_doppelt'] or 'keine'}.")
    for c in mb["chips"]:
        print(f"   - {c['chip']}: {c['platz']} - {c['aufgabe']}")
    print(f"-> aWAKE: {r['awake']['respo']} geweckt. Vektor {r['awake']['vector']}.")
    for k, v in r["logik"].items():
        if k.startswith("logik"):
            print(f"-> Logik: {v}")
    ok = sum(r["selbsttest"].values())
    print(f"-> Selbsttest: {ok}/{len(r['selbsttest'])} bestanden")
    for name, val in r["selbsttest"].items():
        if not val:
            print("   FEHLT:", name)
    print(f"-> Log: {len(r['log'])} Zeilen. Kette unversehrt: {r['log_unversehrt']}.")
