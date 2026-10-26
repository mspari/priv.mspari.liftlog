# liftlog

Trainingsdaten — Kraft, Laufen, Radfahren.

## sessions.csv

Eine Zeile pro Satz.

| Spalte | Bedeutung |
|---|---|
| `date` | ISO-Datum der Einheit |
| `session` | `A` (Squat + Press), `B` (Deadlift + Bench), `CARDIO` |
| `exercise` | Übungsname |
| `set_no` | Satznummer innerhalb der Übung |
| `weight_kg` | Gesamtgewicht in kg; leer bei Körpergewicht oder Band |
| `reps` | Wiederholungen in diesem Satz |
| `unit` | `kg`, `bodyweight`, `band`, `min`, `km` |
| `note` | Freitext |

Einarmige Übungen: `weight_kg` ist das Gewicht pro Hantel, `reps` gilt pro Seite (steht in `note`).
Kurzhantel-Bankdrücken: `weight_kg` ist die Summe beider Hanteln.

## Plan

Zwei Krafteinheiten pro Woche, dazu eine Laufeinheit und eine Radrunde.

**Session A** — Back/Front Squat 4×5 · Strict Press 3×6 · Hip Thrusts 3×10 · DB Rows einarmig 3×10 · Core (Dead Bug, Pallof Press)

**Session B** — Deadlift 4×5 · Bench Press 3×6 · Pull-ups 6×2 mit Band (Scapula Pull-ups davor) · Walking Lunges 3×10/Seite · Face Pulls 3×15

Progression: alle Sätze sauber → Oberkörper Double Progression (3×6 → 3×8, dann +2,5 kg), Unterkörper +5 kg. Zweimal dasselbe Gewicht verfehlt → 10 % runter.
