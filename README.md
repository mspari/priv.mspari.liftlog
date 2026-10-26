# liftlog

Trainingsdaten — Kraft, Laufen, Radfahren.

## sessions.jsonl

Ein JSON-Objekt pro Zeile, eine Zeile pro Session. Neue Session = genau eine neue Zeile, dadurch bleiben die Diffs lesbar.

```json
{
  "date": "2026-10-26",
  "session": "A",
  "duration_min": 75,
  "exercises": [
    {
      "exercise": "Back Squat",
      "sets": [
        {"set": 1, "weight_kg": 50, "reps": 5, "unit": "kg", "note": "hart aber durch"}
      ]
    }
  ]
}
```

### Felder

| Feld | Bedeutung |
|---|---|
| `date` | ISO-Datum |
| `session` | `A` (Squat + Press), `B` (Deadlift + Bench), `CARDIO` |
| `duration_min` | optional, Gesamtdauer |
| `exercises[].exercise` | Übungsname |
| `exercises[].sets[].set` | Satznummer |
| `exercises[].sets[].weight_kg` | Gesamtgewicht; fehlt bei Körpergewicht oder Band |
| `exercises[].sets[].reps` | Wiederholungen in diesem Satz |
| `exercises[].sets[].unit` | `kg`, `bodyweight`, `band`, `min`, `km` |
| `exercises[].sets[].note` | optional, Freitext |

Einarmige Übungen: `weight_kg` ist das Gewicht pro Hantel, `reps` gilt pro Seite (steht in `note`).
Kurzhantel-Bankdrücken: `weight_kg` ist die Summe beider Hanteln.

### Einlesen

```python
import pandas as pd, json
sessions = [json.loads(l) for l in open("sessions.jsonl")]
sets = pd.json_normalize(sessions, ["exercises", "sets"], ["date", "session"],
                         meta_prefix="", record_prefix="")
```

## Plan

Der aktuelle Plan mit Gewichten, Progression und Technik-Cues steht in [`plan.md`](plan.md).

Kontext zur Arbeitsweise — wie geloggt wird, wie gecoacht wird, was offen ist — in [`AGENTS.md`](AGENTS.md).
