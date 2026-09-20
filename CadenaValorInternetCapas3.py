import networkx as nx
import plotly.graph_objects as go
import numpy as np

np.random.seed(42)

# ============================================================
# 1. NODOS
# ============================================================
nodos = [
    ("tt_acc",           1, "Telecom-Telefónica (fusión)",    12, "operador",      True),
    ("claro_acc",        1, "América Móvil (Carlos Slim)",     8, "operador",      False),
    ("cabase",           2, "Asociación civil sin fines de lucro", 9, "ixp",       False),
    ("pit",              2, "Operador privado",                3, "ixp",           False),
    ("globenet",         3, "Operador mayorista",              6, "transporte",    False),
    ("cirion",           3, "Stonepeak (ex Lumen)",            7, "transporte",    False),
    ("tt_trans",         3, "Telecom-Telefónica (fusión)",    12, "operador",      True),
    ("arsat_trans",      3, "Estado Nacional",                 8, "estatal",       False),
    ("silica",           3, "Grupo Datco (Horacio Martínez)",  6, "transporte",    False),
    ("metrotel",         3, "Riverwood + Blackstone",          7, "transporte",    False),
    ("tt_transito",      4, "Telecom-Telefónica (fusión)",    12, "operador",      True),
    ("claro_trans",      4, "América Móvil (Carlos Slim)",     7, "operador",      False),
    ("arsat_transito",   4, "Estado Nacional",                 6, "estatal",       False),
    ("silica_transito",  4, "Grupo Datco",                     5, "transporte",    False),
    ("cirion_transito",  4, "Stonepeak",                       6, "transporte",    False),
    ("he",               4, "Mike Leber (privada)",            9, "internacional", False),
    ("netflix",          5, "Corporación global",               7, "contenido",    False),
    ("google",           5, "Alphabet (Vanguard / BlackRock)",  8, "cdn",          False),
    ("akamai",           5, "Vanguard / BlackRock / Capital Research", 6, "cdn",   False),
    ("cloudflare",       5, "Capital Group / Vanguard / BlackRock", 9, "cdn",       False),
    ("fastly",           5, "BlackRock / Vanguard / FMR",       5, "cdn",          False),
    ("amazon",           5, "Jeff Bezos / Vanguard / BlackRock", 7, "cdn",         False),
    ("meta",             5, "Corporación global",               7, "contenido",    False),
]

links = [
    ("tt_acc", "cabase", "fisico", 3),
    ("claro_acc", "cabase", "fisico", 2),
    ("cabase", "globenet", "logico", 1),
    ("cabase", "cirion", "logico", 1),
    ("cabase", "tt_trans", "logico", 3),
    ("cabase", "arsat_trans", "logico", 2),
    ("cabase", "silica", "logico", 1),
    ("pit", "cirion", "logico", 1),
    ("globenet", "tt_transito", "fisico", 2),
    ("cirion", "tt_transito", "fisico", 2),
    ("tt_trans", "tt_transito", "fisico", 6),
    ("arsat_trans", "arsat_transito", "fisico", 3),
    ("silica", "silica_transito", "fisico", 3),
    ("metrotel", "claro_trans", "logico", 1),
    ("tt_transito", "he", "logico", 3),
    ("claro_trans", "he", "logico", 1),
    ("cirion_transito", "he", "logico", 1),
    ("netflix", "tt_acc", "contenido", 2),
    ("google", "tt_acc", "contenido", 2),
    ("akamai", "tt_acc", "contenido", 2),
    ("cloudflare", "claro_acc", "contenido", 2),
    ("fastly", "cabase", "contenido", 2),
    ("amazon", "cabase", "contenido", 2),
    ("meta", "cabase", "contenido", 2),
    ("cloudflare", "cabase", "contenido", 2),
    ("google", "cabase", "contenido", 2),
    ("akamai", "cabase", "contenido", 2),
    ("netflix", "cabase", "contenido", 2),
    ("tt_acc", "tt_trans", "fisico", 6),
]

G = nx.Graph()
for nodo_id, capa, dueno, tamano, tipo, es_tt in nodos:
    G.add_node(nodo_id, capa=capa, dueno=dueno, tamano=tamano, tipo=tipo, es_tt=es_tt)
