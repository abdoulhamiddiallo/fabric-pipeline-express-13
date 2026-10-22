"""Recalcule ce que le Script Fjord board doit renvoyer."""
import csv, glob
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

q = lambda x, n: Decimal(x).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP)
rows = []
for f in sorted(glob.glob(str(Path(__file__).resolve().parent.parent / "data" / "crossings" / "*.csv"))):
    rows += list(csv.DictReader(open(f, encoding="utf-8")))
S = lambda c, rs=rows: sum(int(r[c]) for r in rs)
print(f"traversées {len(rows)}  passagers {S('passengers')}  voitures {S('cars')}  MWh {q(Decimal(S('energy_kwh'))/1000,1)}  kWh/voiture {q(Decimal(S('energy_kwh'))/S('cars'),2)}  batterie min {min(int(r['battery_end_pct']) for r in rows)}")
by = {}
for r in rows: by.setdefault(r["route"], []).append(r)
for name, rs in sorted(by.items(), key=lambda kv: Decimal(S('energy_kwh', kv[1])) / S('cars', kv[1])):
    print(f"  {name:22} {len(rs):4} traversées  {S('cars', rs):6} voitures  {q(Decimal(S('energy_kwh', rs))/S('cars', rs),2)} kWh/voiture  batterie min {min(int(r['battery_end_pct']) for r in rs)}")
