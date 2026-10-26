#!/usr/bin/env python3
"""Prueft sessions.jsonl gegen das Schema aus dem README.

Aufruf:  python3 validate.py [pfad]

Exit 0 wenn alles passt, sonst 1 mit Fundliste auf stderr.
Gedacht als Absicherung, bevor eine neue Session committet wird.
"""

import json
import sys
from datetime import date

SESSIONS = {"A", "B", "CARDIO"}
UNITS = {"kg", "bodyweight", "band", "min", "km"}
SET_KEYS = {"set", "weight_kg", "reps", "unit", "note"}


def check(path):
    problems = []

    def bad(line_no, msg):
        problems.append(f"Zeile {line_no}: {msg}")

    seen = set()
    last_date = None

    with open(path, encoding="utf-8") as fh:
        for n, raw in enumerate(fh, start=1):
            if not raw.strip():
                bad(n, "leere Zeile")
                continue
            try:
                s = json.loads(raw)
            except json.JSONDecodeError as exc:
                bad(n, f"kein gueltiges JSON ({exc.msg})")
                continue

            d = s.get("date")
            try:
                parsed = date.fromisoformat(d)
            except (TypeError, ValueError):
                bad(n, f"date fehlt oder ist kein ISO-Datum: {d!r}")
                parsed = None
            else:
                if parsed > date.today():
                    bad(n, f"date liegt in der Zukunft: {d}")
                if last_date and parsed < last_date:
                    bad(n, f"date {d} liegt vor der Vorgaengerzeile — Datei sollte chronologisch sein")
                last_date = parsed

            typ = s.get("session")
            if typ not in SESSIONS:
                bad(n, f"session muss eines von {sorted(SESSIONS)} sein, ist {typ!r}")

            key = (d, typ)
            if key in seen:
                bad(n, f"doppelte Session {d} / {typ}")
            seen.add(key)

            if "duration_min" in s and not isinstance(s["duration_min"], (int, float)):
                bad(n, "duration_min ist keine Zahl")

            exercises = s.get("exercises")
            if not isinstance(exercises, list) or not exercises:
                bad(n, "exercises fehlt oder ist leer")
                continue

            for ex in exercises:
                name = ex.get("exercise")
                if not isinstance(name, str) or not name.strip():
                    bad(n, "exercise ohne Namen")
                    continue

                sets = ex.get("sets")
                if not isinstance(sets, list) or not sets:
                    bad(n, f"{name}: sets fehlt oder ist leer")
                    continue

                for i, st in enumerate(sets, start=1):
                    where = f"{name} Satz {i}"
                    unknown = set(st) - SET_KEYS
                    if unknown:
                        bad(n, f"{where}: unbekannte Felder {sorted(unknown)}")
                    if st.get("set") != i:
                        bad(n, f"{where}: set ist {st.get('set')!r}, erwartet {i}")
                    unit = st.get("unit")
                    if unit not in UNITS:
                        bad(n, f"{where}: unit muss eines von {sorted(UNITS)} sein, ist {unit!r}")
                    if unit == "kg" and not isinstance(st.get("weight_kg"), (int, float)):
                        bad(n, f"{where}: unit kg, aber weight_kg fehlt")
                    if unit in {"bodyweight", "band"} and "weight_kg" in st:
                        bad(n, f"{where}: unit {unit}, aber weight_kg gesetzt")
                    if "reps" in st and not isinstance(st["reps"], int):
                        bad(n, f"{where}: reps ist keine ganze Zahl")
                    if "note" in st and not isinstance(st["note"], str):
                        bad(n, f"{where}: note ist kein Text")

    return problems


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "sessions.jsonl"
    found = check(target)
    if found:
        print(f"{len(found)} Problem(e) in {target}:", file=sys.stderr)
        for p in found:
            print(f"  {p}", file=sys.stderr)
        sys.exit(1)
    print(f"{target}: alles in Ordnung")
