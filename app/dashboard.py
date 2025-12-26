"""
SIAD - Sistema Inteligente de Análisis de Dengue
Dashboard Profesional Dark Mode - Vigilancia Epidemiológica
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================================

st.set_page_config(
    page_title="SIAD - Análisis de Dengue",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# ESTILOS CSS - DARK MODE PROFESIONAL
# ============================================================================

st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    
    <style>
    /* ===== VARIABLES GLOBALES ===== */
    :root {
        --bg-primary: #0E1117;
        --bg-secondary: #161B22;
        --color-primary: #2563EB;
        --color-success: #22C55E;
        --text-primary: #E5E7EB;
        --text-secondary: #9CA3AF;
        --border-color: #30363D;
    }
    
    /* ===== RESET Y FUENTES ===== */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    
    
    /* ===== FORZAR FONDO OSCURO ===== */
    .stApp {
        background-color: var(--bg-primary) !important;
    }
    
    /* ===== MAIN CONTAINER - PEGADO ARRIBA ===== */
    .stMain .block-container,
    .main .block-container,
    section.main > div.block-container,
    div[data-testid="stAppViewContainer"] .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
        margin-top: 0 !important;
    }
    
    /* Forzar CERO padding en TODOS los contenedores superiores */
    .stMain,
    section.main,
    div[data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Eliminar espacios superiores SOLO en el contenido principal */
    .stMain div.stVerticalBlock {
        padding-top: 0 !important;
        margin-top: 0 !important;
        gap: 0 !important;
    }
    
    /* Forzar contenedor principal arriba (solo main, no sidebar) */
    .stMain .st-emotion-cache-1j22a0y,
    .stMain .st-emotion-cache-tn0cau,
    .stMain .ek2vi383,
    .stMain [data-testid="stVerticalBlock"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    /* Eliminar padding del contenedor de la app */
    .appview-container,
    .main,
    section.main {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    
    
    /* Minimizar el header de Streamlit pero mantener botón de sidebar */
    header[data-testid="stHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        overflow: visible !important;
        background-color: transparent !important;
    }
    
    /* Asegurar que el botón de expandir sidebar sea visible */
    button[data-testid="stExpandSidebarButton"] {
        display: block !important;
        visibility: visible !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0.5rem !important;
        z-index: 999999 !important;
        background-color: var(--bg-secondary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        padding: 0.5rem !important;
        color: var(--text-primary) !important;
    }
    
    button[data-testid="stExpandSidebarButton"]:hover {
        background-color: var(--color-primary) !important;
    }
    
    /* ===== HEADER PRINCIPAL - SIN ESPACIO SUPERIOR ===== */
    .dashboard-header {
        padding: 0 0 1rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
        margin-top: 0 !important;
    }
    
    .dashboard-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }
    
    .dashboard-subtitle {
        font-size: 0.875rem;
        color: var(--text-secondary);
        margin: 0;
        font-weight: 400;
    }
    
    /* ===== TARJETAS DE MÉTRICAS - GLASSMORPHISM ===== */
    .metric-card {
        background: rgba(22, 27, 34, 0.8);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(48, 54, 61, 0.5);
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
        border-color: rgba(37, 99, 235, 0.5);
        background: rgba(22, 27, 34, 0.95);
    }
    
    .metric-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
        display: block;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover .metric-icon {
        transform: scale(1.1);
    }
    
    /* Iconos diferenciados por color */
    .metric-card:nth-child(1) .metric-icon {
        color: #2563EB;
    }
    
    .metric-card:nth-child(2) .metric-icon {
        color: #F59E0B;
    }
    
    .metric-card:nth-child(3) .metric-icon {
        color: #22C55E;
    }
    
    .metric-card:nth-child(4) .metric-icon {
        color: #8B5CF6;
    }
    
    .metric-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.25rem;
        font-weight: 700;
        color: #FFFFFF;
        font-variant-numeric: tabular-nums;
        margin-bottom: 0.25rem;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    
    .metric-delta {
        font-size: 0.75rem;
        color: var(--text-secondary);
    }
    
    /* ===== INFO BOX - COMPACTO Y ELEGANTE ===== */
    .info-box {
        background: rgba(22, 27, 34, 0.6);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-left: 3px solid var(--color-primary);
        padding: 0.875rem 1.25rem;
        border-radius: 6px;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.875rem;
        border: 1px solid rgba(48, 54, 61, 0.3);
    }
    
    .info-icon {
        color: var(--color-primary);
        font-size: 1.125rem;
        flex-shrink: 0;
    }
    
    .info-text {
        font-size: 0.8125rem;
        color: var(--text-secondary);
        line-height: 1.4;
    }
    
    .info-text strong {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* ===== SECCIONES ===== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin: 2rem 0 1.25rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid var(--border-color);
    }
    
    .section-icon {
        color: var(--color-primary);
        font-size: 1.5rem;
    }
    
    .section-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    section[data-testid="stSidebar"] > div {
        background-color: var(--bg-secondary);
        padding-top: 1rem;
    }
    
    .sidebar-header {
        padding: 1rem 0;
        border-bottom: 1px solid var(--border-color);
        margin-bottom: 1.5rem;
    }
    
    .sidebar-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .filter-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .filter-info {
        background: var(--bg-primary);
        border: 1px solid var(--border-color);
        padding: 1rem;
        border-radius: 6px;
        margin-top: 2rem;
    }
    
    .filter-info-label {
        font-size: 0.75rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    
    .filter-info-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-primary);
        font-variant-numeric: tabular-nums;
    }
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background-color: transparent;
        border-bottom: 1px solid var(--border-color);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        padding: 0.75rem 1.25rem;
        font-weight: 500;
        color: var(--text-secondary);
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: var(--color-primary);
        border-bottom-color: var(--color-primary);
    }
    
    /* ===== STREAMLIT WIDGETS ===== */
    .stSelectbox label, .stSlider label {
        color: var(--text-secondary) !important;
        font-size: 0.875rem !important;
    }
    
    /* ===== DATAFRAME ===== */
    .stDataFrame {
        background-color: var(--bg-secondary);
    }
    
    /* ===== FOOTER ===== */
    .dashboard-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
        color: var(--text-secondary);
        font-size: 0.8125rem;
    }
    
    .footer-title {
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    /* ===== OCULTAR ELEMENTOS STREAMLIT ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

@st.cache_data
def cargar_datos():
    """Carga los datos procesados"""
    base_path = Path(__file__).parent.parent
    
    df_limpio = pd.read_csv(base_path / 'data' / 'processed' / 'dengue_loreto_limpio.csv')
    df_serie = pd.read_csv(base_path / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv')
    
    if 'fecha' in df_limpio.columns:
        df_limpio['fecha'] = pd.to_datetime(df_limpio['fecha'])
    
    return df_limpio, df_serie


# ============================================================================
# COMPONENTES UI
# ============================================================================

def render_header():
    """Renderiza el header principal"""
    st.markdown("""
        <div class="dashboard-header">
            <h1 class="dashboard-title">SIAD – Sistema Inteligente de Análisis de Dengue</h1>
            <p class="dashboard-subtitle">Plataforma de Vigilancia Epidemiológica | Región Loreto – Perú</p>
        </div>
    """, unsafe_allow_html=True)


def render_info_institucional():
    """Renderiza información institucional"""
    st.markdown("""
        <div class="info-box">
            <span class="material-icons info-icon">info</span>
            <div class="info-text">
                <strong>Fuente de datos:</strong> MINSA – Ministerio de Salud | 
                <strong>Periodo:</strong> 2000-2024 | 
                <strong>Cobertura:</strong> 8 provincias, 53 distritos
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_metric_card(icon, label, value, delta):
    """Renderiza una tarjeta de métrica"""
    return f"""
        <div class="metric-card">
            <span class="material-icons metric-icon">{icon}</span>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-delta">{delta}</div>
        </div>
    """


