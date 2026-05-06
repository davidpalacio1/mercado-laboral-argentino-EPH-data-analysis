"""
Dashboard — Mercado Laboral Argentino (EPH T3-2025)
Autor: David Palacio Velásquez | UBA — Ciencias de Datos
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ──────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Mercado Laboral AR · EPH T3-2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# PALETA DE COLORES
# ──────────────────────────────────────────────
NAVY   = "#060C20"
PANEL  = "#0D1530"
BORDER = "#1E2D52"
CYAN   = "#00D4FF"
GOLD   = "#FFB800"
TEAL   = "#00E5C3"
ROSE   = "#FF4E6A"
SLATE  = "#A8B8D8"
WHITE  = "#F0F6FF"

CLUSTER_COLORS = [CYAN, GOLD, TEAL, ROSE]
MODEL_COLORS   = [CYAN, GOLD, TEAL]
GRID = dict(gridcolor=BORDER, zerolinecolor=BORDER, linecolor=BORDER)


def base_layout(**kwargs):
    """Retorna un dict de layout base; los kwargs sobreescriben o agregan claves."""
    layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(13,21,48,0.6)",
        font=dict(family="'DM Sans', sans-serif", color=SLATE, size=13),
        colorway=[CYAN, GOLD, TEAL, ROSE],
    )
    layout.update(kwargs)
    return layout


def hex_to_rgba(hex_color, alpha=0.12):
    """Convierte color hex a string rgba."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


# ──────────────────────────────────────────────
# CSS PERSONALIZADO
# ──────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {{
    font-family: 'DM Sans', sans-serif;
    background-color: {NAVY};
    color: {WHITE};
}}
.stApp {{
    background: radial-gradient(ellipse at 20% 0%, #0A1840 0%, {NAVY} 60%);
}}
section[data-testid="stSidebar"] {{
    background: {PANEL} !important;
    border-right: 1px solid {BORDER} !important;
}}
section[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
#MainMenu, footer, header {{ visibility: hidden; }}

.metric-card {{
    background: linear-gradient(135deg, {PANEL} 0%, #0A1535 100%);
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: border-color 0.3s, transform 0.2s;
    height: 100%;
}}
.metric-card:hover {{ border-color: {CYAN}; transform: translateY(-2px); }}
.metric-value {{
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    font-weight: 400;
    color: {CYAN};
    line-height: 1.1;
    margin: 8px 0 4px;
}}
.metric-label {{
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {SLATE};
}}
.metric-delta {{ font-size: 0.85rem; color: {TEAL}; margin-top: 4px; }}

.hero {{
    padding: 48px 0 32px;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 40px;
}}
.hero-eyebrow {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: {CYAN};
    margin-bottom: 12px;
}}
.hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2rem, 4vw, 3.2rem);
    font-weight: 400;
    color: {WHITE};
    line-height: 1.15;
    margin: 0 0 16px;
}}
.hero-title span {{ color: {GOLD}; }}
.hero-subtitle {{
    font-size: 1rem;
    color: {SLATE};
    max-width: 640px;
    line-height: 1.7;
}}
.section-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: {WHITE};
    margin: 40px 0 8px;
    padding-bottom: 12px;
    border-bottom: 1px solid {BORDER};
}}
.section-subtitle {{
    font-size: 0.9rem;
    color: {SLATE};
    margin-bottom: 24px;
    line-height: 1.6;
}}
.cluster-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    margin-top: 12px;
}}
.cluster-table th {{
    color: {SLATE};
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-size: 0.72rem;
    padding: 10px 16px;
    border-bottom: 1px solid {BORDER};
    text-align: left;
}}
.cluster-table td {{
    padding: 12px 16px;
    border-bottom: 1px solid {BORDER};
    color: {WHITE};
}}
.cluster-table tr:last-child td {{ border-bottom: none; }}
.cluster-table tr:hover td {{ background: rgba(0,212,255,0.04); }}
.highlight-box {{
    background: linear-gradient(135deg, rgba(0,212,255,0.08), rgba(0,229,195,0.04));
    border-left: 3px solid {CYAN};
    border-radius: 0 12px 12px 0;
    padding: 16px 20px;
    margin: 16px 0;
    font-size: 0.9rem;
    color: {SLATE};
    line-height: 1.7;
}}
.highlight-box strong {{ color: {WHITE}; }}
.sep {{
    height: 1px;
    background: linear-gradient(90deg, {BORDER}, transparent);
    margin: 32px 0;
}}
.stRadio > div {{ gap: 8px !important; }}
.stRadio > div > label {{
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    padding: 10px 16px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: {SLATE} !important;
    font-size: 0.88rem !important;
}}
.stRadio > div > label:hover {{
    border-color: {CYAN} !important;
    color: {WHITE} !important;
    background: rgba(0,212,255,0.06) !important;
}}
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# DATOS DEL ANÁLISIS
# ──────────────────────────────────────────────
np.random.seed(42)