for origen, destino, tipo_link, grosor in links:
    G.add_edge(origen, destino, tipo=tipo_link, grosor=grosor)

# ============================================================
# 2. POSICIONES
# ============================================================
OFFSET_X = 8.0

distancias_entre_capas = {
    1: 18.0,
    2: 24.0,
    3: 18.0,
    4: 18.0,
}

posiciones_capa = {1: OFFSET_X}
for capa in range(2, 6):
    posiciones_capa[capa] = posiciones_capa[capa - 1] + distancias_entre_capas[capa - 1]

pos = {}
for capa in range(1, 6):
    nodos_capa = [n for n, d in G.nodes(data=True) if d["capa"] == capa]
    n = len(nodos_capa)
    x_base = posiciones_capa[capa]
    separacion = 6.5
    for i, nodo in enumerate(nodos_capa):
        x = x_base + np.random.uniform(-0.15, 0.15)
        y = (i - (n - 1) / 2) * separacion + np.random.uniform(-0.1, 0.1)
        pos[nodo] = (x, y)

# ============================================================
# 3. PALETA
# ============================================================
colores_capa = {
    1: dict(fill="#00E5FF", glow="rgba(0, 229, 255, 0.15)", fondo="rgba(0, 229, 255, 0.05)"),
    2: dict(fill="#FF6B00", glow="rgba(255, 107, 0, 0.15)", fondo="rgba(255, 107, 0, 0.05)"),
    3: dict(fill="#00FF88", glow="rgba(0, 255, 136, 0.15)", fondo="rgba(0, 255, 136, 0.05)"),
    4: dict(fill="#FF0055", glow="rgba(255, 0, 85, 0.15)", fondo="rgba(255, 0, 85, 0.05)"),
    5: dict(fill="#B026FF", glow="rgba(176, 38, 255, 0.15)", fondo="rgba(176, 38, 255, 0.05)"),
}

colores_link = {
    "fisico":    dict(core="#00E5FF", glow="rgba(0, 229, 255, 0.12)", width_core=3.0, width_glow=8.0, nombre="Links Físicos"),
    "logico":    dict(core="#FF6B00", glow="rgba(255, 107, 0, 0.12)", width_core=2.6, width_glow=7.0, nombre="Links Lógicos"),
    "contenido": dict(core="#FF00AA", glow="rgba(255, 0, 170, 0.10)", width_core=1.8, width_glow=5.0, nombre="Links de Contenido"),
}

# ============================================================
# 4. NOMBRES PERSONALIZADOS
# ============================================================
nombres_personalizados = {
    "tt_acc": "Telecom-Telefónica Fusión",
    "tt_trans": "Telecom-Telefónica Fusión",
    "tt_transito": "Telecom-Telefónica Fusión",
    "arsat_trans": "ARSAT",
    "arsat_transito": "ARSAT",
    "claro_acc": "Claro",
    "claro_trans": "Claro",
    "cirion_transito": "Cirion",
    "silica_transito": "Silica",
    "he": "Hurricane Electric",
}

def partir_nombre(nombre):
    if nombre == "Telecom-Telefónica Fusión":
        return "Telecom-<br>Telefónica<br>Fusión"
    if nombre == "Hurricane Electric":
        return "Hurricane<br>Electric"
    partes = nombre.split()
    if len(partes) <= 1:
        return nombre
    if len(nombre) > 12:
        mitad = len(partes) // 2
        linea1 = " ".join(partes[:mitad])
        linea2 = " ".join(partes[mitad:])
        return f"{linea1}<br>{linea2}"
    return nombre

def nombre_mostrar(nodo):
    if nodo in nombres_personalizados:
        return nombres_personalizados[nodo]
    return nodo.replace("_", " ").title()

# ============================================================
# 5. DIBUJO
# ============================================================
fig = go.Figure()

etiquetas_capa = {
    1: "Capa 1: Acceso (ISPs)",
    2: "Capa 2: Interconexión (IXP)",
    3: "Capa 3: Transporte Global",
    4: "Capa 4: Tránsito IP",
    5: "Capa 5: Contenido (CDN/CP)",
}

