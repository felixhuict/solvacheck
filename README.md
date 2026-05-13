# SolvaCheck

A research tool for checking solvent–ingredient compatibility using **Hansen Solubility Parameters (HSP)**.

Given a solvent, SolvaCheck calculates the Hansen distance (Ra) to each cosmetic ingredient and classifies the compatibility:

| Ra | Classification |
|----|----------------|
| < 5 | Goed compatibel |
| 5 – 10 | Matig compatibel |
| > 10 | Incompatibel |

---

## Requirements

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) (package manager)

---

## Getting started

### 1. Clone the repository

```bash
git clone <repository-url>
cd afiefah
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the app

```bash
uv run streamlit run main.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Project structure

```
afiefah/
├── main.py              # Application entry point
├── solvents.json        # Solvent library (auto-generated on first run)
├── ingredients.json     # Cosmetic ingredient library (auto-generated on first run)
├── pyproject.toml       # Project metadata and dependencies
├── .streamlit/
│   └── config.toml      # UI theme
└── .gitignore
```

> `solvents.json` and `ingredients.json` are excluded from version control.
> They are generated from the defaults in `main.py` on first run.

---

## Adding data

### Solvents
Go to the **Solventen** page in the app. You can:
- Add a single solvent manually (name, δD, δP, δH)
- Upload a CSV file with columns: `name`, `dD`, `dP`, `dH`

### Ingredients
Ingredient data is defined in `DEFAULT_INGREDIENTS` inside `main.py`.
To add a new ingredient, append an entry:

```python
{
    "name": "Your ingredient",
    "dD": 17.0,
    "dP": 8.0,
    "dH": 5.0,
    "hsp_method": "Predicted",       # or "Determined"
    "molar_volume": 300.0,           # optional, cm³/mol
    "melting_point_c": 120.0,        # optional, °C
}
```

Then delete `ingredients.json` and restart the app to regenerate it.

---

## HSP background

Hansen Solubility Parameters split the total solubility parameter into three components:

- **δD** — dispersion interactions
- **δP** — polar interactions
- **δH** — hydrogen-bonding interactions

The Hansen distance between a solvent and an ingredient is:

$$R_a = \sqrt{4(\delta D_1 - \delta D_2)^2 + (\delta P_1 - \delta P_2)^2 + (\delta H_1 - \delta H_2)^2}$$

The factor 4 on the δD term is a convention introduced by Hansen to make the sphere a better fit to experimental solubility data.