def render_metricas_principales(df):
    """Renderiza las métricas principales"""
    col1, col2, col3, col4 = st.columns(4)
    
    metricas = [
        {
            "icon": "analytics",
            "label": "Total de Casos",
            "value": f"{len(df):,}",
            "delta": "Casos registrados"
        },
        {
            "icon": "calendar_today",
            "label": "Periodo Analizado",
            "value": f"{df['ano'].nunique()}",
            "delta": f"{df['ano'].min()}–{df['ano'].max()}"
        },
        {
            "icon": "location_on",
            "label": "Provincias",
            "value": f"{df['provincia'].nunique()}",
            "delta": "Cobertura regional"
        },
        {
            "icon": "people",
            "label": "Edad Promedio",
            "value": f"{df['edad'].mean():.1f}",
            "delta": "Años"
        }
    ]
    
    for col, metrica in zip([col1, col2, col3, col4], metricas):
        with col:
            st.markdown(
                render_metric_card(
                    metrica['icon'],
                    metrica['label'],
                    metrica['value'],
                    metrica['delta']
                ),
                unsafe_allow_html=True
            )


def render_section_header(icon, title):
    """Renderiza un header de sección"""
    st.markdown(f"""
        <div class="section-header">
            <span class="material-icons section-icon">{icon}</span>
            <h2 class="section-title">{title}</h2>
        </div>
    """, unsafe_allow_html=True)


