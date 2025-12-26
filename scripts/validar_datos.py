"""
Script de validación de datos de dengue
Ejecuta la carga y validación inicial del dataset
"""

import sys
import pandas as pd
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from ingestion import (
    cargar_datos_dengue,
    validar_integridad,
    filtrar_por_departamento,
    obtener_resumen_temporal,
    obtener_resumen_geografico,
    generar_reporte_validacion
)


def main():
    """Función principal de validación"""
    
    print("=" * 60)
    print("VALIDACION DE DATOS - SISTEMA DE ANALISIS DE DENGUE")
    print("=" * 60)
    
    # Rutas
    ruta_datos = Path(__file__).parent.parent / 'data' / 'raw' / 'datos_abiertos_vigilancia_dengue_2000_2024.csv'
    
    # 1. Cargar datos
    print("\n[1/5] Cargando datos...")
    df = cargar_datos_dengue(str(ruta_datos))
    
    # 2. Validar integridad
    print("\n[2/5] Validando integridad...")
    validacion = validar_integridad(df)
    
    # 3. Mostrar reporte
    print("\n[3/5] Generando reporte...")
    reporte = generar_reporte_validacion(validacion)
    print(reporte)
    
    # 4. Filtrar para Loreto
    print("\n[4/5] Filtrando datos para Loreto...")
    df_loreto = filtrar_por_departamento(df, 'LORETO')
    
    # 5. Resumen de Loreto
    print("\n[5/5] Generando resumen de Loreto...")
    
    # Resumen temporal
    print("\nDistribucion temporal en Loreto:")
    casos_por_ano = obtener_resumen_temporal(df_loreto)
    print(f"  - Rango de anos: {casos_por_ano.index.min()} - {casos_por_ano.index.max()}")
    print(f"  - Total de anos: {len(casos_por_ano)}")
    print(f"  - Ano con mas casos: {casos_por_ano.idxmax()} ({casos_por_ano.max():,} casos)")
    
    # Resumen geográfico
    print("\nDistribucion geografica en Loreto:")
    casos_por_provincia = obtener_resumen_geografico(df_loreto, 'provincia')
    print(f"  - Total de provincias: {len(casos_por_provincia)}")
    print(f"  - Provincia con mas casos: {casos_por_provincia.idxmax()} ({casos_por_provincia.max():,} casos)")
    
    print("\n" + "=" * 60)
    print("VALIDACION COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    
    return df, df_loreto


if __name__ == "__main__":
    df_completo, df_loreto = main()