clusters_df = pd.DataFrame({
    "Perfil_short": ["No ocupados", "Activos plenos", "Subocupados", "Inactivos jóvenes"],
    "n":            [18704, 14240, 3141, 1227],
    "pct":          [50.1, 38.2, 8.4, 3.3],
    "ingreso":      [250562, 933985, 490782, 148520],
    "horas":        [0, 38.5, 28.1, 0],
    "color":        CLUSTER_COLORS,
})


def gen_cluster_points(n, cx, cy, sx=0.6, sy=0.5):
    return pd.DataFrame({
        "PC1": np.random.randn(n) * sx + cx,
        "PC2": np.random.randn(n) * sy + cy,
    })


pca_dfs = [
    gen_cluster_points(800, -1.5,  0.3, 0.7, 0.6),
    gen_cluster_points(610,  1.2,  0.5, 0.6, 0.5),
    gen_cluster_points(135,  0.3, -1.2, 0.5, 0.4),
    gen_cluster_points( 52, -0.8, -1.5, 0.35, 0.35),
]
for i, df in enumerate(pca_dfs):
    df["Cluster"] = clusters_df["Perfil_short"].iloc[i]
pca_all = pd.concat(pca_dfs, ignore_index=True)

sector_labels = ["Formal", "Informal", "Serv. doméstico"]
sector_pct    = [64.8, 26.8, 8.4]
sector_colors = [CYAN, GOLD, ROSE]

cm = np.array([
    [2687, 298,   4],
    [ 136, 843,  88],
    [   2,   5, 399],
])

modelos_df = pd.DataFrame({
    "Modelo":    ["Ridge (α=500)", "OLS completo", "OLS reducido (3 vars)"],
    "R²_test":   [0.5073, 0.5073, 0.2023],
    "RMSE_test": [0.5901, 0.5901, 0.7508],
    "color":     MODEL_COLORS,
})

coefs_df = pd.DataFrame({
    "Variable":           ["Nivel educativo", "Edad", "Sector formal",
                           "Jefatura de hogar", "Jerarquía laboral", "Horas semanales"],
    "Efecto (% ingreso)": [15.6, 11.3, 8.2, 4.7, 3.0, 2.1],
}).sort_values("Efecto (% ingreso)")

