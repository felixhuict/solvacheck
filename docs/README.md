# SolvaCheck — Project Documentation

**SolvaCheck** is a single-page scientific web application for cosmetic chemistry research. It evaluates solvent-ingredient compatibility using [Hansen Solubility Parameters (HSP)](https://en.wikipedia.org/wiki/Hansen_solubility_parameter), helping formulators determine whether a solvent can dissolve or carry a given cosmetic ingredient.

---

## Quick Start

```bash
# Install dependencies
uv sync

# Run the application
uv run streamlit run main.py
```

The app is available at `http://localhost:8501` after startup.

---

## Documentation Sections

| Section | Description |
|---|---|
| [Architecture](architecture/README.md) | Application structure, layers, and module breakdown |
| [Dependencies](dependencies/README.md) | All libraries, frameworks, and runtime versions |
| [Tooling](tooling/README.md) | Package manager, dev server, and available commands |
| [Coding Patterns](coding-patterns/README.md) | Conventions, naming, data types, and UI patterns |
| [Configuration](configuration/README.md) | Config files, constants, and Streamlit theme |
| [Testing](testing/README.md) | Current test coverage status and guidance |
| [Deployment](deployment/README.md) | How to run and host the application |
| [API](api/README.md) | Internal page routing and widget interaction patterns |
| [Data Flow](data-flow/README.md) | How data moves through the application |

---

## Technology Summary

| Concern | Choice |
|---|---|
| Language | Python 3.12 |
| UI Framework | Streamlit ≥ 1.57.0 |
| Visualization | Plotly ≥ 6.7.0 |
| Data processing | NumPy ≥ 2.4.4, Pandas ≥ 3.0.3 |
| Package manager | UV |
| Persistence | Local JSON files |
| UI language | Dutch (Nederlands) |
