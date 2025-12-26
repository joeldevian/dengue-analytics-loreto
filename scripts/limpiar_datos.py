"""
Script de limpieza de datos de dengue para Loreto
Aplica todas las transformaciones necesarias
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from ingestion import cargar_datos_dengue, filtrar_por_departamento, guardar_datos_procesados
from cleaning import (
    analizar_calidad_datos,
    limpiar_valores_faltantes,
    estandarizar_texto,
    validar_rangos_temporales,
    validar_edad,
    crear_fecha_epidemiologica,
    agrupar_por_semana_epidemiologica,
    generar_reporte_limpieza
)


def main():
    """Función principal de limpieza"""
    
    print("=" * 60)
    print("LIMPIEZA DE DATOS - DENGUE LORETO")
    print("=" * 60)
    
    # Rutas
    ruta_datos = Path(__file__).parent.parent / 'data' / 'raw' / 'datos_abiertos_vigilancia_dengue_2000_2024.csv'
    ruta_salida_loreto = Path(__file__).parent.parent / 'data' / 'processed' / 'dengue_loreto_limpio.csv'
    ruta_salida_serie = Path(__file__).parent.parent / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv'
    
    # 1. Cargar datos
    print("\n[1/8] Cargando datos...")
    df = cargar_datos_dengue(str(ruta_datos))
    
    # 2. Filtrar para Loreto
    print("\n[2/8] Filtrando para Loreto...")
    df_loreto = filtrar_por_departamento(df, 'LORETO')
    df_original = df_loreto.copy()
    
    # 3. Analizar calidad
    print("\n[3/8] Analizando calidad de datos...")
    calidad = analizar_calidad_datos(df_loreto)
    print(f"Registros duplicados: {calidad['registros_duplicados']:,} ({calidad['porcentaje_duplicados']:.2f}%)")
    print(f"Columnas con valores nulos: {len(calidad['columnas_con_nulos'])}")
    
    # 4. Limpiar valores faltantes
    print("\n[4/8] Limpiando valores faltantes...")
    df_loreto = limpiar_valores_faltantes(df_loreto, estrategia='eliminar')
    
    # 5. Estandarizar texto
    print("\n[5/8] Estandarizando texto...")
    columnas_texto = ['departamento', 'provincia', 'distrito', 'localidad', 'enfermedad']
    df_loreto = estandarizar_texto(df_loreto, columnas_texto)
    
    # 6. Validar rangos
    print("\n[6/8] Validando rangos temporales y edad...")
    df_loreto = validar_rangos_temporales(df_loreto)
    df_loreto = validar_edad(df_loreto)
    
    # 7. Crear fecha epidemiológica
    print("\n[7/8] Creando columna de fecha...")
    df_loreto = crear_fecha_epidemiologica(df_loreto)
    
    # 8. Generar reporte
    print("\n[8/8] Generando reporte de limpieza...")
    reporte = generar_reporte_limpieza(df_original, df_loreto)
    print("\n" + reporte)
    
    # Guardar datos limpios
    print(f"\nGuardando datos limpios...")
    guardar_datos_procesados(df_loreto, str(ruta_salida_loreto))
    
    # Crear y guardar serie temporal
    print(f"\nCreando serie temporal...")
    df_serie = agrupar_por_semana_epidemiologica(df_loreto)
    guardar_datos_procesados(df_serie, str(ruta_salida_serie))
    
    print("\n" + "=" * 60)
    print("LIMPIEZA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print(f"\nArchivos generados:")
    print(f"  1. {ruta_salida_loreto}")
    print(f"  2. {ruta_salida_serie}")
    
    return df_loreto, df_serie


if __name__ == "__main__":
    df_limpio, df_serie = main()
