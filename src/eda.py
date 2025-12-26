"""
Módulo de Análisis Exploratorio de Datos (EDA)
Sistema de Análisis de Dengue en Perú
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List


def configurar_estilo_graficos():
    """Configura el estilo global de los gráficos"""
    plt.style.use('seaborn-v0_8-darkgrid')
    sns.set_palette('husl')
    plt.rcParams['figure.figsize'] = (14, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12


def analisis_temporal_anual(df: pd.DataFrame, guardar: bool = False, ruta: str = None) -> pd.Series:
    """
    Analiza la distribución temporal anual de casos.
    
    Args:
        df: DataFrame con datos de dengue
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    
    Returns:
        Serie con casos por año
    """
    casos_por_ano = df.groupby('ano').size().sort_index()
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(14, 6))
    casos_por_ano.plot(kind='bar', color='steelblue', edgecolor='black', ax=ax)
    
    ax.set_title('Casos de Dengue por Año en Loreto (2000-2024)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Número de Casos', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # Añadir línea de tendencia
    x = np.arange(len(casos_por_ano))
    z = np.polyfit(x, casos_por_ano.values, 1)
    p = np.poly1d(z)
    ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2, label='Tendencia')
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()
    
    return casos_por_ano


def analisis_temporal_mensual(df_serie: pd.DataFrame, guardar: bool = False, ruta: str = None) -> pd.DataFrame:
    """
    Analiza la distribución temporal por mes (aproximado desde semana).
    
    Args:
        df_serie: DataFrame con serie temporal
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    
    Returns:
        DataFrame con casos por mes
    """
    # Aproximar mes desde semana epidemiológica
    df_serie['mes'] = ((df_serie['semana'] - 1) // 4) + 1
    df_serie['mes'] = df_serie['mes'].clip(upper=12)
    
    casos_por_mes = df_serie.groupby('mes')['casos'].sum().sort_index()
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    casos_por_mes.plot(kind='bar', color='coral', edgecolor='black', ax=ax)
    
    ax.set_title('Casos de Dengue por Mes en Loreto (2000-2024)', fontsize=16, fontweight='bold')
    ax.set_xlabel('Mes', fontsize=12)
    ax.set_ylabel('Total de Casos', fontsize=12)
    ax.set_xticklabels(['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 
                        'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'], rotation=45)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()
    
    return casos_por_mes


def analisis_serie_temporal(df_serie: pd.DataFrame, guardar: bool = False, ruta: str = None):
    """
    Visualiza la serie temporal completa de casos.
    
    Args:
        df_serie: DataFrame con serie temporal
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    """
    # Crear fecha para el eje X
    df_serie['fecha'] = pd.to_datetime(
        df_serie['ano'].astype(str) + '-W' + df_serie['semana'].astype(str).str.zfill(2) + '-1',
        format='%Y-W%W-%w',
        errors='coerce'
    )
    
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(df_serie['fecha'], df_serie['casos'], linewidth=1.5, color='darkblue', alpha=0.7)
    
    ax.set_title('Serie Temporal de Casos de Dengue en Loreto (2000-2024)', 
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Casos por Semana', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()


def analisis_geografico(df: pd.DataFrame, nivel: str = 'provincia', 
                        top_n: int = 10, guardar: bool = False, ruta: str = None) -> pd.Series:
    """
    Analiza la distribución geográfica de casos.
    
    Args:
        df: DataFrame con datos de dengue
        nivel: Nivel geográfico ('provincia', 'distrito')
        top_n: Número de ubicaciones a mostrar
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    
    Returns:
        Serie con casos por ubicación
    """
    casos_por_ubicacion = df[nivel].value_counts().head(top_n)
    
    # Crear gráfico
    fig, ax = plt.subplots(figsize=(12, 8))
    casos_por_ubicacion.plot(kind='barh', color='teal', edgecolor='black', ax=ax)
    
    titulo = f'Top {top_n} {nivel.capitalize()}s con Más Casos de Dengue en Loreto'
    ax.set_title(titulo, fontsize=16, fontweight='bold')
    ax.set_xlabel('Número de Casos', fontsize=12)
    ax.set_ylabel(nivel.capitalize(), fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()
    
    return casos_por_ubicacion


def analisis_demografico_edad(df: pd.DataFrame, guardar: bool = False, ruta: str = None):
    """
    Analiza la distribución de casos por edad.
    
    Args:
        df: DataFrame con datos de dengue
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    """
    # Filtrar edades válidas
    df_edad = df[df['edad'] <= 100].copy()
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histograma
    axes[0].hist(df_edad['edad'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    axes[0].set_title('Distribución de Casos por Edad', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('Edad (años)', fontsize=12)
    axes[0].set_ylabel('Frecuencia', fontsize=12)
    axes[0].grid(axis='y', alpha=0.3)
    
    # Boxplot
    axes[1].boxplot(df_edad['edad'], vert=True, patch_artist=True,
                    boxprops=dict(facecolor='lightgreen', alpha=0.7))
    axes[1].set_title('Boxplot de Edad', fontsize=14, fontweight='bold')
    axes[1].set_ylabel('Edad (años)', fontsize=12)
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()


def analisis_demografico_sexo(df: pd.DataFrame, guardar: bool = False, ruta: str = None) -> pd.Series:
    """
    Analiza la distribución de casos por sexo.
    
    Args:
        df: DataFrame con datos de dengue
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    
    Returns:
        Serie con casos por sexo
    """
    casos_por_sexo = df['sexo'].value_counts()
    
    # Crear gráfico de pastel
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colores = ['#ff9999', '#66b3ff']
    explode = (0.05, 0.05)
    
    ax.pie(casos_por_sexo.values, labels=['Femenino', 'Masculino'], 
           autopct='%1.1f%%', startangle=90, colors=colores, explode=explode,
           textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    ax.set_title('Distribución de Casos por Sexo', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()
    
    return casos_por_sexo


def mapa_calor_temporal(df_serie: pd.DataFrame, guardar: bool = False, ruta: str = None):
    """
    Crea un mapa de calor de casos por año y semana.
    
    Args:
        df_serie: DataFrame con serie temporal
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar el gráfico
    """
    # Crear pivot table
    pivot = df_serie.pivot_table(values='casos', index='semana', columns='ano', aggfunc='sum', fill_value=0)
    
    fig, ax = plt.subplots(figsize=(18, 10))
    
    sns.heatmap(pivot, cmap='YlOrRd', cbar_kws={'label': 'Casos'}, 
                linewidths=0.5, ax=ax, fmt='d')
    
    ax.set_title('Mapa de Calor: Casos de Dengue por Año y Semana Epidemiológica', 
                 fontsize=16, fontweight='bold')
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Semana Epidemiológica', fontsize=12)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Guardado en: {ruta}")
    
    plt.close()


def estadisticas_descriptivas(df: pd.DataFrame) -> Dict:
    """
    Calcula estadísticas descriptivas del dataset.
    
    Args:
        df: DataFrame con datos de dengue
    
    Returns:
        Diccionario con estadísticas
    """
    stats = {
        'total_casos': len(df),
        'periodo': f"{df['ano'].min()} - {df['ano'].max()}",
        'anos_totales': df['ano'].nunique(),
        'provincias': df['provincia'].nunique(),
        'distritos': df['distrito'].nunique(),
        'edad_promedio': df['edad'].mean(),
        'edad_mediana': df['edad'].median(),
        'edad_min': df['edad'].min(),
        'edad_max': df['edad'].max(),
        'casos_por_ano_promedio': len(df) / df['ano'].nunique(),
        'ano_max_casos': df['ano'].value_counts().idxmax(),
        'casos_ano_max': df['ano'].value_counts().max(),
        'provincia_max_casos': df['provincia'].value_counts().idxmax(),
        'casos_provincia_max': df['provincia'].value_counts().max()
    }
    
    return stats


def generar_reporte_eda(stats: Dict) -> str:
    """
    Genera un reporte de texto con las estadísticas del EDA.
    
    Args:
        stats: Diccionario con estadísticas
    
    Returns:
        String con el reporte
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("REPORTE DE ANALISIS EXPLORATORIO DE DATOS")
    reporte.append("=" * 60)
    
    reporte.append(f"\nTotal de casos: {stats['total_casos']:,}")
    reporte.append(f"Periodo: {stats['periodo']}")
    reporte.append(f"Total de anos: {stats['anos_totales']}")
    
    reporte.append(f"\nCobertura geografica:")
    reporte.append(f"  - Provincias: {stats['provincias']}")
    reporte.append(f"  - Distritos: {stats['distritos']}")
    
    reporte.append(f"\nEstadisticas de edad:")
    reporte.append(f"  - Promedio: {stats['edad_promedio']:.1f} anos")
    reporte.append(f"  - Mediana: {stats['edad_mediana']:.1f} anos")
    reporte.append(f"  - Rango: {stats['edad_min']} - {stats['edad_max']} anos")
    
    reporte.append(f"\nTendencias temporales:")
    reporte.append(f"  - Promedio casos/ano: {stats['casos_por_ano_promedio']:.0f}")
    reporte.append(f"  - Ano con mas casos: {stats['ano_max_casos']} ({stats['casos_ano_max']:,} casos)")
    
    reporte.append(f"\nTendencias geograficas:")
    reporte.append(f"  - Provincia con mas casos: {stats['provincia_max_casos']}")
    reporte.append(f"  - Casos en provincia principal: {stats['casos_provincia_max']:,}")
    
    reporte.append("\n" + "=" * 60)
    
    return "\n".join(reporte)
