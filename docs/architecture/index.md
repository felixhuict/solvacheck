# Architecture

## Overview

SolvaCheck is a **monolithic single-file Streamlit application**. All application logic lives in `main.py` (~562 lines). There is no separate backend, database, or build step — the Streamlit server renders the UI directly from Python functions.

```
┌─────────────────────────────────────────────────┐
│                  Browser (UI)                   │
│        Streamlit multi-page navigation          │
│  ┌────────────┐ ┌────────────┐ ┌─────────────┐  │
│  │Compatibility│ │  Solvents  │ │ Ingredients │  │
│  │  Checker   │ │  Library   │ │   Library   │  │
│  └─────┬──────┘ └─────┬──────┘ └─────────────┘  │
└────────┼──────────────┼─────────────────────────┘
         │              │
┌────────▼──────────────▼─────────────────────────┐
│               main.py (Python)                  │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │           Hansen Math Layer              │   │
│  │  hansen_distance()  classify_compat..()  │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │         Visualization Layer              │   │
│  │  create_2d_plots()  create_3d_plot()     │   │
│  │  create_hansen_sphere()                  │   │
│  └──────────────────────────────────────────┘   │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │           Persistence Layer              │   │
│  │  _load_json()  _save_json()              │   │
│  │  load_solvents()  save_solvents()        │   │
│  │  load_ingredients()  add_solvent()       │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────┘
                       │ read / write
              ┌────────┴────────┐
              │  Local FS (JSON)│
              │  solvents.json  │
              │  ingredients.json│
              └─────────────────┘
```

---

## File Structure

```
afiefah/
├── main.py                  # Entire application (562 lines)
├── pyproject.toml           # Project metadata and dependencies
├── uv.lock                  # Pinned dependency tree (UV)
├── .python-version          # Python version pin (3.12)
├── .gitignore
├── README.md
├── solvents.json            # Solvent library (runtime-generated, git-ignored)
├── ingredients.json         # Ingredient library (runtime-generated, git-ignored)
└── .streamlit/
    └── config.toml          # Streamlit UI theme
```

---

## Layers Inside `main.py`

| Lines | Layer | Responsibility |
|---|---|---|
| 1–36 | Bootstrap & styles | Page config, CSS injection via `st.html` |
| 39–44 | Constants | File paths, Ra thresholds |
| 47–99 | Default data | Hardcoded fallback solvents and ingredients |
| 102–137 | Persistence | JSON read/write helpers |
| 139–157 | Hansen math | Ra distance formula and compatibility classification |
| 159–354 | Visualization | Plotly 2D/3D figure factories |
| 356–367 | UI components | Metric card HTML helper |
| 370–466 | Page: Compatibility | Main analysis interface |
| 469–526 | Page: Solvents | Solvent CRUD and CSV import |
| 529–551 | Page: Ingredients | Read-only ingredient table |
| 554–561 | Navigation | `st.navigation` router |

---

## Design Decisions

**Single file.** The entire application is one `main.py`. This keeps deployment trivial (no package to install, no import paths to configure) and is appropriate for a tool of this scope.

**No database.** Persistence is plain JSON on the local filesystem. This avoids any infrastructure dependency and is sufficient for a local research tool with small datasets (tens of ingredients, tens of solvents).

**Functional, not object-oriented.** All logic is expressed as module-level functions. There are no classes. This matches the Streamlit execution model, where the entire script re-runs on every user interaction.

**JSON files are git-ignored.** `solvents.json` and `ingredients.json` are treated as runtime state, not source code. The application seeds them from embedded Python defaults on first run, so the repository remains clean.