# Ajuste fino de la posición X de cada etiqueta
ajustes_etiqueta_x = {
    1: 0.0,      # sin ajuste
    2: 3.0,      # <-- mover +3 hacia la derecha para centrarla entre Capa 1 y Capa 3
    3: 0.0,
    4: 0.0,
    5: 0.0,
}

# --- 5a. Columnas verticales de fondo ---
for capa in range(1, 6):
    nodos_capa = [n for n, d in G.nodes(data=True) if d["capa"] == capa]
    if not nodos_capa:
        continue
    ys = [pos[n][1] for n in nodos_capa]
    y_min = min(ys) - 3.5
    y_max = max(ys) + 3.5
    x_centro = posiciones_capa[capa]
    ancho = 6.5

    fig.add_shape(
        type="rect",
        x0=x_centro - ancho / 2, x1=x_centro + ancho / 2,
        y0=y_min, y1=y_max,
        fillcolor=colores_capa[capa]["fondo"],
        line=dict(color=colores_capa[capa]["glow"], width=2),
        layer="below",
    )

# --- 5b. Links con glow ---
indices_links_glow = {}
indices_links_core = {}

for tipo_link, estilo in colores_link.items():
    xs_glow, ys_glow = [], []
    xs_core, ys_core = [], []

    for origen, destino, data in G.edges(data=True):
        if data["tipo"] != tipo_link:
            continue
        x0, y0 = pos[origen]
        x1, y1 = pos[destino]
        xs_glow += [x0, x1, None]; ys_glow += [y0, y1, None]
        xs_core += [x0, x1, None]; ys_core += [y0, y1, None]

    idx_glow = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs_glow, y=ys_glow, mode="lines",
        line=dict(color=estilo["glow"], width=estilo["width_glow"]),
        hoverinfo="none", showlegend=False,
        legendgroup=f"links_glow_{tipo_link}",
        name=f"{estilo['nombre']} (glow)",
    ))
    indices_links_glow[tipo_link] = idx_glow

    idx_core = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs_core, y=ys_core, mode="lines",
        line=dict(color=estilo["core"], width=estilo["width_core"]),
        name=estilo["nombre"], hoverinfo="none",
        legendgroup=f"links_{tipo_link}",
    ))
    indices_links_core[tipo_link] = idx_core

# --- 5c. Nodos ---
indices_nodos_normal = {}
indices_nodos_atenuado = {}

# NORMALES
for capa in range(1, 6):
    nodos_capa = [n for n, d in G.nodes(data=True) if d["capa"] == capa]
    xs, ys, tamanos, textos, hovertexts, colores = [], [], [], [], [], []
    for nodo in nodos_capa:
        data = G.nodes[nodo]
        x, y = pos[nodo]
        xs.append(x); ys.append(y)
        tamanos.append(data["tamano"] * 7.5)

        nombre = nombre_mostrar(nodo)
        textos.append(partir_nombre(nombre))
        hovertexts.append(
            f"<b>{nombre}</b><br>"
            f"<b>Capa:</b> {data['capa']}<br>"
            f"<b>Dueño:</b> {data['dueno']}<br>"
            f"<b>Conexiones:</b> {G.degree(nodo)}"
        )
        colores.append(colores_capa[capa]["fill"])

    idx_halo_norm = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(size=[t * 1.8 for t in tamanos],
                    color=colores_capa[capa]["glow"],
                    line=dict(width=0)),
        hoverinfo="none", showlegend=False, visible=True,
        legendgroup=f"nodos_glow_{capa}",
        name=f"Halo {etiquetas_capa[capa]}",
    ))
    idx_nucleo_norm = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        marker=dict(size=tamanos, color=colores,
                    line=dict(width=1.5, color="rgba(255,255,255,0.9)"),
                    opacity=0.92),
        text=[f"<span style='background-color:rgba(255,255,255,0.7);color:#000000;padding:2px 3px;'>{t}</span>" for t in textos],
        textposition="middle center",
        textfont=dict(
            size=13,
            color="#000000",
            family="Verdana, Arial Black, sans-serif",
        ),
        hovertext=hovertexts, hoverinfo="text", visible=True,
        name=etiquetas_capa[capa],
        legendgroup=f"nodos_{capa}",
    ))
    indices_nodos_normal[capa] = (idx_halo_norm, idx_nucleo_norm)

