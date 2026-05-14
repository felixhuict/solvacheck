# Dependencies

## Runtime

| Requirement | Version |
|---|---|
| Python | ≥ 3.12 (pinned to 3.12 via `.python-version`) |

---

## Direct Dependencies

Declared in `pyproject.toml`:

| Package | Version Constraint | Role |
|---|---|---|
| `streamlit` | ≥ 1.57.0 | Web UI framework — pages, widgets, forms, file upload |
| `plotly` | ≥ 6.7.0 | Interactive 2D scatter plots and 3D surface/scatter plots |
| `numpy` | ≥ 2.4.4 | Numerical computing — sphere mesh generation, array ops |
| `pandas` | ≥ 3.0.3 | DataFrame operations — ingredient table, distance computation |

---

## Transitive Dependencies (resolved by UV)

These are pulled in by the direct dependencies above. Exact versions are pinned in `uv.lock`.

| Package | Pulled in by | Purpose |
|---|---|---|
| `altair` | streamlit | Declarative chart support inside Streamlit |
| `anyio` | streamlit/uvicorn | Async I/O abstraction |
| `attrs` | jsonschema | Class utility library |
| `blinker` | streamlit | Signal/event system |
| `cachetools` | streamlit | In-memory caching |
| `certifi` | requests | SSL certificate bundle |
| `charset-normalizer` | requests | Character encoding detection |
| `click` | streamlit | CLI argument parsing |
| `colorama` | streamlit | Colored terminal output (Windows) |
| `gitdb` | gitpython | Git object database |
| `gitpython` | streamlit | Git integration for auto-reload |
| `h11` | uvicorn | HTTP/1.1 wire protocol |
| `httptools` | uvicorn | Fast HTTP parsing |
| `idna` | requests | Internationalized domain name support |
| `itsdangerous` | streamlit | Cookie/session signing |
| `jinja2` | altair | Template engine |
| `jsonschema` | altair | JSON schema validation |
| `markupsafe` | jinja2 | Safe HTML string handling |
| `narwhals` | altair | DataFrame abstraction layer |
| `pillow` | streamlit | Image processing |
| `protobuf` | streamlit | Protocol buffer serialization |
| `pyarrow` | streamlit | Apache Arrow columnar format |
| `pydeck` | streamlit | Deck.gl map rendering |
| `python-dateutil` | pandas | Date/time parsing utilities |
| `python-multipart` | streamlit | Multipart form data parsing |
| `referencing` | jsonschema | JSON schema reference resolution |
| `requests` | streamlit | HTTP client |
| `rpds-py` | referencing | Rust-backed persistent data structures |
| `six` | python-dateutil | Python 2/3 compatibility shims |
| `smmap` | gitdb | Sliding-window memory mapping |
| `starlette` | streamlit | ASGI framework used by Streamlit's server |
| `tenacity` | streamlit | Automatic retry logic |
| `toml` | streamlit | TOML parser |
| `typing-extensions` | various | Type hint backports |
| `tzdata` | pandas | Timezone database |
| `urllib3` | requests | Lower-level HTTP client |
| `uvicorn` | streamlit | ASGI server |
| `watchdog` | streamlit | Filesystem change detection for hot-reload |
| `websockets` | streamlit | WebSocket transport for browser ↔ server |

---

## Lockfile

All 47 transitive packages are pinned with SRI hashes in `uv.lock`. The lockfile is git-ignored (see `.gitignore`) — run `uv sync` to regenerate it from `pyproject.toml`.

> **Note:** `uv.lock` is currently listed in `.gitignore`. Consider removing it from `.gitignore` and committing the lockfile to ensure reproducible installs across environments.
