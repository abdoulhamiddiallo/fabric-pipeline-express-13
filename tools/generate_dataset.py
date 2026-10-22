"""Génère une semaine de traversées des ferries électriques de l'ouest de la Norvège, 12 au 18 octobre 2026 (données fictives).

Un fichier CSV par liaison, dans data/crossings : six petits fichiers, comme les envoient les compagnies.
Chaque traversée : passagers, voitures, énergie consommée (kWh) et batterie restante à l'arrivée (%).
"""
import csv, random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(1313)
OUT = Path(__file__).resolve().parent.parent / "data" / "crossings"
OUT.mkdir(parents=True, exist_ok=True)

ROUTES = [  # fichier, liaison, minutes de traversée, rotations par jour, kWh de base, kWh par voiture
    ("halhjem_sandvikvag", "Halhjem-Sandvikvåg", 40, 22, 900, 6.4),
    ("lavik_oppedal", "Lavik-Oppedal", 20, 30, 380, 3.1),
    ("hareid_sulesund", "Hareid-Sulesund", 25, 26, 470, 3.6),
    ("molde_vestnes", "Molde-Vestnes", 35, 24, 760, 5.5),
    ("flakk_rorvik", "Flakk-Rørvik", 25, 28, 420, 3.9),
    ("moss_horten", "Moss-Horten", 30, 20, 640, 4.2),
]
cid = 13000
for key, name, minutes, rot, base, per_car in ROUTES:
    rows = []
    for day in range(7):
        d = datetime(2026, 10, 12) + timedelta(days=day)
        weekend = day >= 5
        for k in range(rot - (4 if weekend else 0)):
            cid += 1
            t = d + timedelta(hours=5.5, minutes=k * (18 * 60 // rot) + random.randint(0, 6))
            cars = max(4, int(random.gauss(48 if not weekend else 62, 14)))
            pax = cars * random.randint(1, 3) + random.randint(0, 40)
            kwh = int(base + per_car * cars * random.uniform(0.9, 1.1))
            batt = max(18, min(92, int(random.gauss(64, 9))))
            rows.append([cid, name, t.strftime("%Y-%m-%d %H:%M:%S"), minutes, pax, cars, kwh, batt])
    with open(OUT / f"{key}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["crossing_id", "route", "departed_at", "minutes", "passengers", "cars", "energy_kwh", "battery_end_pct"]); w.writerows(rows)
    print(f"{name} : {len(rows)} traversées")