# ATENUADAS
for capa in range(1, 6):
    nodos_capa = [n for n, d in G.nodes(data=True) if d["capa"] == capa]
    xs, ys, tamanos, textos, colores = [], [], [], [], []
    for nodo in nodos_capa:
        data = G.nodes[nodo]
        x, y = pos[nodo]
        xs.append(x); ys.append(y)
        tamanos.append(data["tamano"] * 7.5)
        textos.append(partir_nombre(nombre_mostrar(nodo)))
        colores.append(colores_capa[capa]["fill"])

    idx_halo_at = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(size=[t * 1.8 for t in tamanos],
                    color="rgba(100, 100, 100, 0.05)",
                    line=dict(width=0)),
        hoverinfo="none", showlegend=False, visible=False,
        legendgroup=f"nodos_glow_at_{capa}",
        name=f"Halo Atenuado {etiquetas_capa[capa]}",
    ))
    idx_nucleo_at = len(fig.data)
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        marker=dict(size=tamanos, color=colores,
                    line=dict(width=1.0, color="rgba(150,150,150,0.3)"),
                    opacity=0.15),
        text=textos, textposition="middle center",
        textfont=dict(
            size=13,
            color="rgba(150,150,150,0.4)",
            family="Verdana, Arial Black, sans-serif",
        ),
        hoverinfo="skip", showlegend=False, visible=False,
        name=f"{etiquetas_capa[capa]} (atenuada)",
        legendgroup=f"nodos_at_{capa}",
    ))
    indices_nodos_atenuado[capa] = (idx_halo_at, idx_nucleo_at)

# --- 5d. Etiquetas de capa (con ajuste fino de posición X) ---
y_max_global = max(pos[n][1] for n in G.nodes())
y_etiqueta = y_max_global + 5.5

for capa in range(1, 6):
    x_etiqueta = posiciones_capa[capa] + ajustes_etiqueta_x[capa]

    fig.add_annotation(
        x=x_etiqueta, y=y_etiqueta,
        text=f"<b>{etiquetas_capa[capa].upper()}</b>",
        showarrow=False,
        font=dict(size=15, color=colores_capa[capa]["fill"],
                  family="Courier New, monospace"),
        bgcolor="rgba(10, 10, 26, 0.9)",
        bordercolor=colores_capa[capa]["fill"], borderwidth=1,
    )

# ============================================================
# 5e. ÍCONO DEL USUARIO FINAL
# ============================================================
fig.add_annotation(
    x=-13.0, y=0,
    text="<span style='font-size:110px'>👩‍💻</span>",
    showarrow=False,
    xanchor="center", yanchor="middle",
)

fig.add_annotation(
    x=-13.0, y=-10.0,
    text="<b>USUARIO<br>FINAL</b>",
    showarrow=False,
    font=dict(size=14, color="#88DDEE", family="Courier New, monospace"),
    xanchor="center", yanchor="middle",
    bgcolor="rgba(10, 10, 26, 0.8)",
    bordercolor="#88DDEE", borderwidth=1,
)

# ============================================================
# 6. BOTONES
# ============================================================
n_trazas = len(fig.data)

botones_capa = []
for capa_sel in range(1, 6):
    vis = [True] * n_trazas
    for capa in range(1, 6):
        idx_h_norm, idx_n_norm = indices_nodos_normal[capa]
        idx_h_at, idx_n_at = indices_nodos_atenuado[capa]
        if capa == capa_sel:
            vis[idx_h_norm] = True
            vis[idx_n_norm] = True
            vis[idx_h_at] = False
            vis[idx_n_at] = False
        else:
            vis[idx_h_norm] = False
            vis[idx_n_norm] = False
            vis[idx_h_at] = True
            vis[idx_n_at] = True
    botones_capa.append(dict(
        label=etiquetas_capa[capa_sel],
        method="update",
        args=[{"visible": vis}],
    ))

botones_edge = []
for tipo_link, estilo in colores_link.items():
    vis = [True] * n_trazas
    vis[indices_links_glow[tipo_link]] = False
    vis[indices_links_core[tipo_link]] = False
    botones_edge.append(dict(
        label=estilo["nombre"],
        method="update",
        args=[{"visible": vis}],
    ))

