"""
Script de ejecución de Análisis Exploratorio de Datos (EDA)
Genera todos los análisis y visualizaciones
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import pandas as pd
from eda import (
    configurar_estilo_graficos,
    analisis_temporal_anual,
    analisis_temporal_mensual,
    analisis_serie_temporal,
    analisis_geografico,
    analisis_demografico_edad,
    analisis_demografico_sexo,
    mapa_calor_temporal,
    estadisticas_descriptivas,
    generar_reporte_eda
)


def main():
    """Función principal de EDA"""
    
    print("=" * 60)
    print("ANALISIS EXPLORATORIO DE DATOS - DENGUE LORETO")
    print("=" * 60)
    
    # Configurar estilo
    configurar_estilo_graficos()
    
    # Rutas
    base_path = Path(__file__).parent.parent
    ruta_limpio = base_path / 'data' / 'processed' / 'dengue_loreto_limpio.csv'
    ruta_serie = base_path / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv'
    
    # Crear carpeta de visualizaciones
    ruta_viz = base_path / 'visualizations'
    ruta_viz.mkdir(exist_ok=True)
    
    # Cargar datos
    print("\n[1/10] Cargando datos...")
    df = pd.read_csv(ruta_limpio)
    df_serie = pd.read_csv(ruta_serie)
    print(f"Datos cargados: {len(df):,} registros")
    
    # Análisis temporal anual
    print("\n[2/10] Analisis temporal anual...")
    casos_ano = analisis_temporal_anual(
        df, 
        guardar=True, 
        ruta=str(ruta_viz / 'casos_por_ano.png')
    )
    
    # Análisis temporal mensual
    print("\n[3/10] Analisis temporal mensual...")
    casos_mes = analisis_temporal_mensual(
        df_serie.copy(), 
        guardar=True, 
        ruta=str(ruta_viz / 'casos_por_mes.png')
    )
    
    # Serie temporal completa
    print("\n[4/10] Generando serie temporal...")
    analisis_serie_temporal(
        df_serie.copy(), 
        guardar=True, 
        ruta=str(ruta_viz / 'serie_temporal.png')
    )
    
    # Análisis geográfico - Provincias
    print("\n[5/10] Analisis geografico - Provincias...")
    casos_provincia = analisis_geografico(
        df, 
        nivel='provincia', 
        top_n=8,
        guardar=True, 
        ruta=str(ruta_viz / 'casos_por_provincia.png')
    )
    
    # Análisis geográfico - Distritos
    print("\n[6/10] Analisis geografico - Distritos...")
    casos_distrito = analisis_geografico(
        df, 
        nivel='distrito', 
        top_n=15,
        guardar=True, 
        ruta=str(ruta_viz / 'casos_por_distrito.png')
    )
    
    # Análisis demográfico - Edad
    print("\n[7/10] Analisis demografico - Edad...")
    analisis_demografico_edad(
        df, 
        guardar=True, 
        ruta=str(ruta_viz / 'distribucion_edad.png')
    )
    
    # Análisis demográfico - Sexo
    print("\n[8/10] Analisis demografico - Sexo...")
    casos_sexo = analisis_demografico_sexo(
        df, 
        guardar=True, 
        ruta=str(ruta_viz / 'distribucion_sexo.png')
    )
    
    # Mapa de calor
    print("\n[9/10] Generando mapa de calor...")
    mapa_calor_temporal(
        df_serie.copy(), 
        guardar=True, 
        ruta=str(ruta_viz / 'mapa_calor_temporal.png')
    )
    
    # Estadísticas descriptivas
    print("\n[10/10] Calculando estadisticas descriptivas...")
    stats = estadisticas_descriptivas(df)
    
    # Generar reporte
    reporte = generar_reporte_eda(stats)
    print("\n" + reporte)
    
    # Guardar reporte
    ruta_reporte = base_path / 'visualizations' / 'reporte_eda.txt'
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)
    print(f"\n[OK] Reporte guardado en: {ruta_reporte}")
    
    print("\n" + "=" * 60)
    print("ANALISIS EXPLORATORIO COMPLETADO")
    print("=" * 60)
    print(f"\nVisualizaciones generadas en: {ruta_viz}")
    print("\nArchivos creados:")
    print("  1. casos_por_ano.png")
    print("  2. casos_por_mes.png")
    print("  3. serie_temporal.png")
    print("  4. casos_por_provincia.png")
    print("  5. casos_por_distrito.png")
    print("  6. distribucion_edad.png")
    print("  7. distribucion_sexo.png")
    print("  8. mapa_calor_temporal.png")
    print("  9. reporte_eda.txt")


if __name__ == "__main__":
    main()
