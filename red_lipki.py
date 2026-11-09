import json, urllib.request as u
from datetime import date, timedelta

LAT, LON = 49.5918, 43.7214

def check(day, window=21):
    end = date.fromisoformat(day)
    start = end - timedelta(days=window)
    url = ("https://archive-api.open-meteo.com/v1/archive"
           f"?latitude={LAT}&longitude={LON}"
           f"&start_date={start}&end_date={end}"
           "&daily=precipitation_sum,temperature_2m_min"
           "&timezone=Europe/Volgograd")
    d = json.load(u.urlopen(url))["daily"]
    total = sum(x or 0 for x in d["precipitation_sum"])
    wet = [(t, p) for t, p in zip(d["time"], d["precipitation_sum"]) if p and p >= 3]
    print(f"{day}: {total:.1f} мм за {window} дн.; "
          f"мин. ночная t за период: {min(d['temperature_2m_min']):.1f} °C; "
          f"за последние 7 дн.: {min(d['temperature_2m_min'][-7:]):.1f} °C")
    print("  дни с осадками ≥3 мм:", wet)
    print()

for day in ("2022-10-14", "2025-10-25", "2026-11-04"):
    check(day)