boton_todo = dict(
    label="Mostrar todo",
    method="update",
    args=[{"visible": [True] * n_trazas}],
)

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.60, y=-0.18, xanchor="center", yanchor="top",
            pad=dict(r=16, t=16),
            showactive=True,
            buttons=[boton_todo] + botones_capa + botones_edge,
            bgcolor="rgba(10, 10, 26, 0.95)",
            bordercolor="#00E5FF",
            font=dict(color="#00E5FF", family="Courier New, monospace", size=14),
        ),
    ],
    annotations=list(fig.layout.annotations) + [
        dict(
            x=0.60, y=-0.10, xref="paper", yref="paper",
            text="<i>Hacé clic en un botón para atenuar el resto y resaltar esa capa o tipo de link.</i>",
            showarrow=False,
            font=dict(size=13, color="#88DDEE", family="Courier New, monospace"),
            xanchor="center",
        ),
    ],
)

# ============================================================
# 7. LAYOUT
# ============================================================
fig.update_layout(
    title=dict(
        text="<b>◢ CADENA DE VALOR DE INTERNET — ARGENTINA ◣</b><br>"
             "<sub>// Vista cyberpunk · Arrastrá para explorar · Scroll para zoom</sub>",
        font=dict(family="Courier New, monospace", size=24, color="#00E5FF"),
        x=0.5, xanchor="center",
    ),
    showlegend=True,
    legend=dict(
        orientation="v", yanchor="top", y=0.95, xanchor="left", x=1.02,
        bgcolor="rgba(10, 10, 26, 0.95)",
        bordercolor="#00E5FF", borderwidth=1,
        font=dict(family="Courier New, monospace", size=13, color="#00E5FF"),
    ),
    hovermode="closest",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
               showline=False, range=[-24.0, 100.0]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False,
               showline=False, range=[-25.0, 27.0],
               scaleanchor="x", scaleratio=1),
    plot_bgcolor="#0A0A1A",
    paper_bgcolor="#0A0A1A",
    font=dict(family="Courier New, monospace", size=13, color="#DDD"),
    autosize=True,
    margin=dict(l=0, r=0, t=200, b=220),
)

# ============================================================
# 8. EXPORTAR CON CSS
# ============================================================
html_string = fig.to_html(
    config={
        "displayModeBar": True,
        "displaylogo": False,
        "scrollZoom": True,
        "responsive": True,
        "modeBarButtonsToRemove": ["lasso2d", "select2d"],
        "toImageButtonOptions": {
            "format": "png",
            "filename": "cadena_valor_internet",
            "height": 1080,
            "width": 1920,
            "scale": 2,
        },
    },
    full_html=True,
    include_plotlyjs="cdn",
)

css = """
<style>
    html, body {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background-color: #0A0A1A;
    }
    .plotly-graph-div {
        width: 100vw !important;
        height: 100vh !important;
    }
    .updatemenu-button {
        background-color: rgba(0, 229, 255, 0.08) !important;
        border: 1px solid #00E5FF !important;
        color: #00E5FF !important;
        font-weight: bold !important;
        padding: 10px 18px !important;
        margin: 4px !important;
        border-radius: 4px !important;
        font-size: 15px !important;
    }
    .updatemenu-button:hover {
        background-color: rgba(0, 229, 255, 0.3) !important;
        color: #FFFFFF !important;
    }
    .modebar {
        background-color: rgba(10, 10, 26, 0.9) !important;
        border: 1px solid #00E5FF !important;
        border-radius: 4px !important;
        padding: 4px !important;
        top: 10px !important;
        right: 10px !important;
    }
    .modebar-btn path {
        fill: #00E5FF !important;
        stroke: #00E5FF !important;
    }
    .modebar-btn:hover path {
        fill: #FFFFFF !important;
        stroke: #FFFFFF !important;
    }
</style>
"""

html_string = html_string.replace("</head>", css + "</head>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_string)

print("✅ Gráfico exportado a index.html")
print(f"Nodos: {G.number_of_nodes()} | Links: {G.number_of_edges()}")