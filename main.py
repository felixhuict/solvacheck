import json
import os

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="HSP Compatibility",
    page_icon="🧴",
    layout="wide",
)

st.markdown(
    """
    <style>
    .metric-card {
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        border-left: 5px solid;
        margin-bottom: 0.5rem;
    }
    .metric-good     { background:#F0FBF4; border-color:#27AE60; }
    .metric-moderate { background:#FEF9F0; border-color:#E67E22; }
    .metric-bad      { background:#FDF2F2; border-color:#C0392B; }
    .metric-card .value { font-size:2.4rem; font-weight:700; margin:0; line-height:1.1; }
    .metric-card .label { font-size:0.85rem; color:#555; margin:0.2rem 0 0; }
    .metric-good     .value { color:#27AE60; }
    .metric-moderate .value { color:#E67E22; }
    .metric-bad      .value { color:#C0392B; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Constants ─────────────────────────────────────────────────

SOLVENTS_FILE   = "solvents.json"
INGREDIENTS_FILE = "ingredients.json"
RA_GOOD         = 5.0
RA_MODERATE     = 10.0


# ── Default data ──────────────────────────────────────────────

DEFAULT_SOLVENTS = [
    {"name": "DMSO",                        "dD": 18.4, "dP": 16.4, "dH": 10.2},
    {"name": "Diethyl ether/DMSO 25/75",    "dD": 17.4, "dP": 13.0, "dH":  8.9},
    {"name": "Diethyl ether/DMSO 50/50",    "dD": 16.4, "dP":  9.6, "dH":  7.6},
    {"name": "Diethyl ether/DMSO 75/25",    "dD": 15.4, "dP":  6.2, "dH":  6.3},
    {"name": "Dichloromethane",              "dD": 17.0, "dP":  7.3, "dH":  7.1},
    {"name": "Methanol",                     "dD": 14.7, "dP": 12.3, "dH": 22.3},
    {"name": "2-Propanol",                   "dD": 15.8, "dP":  6.1, "dH": 16.4},
    {"name": "Ethanol",                      "dD": 15.8, "dP":  8.8, "dH": 19.4},
    {"name": "n-Hexane",                     "dD": 14.9, "dP":  0.0, "dH":  0.0},
    {"name": "Acetonitrile",                 "dD": 15.3, "dP": 18.0, "dH":  6.1},
    {"name": "Chloroform",                   "dD": 17.8, "dP":  3.1, "dH":  5.7},
    {"name": "Diethyl ether",               "dD": 14.5, "dP":  2.9, "dH":  4.6},
    {"name": "Ethyl acetate",               "dD": 15.8, "dP":  5.3, "dH":  7.2},
    {"name": "Tetrahydrofuran",             "dD": 16.8, "dP":  5.7, "dH":  8.0},
    {"name": "N,N-Dimethylformamide",       "dD": 17.4, "dP": 13.7, "dH": 11.3},
    {"name": "1-Butanol",                   "dD": 16.0, "dP":  5.7, "dH": 15.8},
    {"name": "Toluene",                     "dD": 18.0, "dP":  1.4, "dH":  2.0},
    {"name": "l-Menthone",                  "dD": 17.0, "dP":  8.1, "dH":  4.1},
]

DEFAULT_INGREDIENTS = [
    {
        "name": "Lyco-sol™",
        "dD": 17.57, "dP": 2.48, "dH": 7.5,
        "hsp_method": "Determined",
    },
    {
        "name": "Lycopene",
        "dD": 17.3, "dP": 0.0, "dH": 1.7,
        "hsp_method": "Predicted",
        "molar_volume": 598.8, "asg": 10.2, "melting_point_c": 158.7,
    },
    {
        "name": "Matrixyl 3000",
        "dD": 19.66, "dP": 13.95, "dH": 17.55,
        "hsp_method": "Determined",
    },
    {
        "name": "Palmitoyl Tripeptide-1",
        "dD": 16.5, "dP": 20.0, "dH": 10.2,
        "hsp_method": "Predicted",
        "molar_volume": 519.7, "asg": 16.4, "melting_point_c": 178.9,
    },
    {
        "name": "Palmitoyl Tetrapeptide-7",
        "dD": 15.9, "dP": 23.8, "dH": 11.8,
        "hsp_method": "Predicted",
        "molar_volume": 588.7, "asg": 16.4, "melting_point_c": 178.9,
    },
]


# ── File helpers ──────────────────────────────────────────────

def _load_json(path: str, default: list[dict]) -> list[dict]:
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(default, f, indent=4)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path: str, data: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_solvents() -> list[dict]:
    return _load_json(SOLVENTS_FILE, DEFAULT_SOLVENTS)


def save_solvents(solvents: list[dict]) -> None:
    _save_json(SOLVENTS_FILE, solvents)


def add_solvent(name: str, dD: float, dP: float, dH: float) -> None:
    solvents = load_solvents()
    solvents.append({"name": name, "dD": float(dD), "dP": float(dP), "dH": float(dH)})
    save_solvents(solvents)


def reset_solvents() -> None:
    save_solvents(DEFAULT_SOLVENTS)


def load_ingredients() -> list[dict]:
    return _load_json(INGREDIENTS_FILE, DEFAULT_INGREDIENTS)


# ── Hansen math ───────────────────────────────────────────────

def hansen_distance(row: pd.Series, dD: float, dP: float, dH: float) -> float:
    return float(
        np.sqrt(
            4 * (row["dD"] - dD) ** 2
            + (row["dP"] - dP) ** 2
            + (row["dH"] - dH) ** 2
        )
    )


def classify_compatibility(ra: float) -> str:
    if ra < RA_GOOD:
        return "Goed compatibel"
    if ra <= RA_MODERATE:
        return "Matig compatibel"
    return "Incompatibel"


def create_hansen_sphere(
    dD: float, dP: float, dH: float, radius: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.linspace(0, 2 * np.pi, 80)
    v = np.linspace(0, np.pi, 40)
    x = dD + (radius / 2) * np.outer(np.cos(u), np.sin(v))
    y = dP + radius * np.outer(np.sin(u), np.sin(v))
    z = dH + radius * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


def create_2d_plots(
    df: pd.DataFrame,
    solvent_name: str,
    dD: float,
    dP: float,
    dH: float,
) -> list[go.Figure]:
    t = np.linspace(0, 2 * np.pi, 300)
    colors = {
        "Goed compatibel":   "#27AE60",
        "Matig compatibel":  "#E67E22",
        "Incompatibel":      "#C0392B",
    }
    symbols = {
        "Goed compatibel":   "circle",
        "Matig compatibel":  "circle",
        "Incompatibel":      "square",
    }

    # (x-axis label, y-axis label, x-column, y-column, dD-scaling on x, dD-scaling on y)
    projections = [
        ("δD", "δP", "dD", "dP", 0.5, 1.0),
        ("δD", "δH", "dD", "dH", 0.5, 1.0),
        ("δP", "δH", "dP", "dH", 1.0, 1.0),
    ]
    center = {"dD": dD, "dP": dP, "dH": dH}

    figs = []
    for i, (xl, yl, xc, yc, xs, ys) in enumerate(projections):
        fig = go.Figure()
        first = i == 0

        for ra, color, dash, zone_name in [
            (RA_MODERATE, "#E67E22", "dash",  "Ra ≤ 10"),
            (RA_GOOD,     "#27AE60", "solid", "Ra ≤ 5"),
        ]:
            fig.add_trace(go.Scatter(
                x=center[xc] + (ra * xs) * np.cos(t),
                y=center[yc] + (ra * ys) * np.sin(t),
                mode="lines",
                line=dict(color=color, width=2, dash=dash),
                name=zone_name,
                showlegend=first,
            ))

        for compat, color in colors.items():
            sub = df[df["Compatibility"] == compat]
            if len(sub) == 0:
                continue
            fig.add_trace(go.Scatter(
                x=sub[xc], y=sub[yc],
                mode="markers+text",
                text=sub["name"],
                textposition="top center",
                marker=dict(size=10, color=color, symbol=symbols[compat],
                            line=dict(width=1, color="white")),
                name=compat,
                showlegend=first,
                customdata=sub["Ra"].round(2),
                hovertemplate=(
                    "<b>%{text}</b><br>"
                    f"{xl}: %{{x}}  {yl}: %{{y}}<br>"
                    "Ra: %{customdata}<br>"
                    "<extra></extra>"
                ),
            ))

        fig.add_trace(go.Scatter(
            x=[center[xc]], y=[center[yc]],
            mode="markers+text",
            text=[solvent_name],
            textposition="bottom center",
            marker=dict(size=12, color="#1A6B8A", symbol="diamond",
                        line=dict(width=2, color="white")),
            name=solvent_name,
            showlegend=False,
            hovertemplate=(
                f"<b>{solvent_name}</b><br>"
                f"{xl}: %{{x}}  {yl}: %{{y}}<br>"
                "<extra></extra>"
            ),
        ))

        fig.update_layout(
            title=dict(text=f"{xl} vs {yl}", font=dict(size=14)),
            xaxis_title=xl,
            yaxis_title=yl,
            height=420,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor="#FFFFFF",
            legend=dict(bgcolor="rgba(255,255,255,0.8)", bordercolor="#ddd", borderwidth=1),
        )
        figs.append(fig)

    return figs


def create_3d_plot(
    df: pd.DataFrame,
    solvent_name: str,
    dD: float,
    dP: float,
    dH: float,
) -> go.Figure:
    sx5,  sy5,  sz5  = create_hansen_sphere(dD, dP, dH, RA_GOOD)
    sx10, sy10, sz10 = create_hansen_sphere(dD, dP, dH, RA_MODERATE)

    good       = df[df["Compatibility"] == "Goed compatibel"]
    moderate   = df[df["Compatibility"] == "Matig compatibel"]
    incompatible = df[df["Compatibility"] == "Incompatibel"]

    fig = go.Figure()

    fig.add_trace(go.Surface(
        x=sx10, y=sy10, z=sz10,
        opacity=0.12,
        colorscale=[[0, "#E67E22"], [1, "#F9CA8B"]],
        showscale=False, name="Ra ≤ 10 zone", hoverinfo="skip",
    ))
    fig.add_trace(go.Surface(
        x=sx5, y=sy5, z=sz5,
        opacity=0.30,
        colorscale=[[0, "#27AE60"], [1, "#A9DFBF"]],
        showscale=False, name="Ra ≤ 5 zone", hoverinfo="skip",
    ))

    def _scatter(subset: pd.DataFrame, color: str, symbol: str, label: str) -> go.Scatter3d:
        cd = subset["Ra"].round(2).values.reshape(-1, 1) if len(subset) > 0 else None
        return go.Scatter3d(
            x=subset["dD"], y=subset["dP"], z=subset["dH"],
            mode="markers+text",
            text=subset["name"],
            textposition="top center",
            marker=dict(size=8, color=color, symbol=symbol,
                        line=dict(width=1, color="white")),
            name=label,
            customdata=cd,
            hovertemplate=(
                "<b>%{text}</b><br>"
                "δD: %{x}  δP: %{y}  δH: %{z}<br>"
                "Ra: %{customdata[0]}<br>"
                "<extra></extra>"
            ),
        )

    fig.add_trace(_scatter(good,         "#27AE60", "circle", "Goed compatibel"))
    fig.add_trace(_scatter(moderate,     "#E67E22", "circle", "Matig compatibel"))
    fig.add_trace(_scatter(incompatible, "#C0392B", "square", "Incompatibel"))

    fig.add_trace(go.Scatter3d(
        x=[dD], y=[dP], z=[dH],
        mode="markers+text",
        text=[solvent_name],
        textposition="bottom center",
        marker=dict(size=11, color="#1A6B8A", symbol="diamond",
                    line=dict(width=2, color="white")),
        name=f"Solvent: {solvent_name}",
        hovertemplate=(
            f"<b>{solvent_name}</b><br>"
            "δD: %{x}  δP: %{y}  δH: %{z}<br>"
            "<extra></extra>"
        ),
    ))

    fig.update_layout(
        title=dict(
            text=f"Hansen space — <b>{solvent_name}</b> vs cosmetic ingredients",
            font=dict(size=16),
        ),
        scene=dict(
            xaxis_title="δD (dispersion)",
            yaxis_title="δP (polar)",
            zaxis_title="δH (H-bonding)",
            xaxis=dict(range=[5, 25], backgroundcolor="#F0F4F8"),
            yaxis=dict(range=[0, 30], backgroundcolor="#F0F4F8"),
            zaxis=dict(range=[0, 45], backgroundcolor="#F0F4F8"),
            aspectmode="cube",
        ),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#ddd", borderwidth=1),
        margin=dict(l=0, r=0, t=50, b=0),
        paper_bgcolor="#FFFFFF",
    )
    return fig


# ── Shared metric card helper ─────────────────────────────────

def _metric_card(value: int, label: str, css_class: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card {css_class}">
            <p class="value">{value}</p>
            <p class="label">{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Page 1: Compatibility Checker ────────────────────────────

def page_compatibility() -> None:
    st.title("Compatibility Checker")
    st.markdown(
        "Kies een solvent uit de bibliotheek (of voer eigen waarden in). "
        "De app berekent de Hansen-afstand (Ra) tot elk cosmetisch ingrediënt."
    )

    with st.expander("Hansen-formule"):
        st.latex(
            r"R_a = \sqrt{4(\delta D_1-\delta D_2)^2"
            r"+(\delta P_1-\delta P_2)^2"
            r"+(\delta H_1-\delta H_2)^2}"
        )
        st.markdown(
            "| Ra | Oordeel |\n|---|---|\n"
            "| < 5 | Goed compatibel |\n"
            "| 5 – 10 | Matig compatibel |\n"
            "| > 10 | Incompatibel |"
        )

    st.divider()

    solvents = load_solvents()
    solvent_options = ["— Custom —"] + [s["name"] for s in solvents]

    col_sel, col_vals = st.columns([1, 2], gap="large")

    with col_sel:
        selected = st.selectbox("Selecteer solvent", solvent_options, label_visibility="visible")

    if selected == "— Custom —":
        with col_vals:
            c1, c2, c3 = st.columns(3)
            sol_dD = c1.number_input("δD", 0.0, 50.0, 17.0, 0.1)
            sol_dP = c2.number_input("δP", 0.0, 50.0,  8.0, 0.1)
            sol_dH = c3.number_input("δH", 0.0, 50.0,  8.0, 0.1)
        solvent_label = "Custom solvent"
    else:
        solvent = next(s for s in solvents if s["name"] == selected)
        sol_dD, sol_dP, sol_dH = solvent["dD"], solvent["dP"], solvent["dH"]
        solvent_label = selected
        with col_vals:
            st.markdown(
                f"**δD** = {sol_dD} &nbsp;|&nbsp; "
                f"**δP** = {sol_dP} &nbsp;|&nbsp; "
                f"**δH** = {sol_dH}"
            )

    # ── Compute ───────────────────────────────────────────────
    ingredients = load_ingredients()
    df = pd.DataFrame(ingredients)
    df["Ra"] = df.apply(
        hansen_distance, axis=1, dD=sol_dD, dP=sol_dP, dH=sol_dH
    )
    df["Compatibility"] = df["Ra"].apply(classify_compatibility)

    counts       = df["Compatibility"].value_counts()
    n_good       = int(counts.get("Goed compatibel",   0))
    n_moderate   = int(counts.get("Matig compatibel",  0))
    n_incompatible = int(counts.get("Incompatibel",    0))

    # ── Metric cards ──────────────────────────────────────────
    st.markdown("###")
    m1, m2, m3 = st.columns(3)
    with m1:
        _metric_card(n_good,        "Goed compatibel  (Ra < 5)",    "metric-good")
    with m2:
        _metric_card(n_moderate,    "Matig compatibel (Ra 5 – 10)", "metric-moderate")
    with m3:
        _metric_card(n_incompatible,"Incompatibel     (Ra > 10)",   "metric-bad")

    # ── View toggle ───────────────────────────────────────────
    use_3d = st.toggle("3D weergave", value=True, key="view_toggle")

    if use_3d:
        fig = create_3d_plot(df, solvent_label, sol_dD, sol_dP, sol_dH)
        st.plotly_chart(fig, width="stretch")
    else:
        figs = create_2d_plots(df, solvent_label, sol_dD, sol_dP, sol_dH)
        c1, c2, c3 = st.columns(3)
        for col, fig in zip([c1, c2, c3], figs):
            col.plotly_chart(fig, width="stretch")

    # ── Results table ─────────────────────────────────────────
    st.subheader("Resultaten")
    display = df[["name", "dD", "dP", "dH", "Ra", "Compatibility"]].copy()
    display["Ra"] = display["Ra"].round(2)
    st.dataframe(display.sort_values("Ra"), width="stretch", hide_index=True)

    st.download_button(
        label="⬇ Download als CSV",
        data=display.sort_values("Ra").to_csv(index=False),
        file_name=f"compatibiliteit_{solvent_label.replace(' ', '_')}.csv",
        mime="text/csv",
    )


# ── Page 2: Solvent Library ───────────────────────────────────

def page_solvents() -> None:
    st.title("Solventenbibliotheek")
    st.markdown("Bekijk, voeg toe of reset de lijst met solventen.")

    solvents = load_solvents()
    st.dataframe(pd.DataFrame(solvents), width="stretch", hide_index=True)

    st.divider()
    st.subheader("Solvent toevoegen")

    with st.form("add_solvent_form"):
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        name   = c1.text_input("Naam")
        new_dD = c2.number_input("δD", 0.0, 50.0, 15.0, 0.1)
        new_dP = c3.number_input("δP", 0.0, 50.0,  5.0, 0.1)
        new_dH = c4.number_input("δH", 0.0, 50.0,  5.0, 0.1)
        submitted = st.form_submit_button("Toevoegen", type="primary")

    if submitted:
        if name.strip() == "":
            st.warning("Vul een naam in.")
        else:
            add_solvent(name.strip(), new_dD, new_dP, new_dH)
            st.success(f"'{name}' toegevoegd.")
            st.rerun()

    st.divider()
    st.subheader("Importeren via CSV")
    st.caption("Verwacht kolommen: `name` (of `naam`), `dD` (of `D`), `dP` (of `P`), `dH` (of `H`)")
    uploaded = st.file_uploader("Upload CSV", type="csv", label_visibility="collapsed")
    if uploaded is not None:
        try:
            df_up = pd.read_csv(uploaded)
            df_up.columns = df_up.columns.str.strip()
            col_map = {
                "naam": "name", "ingredient": "name",
                "d": "dD", "p": "dP", "h": "dH",
            }
            df_up = df_up.rename(columns={c: col_map[c.lower()] for c in df_up.columns if c.lower() in col_map})
            missing = {"name", "dD", "dP", "dH"} - set(df_up.columns)
            if missing:
                st.error(f"Kolommen ontbreken: {', '.join(missing)}")
            else:
                for _, row in df_up.iterrows():
                    add_solvent(str(row["name"]), float(row["dD"]), float(row["dP"]), float(row["dH"]))
                st.success(f"{len(df_up)} solventen geïmporteerd.")
                st.rerun()
        except Exception as e:
            st.error(f"Fout bij inlezen: {e}")

    st.divider()
    st.warning("Dit verwijdert alle zelfgemaakte solventen.")
    if st.button("Reset naar standaard"):
        reset_solvents()
        st.success("Lijst gereset.")
        st.rerun()


# ── Page 3: Ingredient Library ────────────────────────────────

def page_ingredients() -> None:
    st.title("Ingrediëntenbibliotheek")
    st.markdown("Overzicht van alle cosmetische ingrediënten met hun HSP-waarden.")

    ingredients = load_ingredients()
    df = pd.DataFrame(ingredients)

    display_cols = ["name", "hsp_method", "dD", "dP", "dH"]
    if "molar_volume" in df.columns:
        display_cols.append("molar_volume")
    if "melting_point_c" in df.columns:
        display_cols.append("melting_point_c")

    df_display = df[display_cols].copy()
    df_display.columns = (
        ["Naam", "HSP-methode", "δD", "δP", "δH"]
        + (["Molvolume (cm³/mol)"] if "molar_volume" in df.columns else [])
        + (["Smeltpunt (°C)"]      if "melting_point_c" in df.columns else [])
    )

    st.dataframe(df_display, width="stretch", hide_index=True)


# ── Navigation ────────────────────────────────────────────────

pg = st.navigation([
    st.Page(page_compatibility, title="Compatibility",  icon="🔍", default=True),
    st.Page(page_solvents,      title="Solventen",      icon="🧪"),
    st.Page(page_ingredients,   title="Ingrediënten",   icon="🌿"),
])
pg.run()