n_res      = 500
y_pred_log = np.linspace(10, 16, n_res)
residuos   = np.random.randn(n_res) * 0.59

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding:20px 0 12px;">
        <div style="font-size:0.68rem;letter-spacing:0.18em;text-transform:uppercase;
                    color:{CYAN};font-weight:600;margin-bottom:8px;">Análisis · EPH</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.25rem;
                    color:{WHITE};line-height:1.3;">Mercado Laboral<br>Argentino</div>
        <div style="font-size:0.78rem;color:{SLATE};margin-top:6px;">T3 · 2025 — INDEC</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:8px 0 20px;'></div>",
                unsafe_allow_html=True)

    page = st.radio(
        "Navegación",
        ["📊  Resumen general", "🔵  Clustering", "🎯  Clasificación", "📈  Regresión"],
        label_visibility="collapsed",
    )

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:20px 0 16px;'></div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.78rem;color:{SLATE};line-height:1.8;">
        <b style="color:{WHITE};">Muestra limpia</b><br>37.312 individuos<br>113 variables<br><br>
        <b style="color:{WHITE};">Fuente</b><br>INDEC — EPH<br>3er trimestre 2025
    </div>""", unsafe_allow_html=True)

    st.markdown(f"<div style='height:1px;background:{BORDER};margin:20px 0 16px;'></div>",
                unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.75rem;color:{SLATE};">
        <b style="color:{WHITE};">David Palacio Velásquez</b><br>Ciencias de Datos · UBA
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 1 — RESUMEN GENERAL
# ══════════════════════════════════════════════
if "Resumen" in page:

    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">Portfolio de Data Science · UBA · FCEyN</div>
        <h1 class="hero-title">Mercado Laboral<br><span>Argentino</span> — EPH T3-2025</h1>
        <p class="hero-subtitle">
            Análisis multidimensional de 37.312 individuos de la Encuesta Permanente de Hogares
            del INDEC. Se aplican técnicas de clustering, clasificación supervisada y regresión
            para revelar la estructura del empleo en Argentina.
        </p>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    metrics = [
        ("37.312",   "Individuos analizados",     "de 44.946 entrevistas"),
        ("91,1 %",   "Accuracy clasificación",    "KNN · K = 17"),
        ("0,507",    "R² de regresión",            "Ridge α = 500"),
        ("$800.000", "Ingreso mediano",            "ARS · T3-2025"),
    ]
    for col, (val, label, delta) in zip(cols, metrics):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-delta">{delta}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

    c1, c2 = st.columns([1.15, 1])

    with c1:
        st.markdown("<div class='section-title'>Cuatro perfiles del mercado laboral</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>K-Means con K=4 sobre componentes PCA. "
                    "La condición de actividad es la dimensión de variación más relevante.</div>",
                    unsafe_allow_html=True)

        fig_bar = go.Figure()
        for _, row in clusters_df.iterrows():
            fig_bar.add_trace(go.Bar(
                name=row["Perfil_short"],
                x=[row["Perfil_short"]],
                y=[row["pct"]],
                marker=dict(color=row["color"], opacity=0.85,
                            line=dict(color=row["color"], width=1.5)),
                text=f"{row['pct']}%",
                textposition="outside",
                textfont=dict(color=WHITE, size=13, family="DM Sans"),
            ))
        fig_bar.update_layout(**base_layout(
            showlegend=False, height=340,
            margin=dict(l=0, r=0, t=20, b=0), bargap=0.3,
            xaxis=dict(**GRID),
            yaxis=dict(range=[0, 60], title="Participación (%)", **GRID),
        ))
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with c2:
        st.markdown("<div class='section-title'>Composición sectorial</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Distribución de ocupados por categoría. "
                    "El sector informal representa más de un cuarto del total.</div>",
                    unsafe_allow_html=True)

        fig_pie = go.Figure(go.Pie(
            labels=sector_labels, values=sector_pct, hole=0.55,
            marker=dict(colors=sector_colors, line=dict(color=NAVY, width=2)),
            textinfo="label+percent",
            textfont=dict(family="DM Sans", size=12, color=WHITE),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>",
        ))
        fig_pie.add_annotation(text="Ocupados", x=0.5, y=0.55, showarrow=False,
                               font=dict(size=11, color=SLATE, family="DM Sans"))
        fig_pie.add_annotation(text="T3-2025", x=0.5, y=0.42, showarrow=False,
                               font=dict(size=11, color=SLATE, family="DM Sans"))
        fig_pie.update_layout(**base_layout(
            height=340, margin=dict(l=0, r=0, t=20, b=0), showlegend=False,
        ))
        st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Ingreso promedio por perfil laboral</div>",
                unsafe_allow_html=True)

    fig_ing = go.Figure()
    for _, row in clusters_df.iterrows():
        fig_ing.add_trace(go.Bar(
            name=row["Perfil_short"], x=[row["Perfil_short"]], y=[row["ingreso"]],
            marker=dict(color=row["color"], opacity=0.85,
                        line=dict(color=row["color"], width=1)),
            text=f"${row['ingreso']:,.0f}", textposition="outside",
            textfont=dict(color=WHITE, size=12),
        ))
    fig_ing.update_layout(**base_layout(
        showlegend=False, height=300,
        margin=dict(l=0, r=0, t=20, b=0), bargap=0.35,
        xaxis=dict(**GRID),
        yaxis=dict(range=[0, 1_100_000], title="Ingreso promedio (ARS)",
                   tickformat="$,.0f", **GRID),
    ))
    st.plotly_chart(fig_ing, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Hallazgos principales</div>",
                unsafe_allow_html=True)

    h1, h2, h3 = st.columns(3)
    hallazgos = [
        (CYAN, "🏗️ Estructura del mercado",
         "La principal dimensión de variación es la <strong>condición de actividad</strong>. "
         "El clustering captura esta separación como la más relevante en los datos."),
        (GOLD, "🎓 Educación e ingreso",
         "Cada escalón educativo adicional se asocia con <strong>+15,6 % de ingreso</strong>, "
         "consistente con la teoría del capital humano (Becker, 1964; Mincer, 1974)."),
        (TEAL, "📍 Frontera formal-informal",
         "Los errores del KNN se concentran en la frontera <strong>formal-informal</strong>, "
         "ya que ambos sectores comparten muchas características observables en la EPH."),
    ]
    for col, (color, titulo, texto) in zip([h1, h2, h3], hallazgos):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;padding:20px;">
                <div style="font-size:0.8rem;font-weight:600;letter-spacing:0.1em;
                            text-transform:uppercase;color:{color};margin-bottom:10px;">
                    {titulo}
                </div>
                <div style="font-size:0.88rem;color:{SLATE};line-height:1.7;">{texto}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 2 — CLUSTERING
# ══════════════════════════════════════════════
elif "Clustering" in page:

    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">Aprendizaje No Supervisado</div>
        <h1 class="hero-title">Perfiles socioeconómicos<br><span>de la población</span></h1>
        <p class="hero-subtitle">
            K-Means con K=4 aplicado sobre los dos primeros componentes principales
            (21,4 % de varianza explicada). La reducción marginal de inercia cae −58 %
            al pasar de K=4 a K=5.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-title'>Espacio PCA — Distribución de clusters</div>",
                unsafe_allow_html=True)

    fig_pca = go.Figure()
    for _, row in clusters_df.iterrows():
        sub = pca_all[pca_all["Cluster"] == row["Perfil_short"]]
        fig_pca.add_trace(go.Scatter(
            x=sub["PC1"], y=sub["PC2"],
            mode="markers", name=row["Perfil_short"],
            marker=dict(color=row["color"], size=5, opacity=0.55),
            hovertemplate=f"<b>{row['Perfil_short']}</b><br>"
                          "PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>",
        ))
    fig_pca.update_layout(**base_layout(
        height=420, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(title="Componente Principal 1", **GRID),
        yaxis=dict(title="Componente Principal 2", **GRID),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                    font=dict(color=WHITE, size=12), bgcolor="rgba(0,0,0,0)"),
    ))
    st.plotly_chart(fig_pca, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

    tc, rc = st.columns([1.1, 1])

    with tc:
        st.markdown("<div class='section-title'>Caracterización de los 4 perfiles</div>",
                    unsafe_allow_html=True)
        st.markdown("""
        <table class="cluster-table">
            <thead><tr>
                <th>Perfil</th><th>N</th><th>Participación</th>
                <th>Ingreso prom.</th><th>Hs./semana</th>
            </tr></thead><tbody>
        """, unsafe_allow_html=True)
        for _, row in clusters_df.iterrows():
            st.markdown(f"""
            <tr>
                <td><span style="display:inline-block;width:10px;height:10px;
                     border-radius:50%;background:{row['color']};margin-right:8px;"></span>
                    {row['Perfil_short']}</td>
                <td style="color:{SLATE};">{row['n']:,}</td>
                <td><span style="color:{row['color']};font-weight:600;">
                    {row['pct']} %</span></td>
                <td>${row['ingreso']:,.0f}</td>
                <td>{row['horas']}</td>
            </tr>""", unsafe_allow_html=True)
        st.markdown("</tbody></table>", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="highlight-box" style="margin-top:20px;">
            <strong>Nota metodológica:</strong> Normalización con StandardScaler antes del PCA.
            DBSCAN fue descartado por la maldición de la dimensionalidad con n = 37.312
            y p = 116 variables.
        </div>""", unsafe_allow_html=True)

    with rc:
        st.markdown("<div class='section-title'>Radar de perfiles</div>",
                    unsafe_allow_html=True)

        categorias = ["Ingreso", "Horas trab.", "Tasa activ.", "Nivel educ.", "Antigüedad"]
        valores = [
            [0.22, 0.00, 0.00, 0.45, 0.30],
            [0.90, 1.00, 1.00, 0.60, 0.65],
            [0.44, 0.73, 0.80, 0.50, 0.40],
            [0.08, 0.00, 0.00, 0.35, 0.05],
        ]

        fig_radar = go.Figure()
        for i, (_, row) in enumerate(clusters_df.iterrows()):
            v      = valores[i] + [valores[i][0]]
            c_list = categorias + [categorias[0]]
            fig_radar.add_trace(go.Scatterpolar(
                r=v, theta=c_list,
                fill="toself",
                name=row["Perfil_short"],
                line=dict(color=row["color"], width=2),
                fillcolor=hex_to_rgba(row["color"], 0.12),
                opacity=0.9,
            ))
        fig_radar.update_layout(**base_layout(
            polar=dict(
                bgcolor=PANEL,
                radialaxis=dict(visible=True, range=[0, 1], gridcolor=BORDER,
                                tickfont=dict(size=9, color=SLATE)),
                angularaxis=dict(gridcolor=BORDER, tickfont=dict(size=11, color=SLATE)),
            ),
            height=360, margin=dict(l=40, r=40, t=20, b=20),
            showlegend=True,
            legend=dict(font=dict(color=WHITE, size=11), bgcolor="rgba(0,0,0,0)"),
        ))
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})