def render_filter_alert(provincia, ano_min, ano_max):
    """Renderiza alerta de filtros aplicados"""
    if provincia != 'Todas':
        texto = f"<strong>Provincia:</strong> {provincia} | <strong>Periodo:</strong> {ano_min}–{ano_max}"
    else:
        texto = f"<strong>Todas las provincias</strong> | <strong>Periodo:</strong> {ano_min}–{ano_max}"
    
    st.markdown(f"""
        <div class="info-box">
            <span class="material-icons info-icon">filter_alt</span>
            <div class="info-text">{texto}</div>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def get_plotly_theme():
    """Tema dark para gráficos Plotly"""
    return {
        'template': 'plotly_dark',
        'paper_bgcolor': '#161B22',
        'plot_bgcolor': '#161B22',
        'font': {'family': 'Inter, sans-serif', 'color': '#E5E7EB'},
        'title_font': {'size': 16, 'color': '#E5E7EB'},
        'colorway': ['#2563EB', '#22C55E', '#F59E0B', '#EF4444', '#8B5CF6']
    }


def grafico_serie_temporal(df_serie):
    """Serie temporal"""
    df_serie['fecha'] = pd.to_datetime(
        df_serie['ano'].astype(str) + '-W' + df_serie['semana'].astype(str).str.zfill(2) + '-1',
        format='%Y-W%W-%w',
        errors='coerce'
    )
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_serie['fecha'],
        y=df_serie['casos'],
        mode='lines',
        name='Casos Semanales',
        line=dict(color='#2563EB', width=2),
        fill='tozeroy',
        fillcolor='rgba(37, 99, 235, 0.2)',
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>Casos: %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        **get_plotly_theme(),
        title='Serie Temporal de Casos (2000-2024)',
        xaxis_title='Periodo',
        yaxis_title='Casos por Semana',
        hovermode='x unified',
        height=400,
        margin=dict(l=50, r=30, t=50, b=50)
    )
    
    return fig


def grafico_casos_por_ano(df):
    """Gráfico de barras por año"""
    casos_ano = df.groupby('ano').size().reset_index(name='casos')
    
    fig = px.bar(
        casos_ano,
        x='ano',
        y='casos',
        title='Distribución Anual',
        labels={'ano': 'Año', 'casos': 'Casos'},
        color='casos',
        color_continuous_scale=[[0, '#1E3A8A'], [1, '#2563EB']]
    )
    
    fig.update_layout(
        **get_plotly_theme(),
        height=400,
        showlegend=False,
        margin=dict(l=50, r=30, t=50, b=50)
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Casos: %{y}<extra></extra>'
    )
    
    return fig


def grafico_casos_por_provincia(df):
    """Gráfico horizontal de provincias"""
    casos_provincia = df['provincia'].value_counts().reset_index()
    casos_provincia.columns = ['provincia', 'casos']
    
    fig = px.bar(
        casos_provincia,
        x='casos',
        y='provincia',
        orientation='h',
        title='Distribución por Provincia',
        labels={'provincia': 'Provincia', 'casos': 'Casos'},
        color='casos',
        color_continuous_scale=[[0, '#065F46'], [1, '#22C55E']]
    )
    
    fig.update_layout(
        **get_plotly_theme(),
        height=400,
        showlegend=False,
        margin=dict(l=120, r=30, t=50, b=50)
    )
    
    fig.update_traces(
        hovertemplate='<b>%{y}</b><br>Casos: %{x}<extra></extra>'
    )
    
    return fig


def grafico_distribucion_edad(df):
    """Histograma de edad"""
    df_edad = df[df['edad'] <= 100].copy()
    
    fig = px.histogram(
        df_edad,
        x='edad',
        nbins=30,
        title='Distribución por Edad',
        labels={'edad': 'Edad (años)', 'count': 'Frecuencia'},
        color_discrete_sequence=['#F59E0B']
    )
    
    fig.update_layout(
        **get_plotly_theme(),
        height=400,
        showlegend=False,
        margin=dict(l=50, r=30, t=50, b=50)
    )
    
    return fig


def grafico_casos_por_sexo(df):
    """Gráfico de pastel por sexo"""
    casos_sexo = df['sexo'].value_counts().reset_index()
    casos_sexo.columns = ['sexo', 'casos']
    casos_sexo['sexo'] = casos_sexo['sexo'].map({'F': 'Femenino', 'M': 'Masculino'})
    
    fig = px.pie(
        casos_sexo,
        values='casos',
        names='sexo',
        title='Distribución por Sexo',
        color_discrete_sequence=['#EC4899', '#2563EB']
    )
    
    fig.update_layout(
        **get_plotly_theme(),
        height=400,
        margin=dict(l=30, r=30, t=50, b=30)
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Casos: %{value}<br>%{percent}<extra></extra>'
    )
    
    return fig


def grafico_mapa_calor(df_serie):
    """Mapa de calor año x semana"""
    pivot = df_serie.pivot_table(
        values='casos',
        index='semana',
        columns='ano',
        aggfunc='sum',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Año", y="Semana Epidemiológica", color="Casos"),
        title='Mapa de Calor: Intensidad Temporal',
        color_continuous_scale='YlOrRd',
        aspect='auto'
    )
    
    fig.update_layout(
        **get_plotly_theme(),
        height=550,
        margin=dict(l=70, r=30, t=50, b=50)
    )
    
    return fig


# ============================================================================
# SIDEBAR
# ============================================================================

def render_sidebar(df):
    """Renderiza el sidebar con filtros"""
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-header">
                <div class="sidebar-title">
                    <span class="material-icons" style="font-size: 1.25rem;">tune</span>
                    Filtros de Análisis
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Filtro de años
        st.markdown('<div class="filter-label">Rango Temporal</div>', unsafe_allow_html=True)
        anos_disponibles = sorted(df['ano'].unique())
        ano_min, ano_max = st.select_slider(
            "periodo",
            options=anos_disponibles,
            value=(anos_disponibles[0], anos_disponibles[-1]),
            label_visibility="collapsed"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Filtro de provincias
        st.markdown('<div class="filter-label">Ubicación Geográfica</div>', unsafe_allow_html=True)
        provincias = ['Todas'] + sorted(df['provincia'].unique().tolist())
        provincia_seleccionada = st.selectbox(
            "provincia",
            provincias,
            label_visibility="collapsed"
        )
        
        # Aplicar filtros
        df_filtrado = df[(df['ano'] >= ano_min) & (df['ano'] <= ano_max)]
        
        if provincia_seleccionada != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['provincia'] == provincia_seleccionada]
        
        # Info de registros filtrados
        st.markdown(f"""
            <div class="filter-info">
                <div class="filter-info-label">Registros filtrados</div>
                <div class="filter-info-value">{len(df_filtrado):,}</div>
            </div>
        """, unsafe_allow_html=True)
        
        return df_filtrado, ano_min, ano_max, provincia_seleccionada


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """Función principal del dashboard"""
    
    # Header
    render_header()
    
    # Info institucional
    render_info_institucional()
    
    # Cargar datos
    with st.spinner('Cargando datos...'):
        df_limpio, df_serie = cargar_datos()
    
    # Sidebar con filtros
    df_filtrado, ano_min, ano_max, provincia = render_sidebar(df_limpio)
    
    # Alerta de filtros
    render_filter_alert(provincia, ano_min, ano_max)
    
    # Métricas principales
    render_section_header("analytics", "Indicadores Principales")
    render_metricas_principales(df_filtrado)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabs de análisis
    tab1, tab2, tab3, tab4 = st.tabs([
        "Análisis Temporal",
        "Análisis Geográfico",
        "Análisis Demográfico",
        "Mapa de Calor"
    ])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_serie = grafico_serie_temporal(
                df_serie[(df_serie['ano'] >= ano_min) & (df_serie['ano'] <= ano_max)]
            )
            st.plotly_chart(fig_serie, use_container_width=True)
        
        with col2:
            fig_ano = grafico_casos_por_ano(df_filtrado)
            st.plotly_chart(fig_ano, use_container_width=True)
        
        # Estadísticas
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("insights", "Estadísticas Temporales")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            ano_max_casos = df_filtrado['ano'].value_counts().idxmax()
            casos_max = df_filtrado['ano'].value_counts().max()
            st.metric("Año con Más Casos", ano_max_casos, f"{casos_max:,} casos")
        
        with col2:
            promedio_anual = len(df_filtrado) / df_filtrado['ano'].nunique()
            st.metric("Promedio Anual", f"{promedio_anual:.0f} casos")
        
        with col3:
            total_anos = df_filtrado['ano'].nunique()
            st.metric("Años Analizados", total_anos)
    
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_provincia = grafico_casos_por_provincia(df_filtrado)
            st.plotly_chart(fig_provincia, use_container_width=True)
        
        with col2:
            st.markdown("### Top 10 Distritos")
            top_distritos = df_filtrado['distrito'].value_counts().head(10).reset_index()
            top_distritos.columns = ['Distrito', 'Casos']
            
            st.dataframe(
                top_distritos,
                use_container_width=True,
                hide_index=True,
                height=350
            )
    
    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_edad = grafico_distribucion_edad(df_filtrado)
            st.plotly_chart(fig_edad, use_container_width=True)
        
        with col2:
            fig_sexo = grafico_casos_por_sexo(df_filtrado)
            st.plotly_chart(fig_sexo, use_container_width=True)
        
        # Estadísticas demográficas
        st.markdown("<br>", unsafe_allow_html=True)
        render_section_header("people", "Estadísticas Demográficas")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Edad Promedio", f"{df_filtrado['edad'].mean():.1f} años")
        
        with col2:
            st.metric("Edad Mediana", f"{df_filtrado['edad'].median():.1f} años")
        
        with col3:
            st.metric("Edad Mínima", f"{df_filtrado['edad'].min():.0f} años")
        
        with col4:
            st.metric("Edad Máxima", f"{df_filtrado['edad'].max():.0f} años")
    
    with tab4:
        st.markdown("<br>", unsafe_allow_html=True)
        
        fig_calor = grafico_mapa_calor(
            df_serie[(df_serie['ano'] >= ano_min) & (df_serie['ano'] <= ano_max)]
        )
        st.plotly_chart(fig_calor, use_container_width=True)
        
        st.markdown("""
            <div class="info-box">
                <span class="material-icons info-icon">lightbulb</span>
                <div class="info-text">
                    <strong>Interpretación:</strong> 
                    El mapa de calor muestra la intensidad de casos por semana epidemiológica. 
                    Los colores más intensos (rojos) indican mayor número de casos. 
                    Se observa estacionalidad marcada con picos en los primeros meses del año.
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
        <div class="dashboard-footer">
            <div class="footer-title">Sistema Inteligente de Análisis y Predicción de Casos de Dengue</div>
            <div>Desarrollado por Joel Ircañaupa| Diciembre 2025</div>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