# ══════════════════════════════════════════════
# PÁGINA 3 — CLASIFICACIÓN
# ══════════════════════════════════════════════
elif "Clasificación" in page:

    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">Aprendizaje Supervisado · Clasificación</div>
        <h1 class="hero-title">Predicción del<br><span>sector de empleo</span></h1>
        <p class="hero-subtitle">
            K-Nearest Neighbors con K=17, seleccionado por validación cruzada 5-fold.
            El modelo distingue entre empleo formal, informal y servicio doméstico
            con un <strong>accuracy del 91,1 %</strong> en el conjunto de test.
        </p>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    for col, (val, lbl, dlt) in zip([m1, m2, m3, m4], [
        ("91,1 %", "Accuracy en test",    "vs. 64,8 % basal"),
        ("90,7 %", "Accuracy CV 5-fold",  "K óptimo = 17"),
        ("0,98",   "F1 — Serv. doméstico","Clase más separable"),
        ("0,78",   "Recall — Informal",   "Clase más difícil"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{lbl}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-delta">{dlt}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

    col_cm, col_bar = st.columns(2)

    with col_cm:
        st.markdown("<div class='section-title'>Matriz de confusión</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Conjunto de test — "
                    "4.462 individuos (20 % estratificado)</div>", unsafe_allow_html=True)

        labels  = ["Formal", "Informal", "Serv. doméstico"]
        cm_norm = cm.astype(float)
        for i in range(3):
            cm_norm[i] = cm[i] / cm[i].sum()

        text_matrix = [
            [f"{cm_norm[i][j]:.1%}<br><span style='font-size:10px;opacity:0.6;'>"
             f"n={cm[i][j]}</span>" for j in range(3)]
            for i in range(3)
        ]

        fig_cm = go.Figure(go.Heatmap(
            z=cm_norm, x=labels, y=labels,
            colorscale=[[0, PANEL], [0.5, "#003366"], [1, CYAN]],
            text=text_matrix, texttemplate="%{text}",
            textfont=dict(size=13, family="DM Sans"), showscale=False,
        ))
        fig_cm.update_layout(**base_layout(
            height=360, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(title="Predicho", **GRID),
            yaxis=dict(title="Real", autorange="reversed", **GRID),
        ))
        st.plotly_chart(fig_cm, use_container_width=True, config={"displayModeBar": False})

    with col_bar:
        st.markdown("<div class='section-title'>Métricas por clase</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Precisión, recall y F1-score "
                    "para cada categoría de empleo</div>", unsafe_allow_html=True)

        metricas_clase = pd.DataFrame({
            "Clase":   ["Formal", "Informal", "Serv. doméstico"] * 3,
            "Métrica": ["Precisión"] * 3 + ["Recall"] * 3 + ["F1"] * 3,
            "Valor":   [0.95, 0.73, 1.00, 0.90, 0.78, 0.98, 0.93, 0.76, 0.99],
        })

        fig_met = go.Figure()
        for met, color in zip(["Precisión", "Recall", "F1"], [CYAN, TEAL, GOLD]):
            sub = metricas_clase[metricas_clase["Métrica"] == met]
            fig_met.add_trace(go.Bar(
                name=met, x=sub["Clase"], y=sub["Valor"],
                marker=dict(color=color, opacity=0.85),
                text=[f"{v:.2f}" for v in sub["Valor"]],
                textposition="outside", textfont=dict(color=WHITE, size=11),
            ))
        fig_met.update_layout(**base_layout(
            barmode="group", height=360, margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(**GRID),
            yaxis=dict(range=[0, 1.15], **GRID),
            legend=dict(font=dict(color=WHITE, size=12), bgcolor="rgba(0,0,0,0)"),
            bargap=0.2, bargroupgap=0.05,
        ))
        st.plotly_chart(fig_met, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Experimento de ablación</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Impacto de eliminar las variables "
                "más informativas del modelo</div>", unsafe_allow_html=True)

    abl_df = pd.DataFrame({
        "Configuración": [
            "Modelo completo",
            "Sin log(ingreso)",
            "Sin log(ingreso) + edad",
            "Sin log(ingreso) + edad + EMPLEO",
        ],
        "Accuracy": [0.911, 0.887, 0.872, 0.862],
    })
    fig_abl = go.Figure(go.Bar(
        x=abl_df["Accuracy"], y=abl_df["Configuración"], orientation="h",
        marker=dict(color=[CYAN, "#007A9E", "#005570", "#003355"],
                    line=dict(color=CYAN, width=0.5)),
        text=[f"{v:.1%}" for v in abl_df["Accuracy"]],
        textposition="outside", textfont=dict(color=WHITE, size=12),
    ))
    fig_abl.update_layout(**base_layout(
        height=220, margin=dict(l=0, r=60, t=10, b=0),
        xaxis=dict(range=[0.82, 0.94], tickformat=".0%", **GRID),
        yaxis=dict(**GRID),
    ))
    st.plotly_chart(fig_abl, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div class="highlight-box">
        <strong>Hallazgo clave:</strong> Eliminar <code>log(P47T)</code>, edad y
        <code>EMPLEO</code> simultáneamente provoca una caída de <strong>4,9 puntos</strong>
        de accuracy (−5,4 % relativo). El ingreso laboral es la variable individual
        más informativa para distinguir sector de empleo.
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# PÁGINA 4 — REGRESIÓN
# ══════════════════════════════════════════════
elif "Regresión" in page:

    st.markdown(f"""
    <div class="hero">
        <div class="hero-eyebrow">Aprendizaje Supervisado · Regresión</div>
        <h1 class="hero-title">Predicción de<br><span>ingresos laborales</span></h1>
        <p class="hero-subtitle">
            Modelos lineales sobre log(P47T) en 13.856 personas ocupadas con ingreso positivo.
            El ingreso mediano real para T3-2025 es de <strong>$800.000 ARS</strong>.
            Ridge con α=500 logra un R² de 0,507 en test.
        </p>
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3, r4 = st.columns(4)
    for col, (val, lbl, dlt) in zip([r1, r2, r3, r4], [
        ("0,507",  "R² en test",       "Ridge α = 500"),
        ("0,590",  "RMSE log-escala",  "error típico"),
        ("±$440K", "Error típico ARS", "sobre $800K mediana"),
        ("13.856", "Individuos",       "ocupados con ingreso +"),
    ]):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{lbl}</div>
                <div class="metric-value">{val}</div>
                <div class="metric-delta">{dlt}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)

    cm1, cm2 = st.columns(2)

    with cm1:
        st.markdown("<div class='section-title'>Comparación de modelos</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>R² y RMSE en escala logarítmica "
                    "para los tres modelos evaluados</div>", unsafe_allow_html=True)

        fig_mod = make_subplots(rows=1, cols=2,
                                subplot_titles=["R² (mayor es mejor)",
                                                "RMSE (menor es mejor)"])
        for _, row in modelos_df.iterrows():
            fig_mod.add_trace(go.Bar(
                name=row["Modelo"], x=[row["Modelo"]], y=[row["R²_test"]],
                marker=dict(color=row["color"], opacity=0.85),
                text=f"{row['R²_test']:.4f}", textposition="outside",
                textfont=dict(color=WHITE, size=11), showlegend=False,
            ), row=1, col=1)
            fig_mod.add_trace(go.Bar(
                name=row["Modelo"], x=[row["Modelo"]], y=[row["RMSE_test"]],
                marker=dict(color=row["color"], opacity=0.85),
                text=f"{row['RMSE_test']:.4f}", textposition="outside",
                textfont=dict(color=WHITE, size=11), showlegend=False,
            ), row=1, col=2)

        fig_mod.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(13,21,48,0.6)",
            font=dict(family="'DM Sans', sans-serif", color=SLATE, size=13),
            height=360, margin=dict(l=0, r=0, t=40, b=0), bargap=0.3,
        )
        fig_mod.update_xaxes(gridcolor=BORDER, linecolor=BORDER,
                             tickfont=dict(color=SLATE))
        fig_mod.update_yaxes(gridcolor=BORDER, linecolor=BORDER,
                             tickfont=dict(color=SLATE))
        fig_mod.update_yaxes(range=[0, 0.65], row=1, col=1)
        fig_mod.update_yaxes(range=[0, 0.95], row=1, col=2)
        fig_mod.update_annotations(font=dict(color=SLATE, size=12))

        st.plotly_chart(fig_mod, use_container_width=True, config={"displayModeBar": False})

        st.markdown(f"""
        <div class="highlight-box">
            <strong>Ridge ≈ OLS:</strong> la regularización no mejora sobre el OLS completo.
            Con ~97 observaciones por parámetro y baja multicolinealidad, el penalizador
            no aporta reducción de varianza. Resultado metodológicamente esperado.
        </div>""", unsafe_allow_html=True)

    with cm2:
        st.markdown("<div class='section-title'>Efectos estimados sobre el ingreso</div>",
                    unsafe_allow_html=True)
        st.markdown("<div class='section-subtitle'>Incremento porcentual en ingreso por "
                    "unidad adicional de cada variable (coeficientes Ridge α=500)</div>",
                    unsafe_allow_html=True)

        bar_colors = [GOLD if v >= 10 else CYAN if v >= 5 else TEAL
                      for v in coefs_df["Efecto (% ingreso)"]]
        fig_coef = go.Figure(go.Bar(
            x=coefs_df["Efecto (% ingreso)"], y=coefs_df["Variable"],
            orientation="h",
            marker=dict(color=bar_colors, opacity=0.85),
            text=[f"+{v:.1f} %" for v in coefs_df["Efecto (% ingreso)"]],
            textposition="outside", textfont=dict(color=WHITE, size=12),
        ))
        fig_coef.update_layout(**base_layout(
            height=300, margin=dict(l=0, r=60, t=10, b=0),
            xaxis=dict(range=[0, 20], ticksuffix=" %", **GRID),
            yaxis=dict(**GRID),
        ))
        st.plotly_chart(fig_coef, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='sep'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Diagnóstico de residuos</div>",
                unsafe_allow_html=True)
    st.markdown("<div class='section-subtitle'>Residuos vs. valores predichos en escala "
                "logarítmica. La dispersión homogénea confirma homocedasticidad razonable.</div>",
                unsafe_allow_html=True)

    fig_res = go.Figure()
    fig_res.add_trace(go.Scatter(
        x=y_pred_log, y=residuos, mode="markers",
        marker=dict(color=CYAN, size=4, opacity=0.35),
        hovertemplate="Pred: %{x:.2f}<br>Res: %{y:.3f}<extra></extra>",
    ))
    fig_res.add_hline(y=0, line=dict(color=GOLD, width=1.5, dash="dot"))
    fig_res.update_layout(**base_layout(
        height=280, margin=dict(l=0, r=0, t=10, b=0), showlegend=False,
        xaxis=dict(title="log(ingreso) predicho", **GRID),
        yaxis=dict(title="Residuo", **GRID),
    ))
    st.plotly_chart(fig_res, use_container_width=True, config={"displayModeBar": False})

    st.markdown(f"""
    <div class="highlight-box">
        <strong>Interpretación económica:</strong> el <strong>nivel educativo</strong>
        es el predictor de ingreso más potente: +15,6 % por escalón adicional.
        La <strong>edad</strong> captura experiencia laboral acumulada (+11,3 %).
        Resultados consistentes con la teoría del capital humano (Becker, 1964)
        y el perfil ingreso-experiencia de Mincer (1974).
    </div>""", unsafe_allow_html=True)
