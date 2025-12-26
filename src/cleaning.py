"""
Módulo de limpieza y estandarización de datos
Sistema de Análisis de Dengue en Perú
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


def analizar_calidad_datos(df: pd.DataFrame) -> Dict:
    """
    Analiza la calidad de los datos del dataset.
    
    Args:
        df: DataFrame a analizar
    
    Returns:
        Diccionario con métricas de calidad
    """
    calidad = {
        'total_registros': len(df),
        'registros_duplicados': df.duplicated().sum(),
        'porcentaje_duplicados': (df.duplicated().sum() / len(df)) * 100,
        'valores_nulos_por_columna': df.isnull().sum().to_dict(),
        'porcentaje_nulos_por_columna': ((df.isnull().sum() / len(df)) * 100).to_dict(),
        'columnas_con_nulos': df.columns[df.isnull().any()].tolist()
    }
    
    return calidad


def limpiar_valores_faltantes(df: pd.DataFrame, estrategia: str = 'eliminar') -> pd.DataFrame:
    """
    Limpia valores faltantes según la estrategia especificada.
    
    Args:
        df: DataFrame a limpiar
        estrategia: 'eliminar', 'rellenar_vacio', 'rellenar_desconocido'
    
    Returns:
        DataFrame limpio
    """
    df_limpio = df.copy()
    
    if estrategia == 'eliminar':
        # Eliminar filas con valores nulos en columnas críticas
        columnas_criticas = ['departamento', 'provincia', 'ano', 'semana']
        df_limpio = df_limpio.dropna(subset=columnas_criticas)
        print(f"[LIMPIEZA] Eliminadas {len(df) - len(df_limpio):,} filas con valores nulos en columnas criticas")
    
    elif estrategia == 'rellenar_vacio':
        # Rellenar valores nulos con cadena vacía
        df_limpio = df_limpio.fillna('')
        print(f"[LIMPIEZA] Valores nulos rellenados con cadena vacia")
    
    elif estrategia == 'rellenar_desconocido':
        # Rellenar valores nulos con 'DESCONOCIDO'
        df_limpio = df_limpio.fillna('DESCONOCIDO')
        print(f"[LIMPIEZA] Valores nulos rellenados con 'DESCONOCIDO'")
    
    return df_limpio


def estandarizar_texto(df: pd.DataFrame, columnas: List[str]) -> pd.DataFrame:
    """
    Estandariza el texto de las columnas especificadas.
    
    Args:
        df: DataFrame a estandarizar
        columnas: Lista de columnas a estandarizar
    
    Returns:
        DataFrame con texto estandarizado
    """
    df_estandarizado = df.copy()
    
    for col in columnas:
        if col in df_estandarizado.columns:
            # Convertir a mayúsculas y eliminar espacios extras
            df_estandarizado[col] = df_estandarizado[col].astype(str).str.upper().str.strip()
            print(f"[ESTANDARIZACION] Columna '{col}' estandarizada")
    
    return df_estandarizado


def validar_rangos_temporales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida que los rangos temporales sean correctos.
    
    Args:
        df: DataFrame a validar
    
    Returns:
        DataFrame con datos válidos
    """
    df_valido = df.copy()
    
    # Validar año (debe estar entre 2000 y 2024)
    if 'ano' in df_valido.columns:
        antes = len(df_valido)
        df_valido = df_valido[(df_valido['ano'] >= 2000) & (df_valido['ano'] <= 2024)]
        eliminados = antes - len(df_valido)
        if eliminados > 0:
            print(f"[VALIDACION] Eliminados {eliminados:,} registros con anos fuera de rango")
    
    # Validar semana epidemiológica (debe estar entre 1 y 53)
    if 'semana' in df_valido.columns:
        antes = len(df_valido)
        df_valido = df_valido[(df_valido['semana'] >= 1) & (df_valido['semana'] <= 53)]
        eliminados = antes - len(df_valido)
        if eliminados > 0:
            print(f"[VALIDACION] Eliminados {eliminados:,} registros con semanas fuera de rango")
    
    return df_valido


def validar_edad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida que los valores de edad sean razonables.
    
    Args:
        df: DataFrame a validar
    
    Returns:
        DataFrame con edades válidas
    """
    df_valido = df.copy()
    
    if 'edad' in df_valido.columns:
        antes = len(df_valido)
        # Eliminar edades negativas o mayores a 120 años
        df_valido = df_valido[(df_valido['edad'] >= 0) & (df_valido['edad'] <= 120)]
        eliminados = antes - len(df_valido)
        if eliminados > 0:
            print(f"[VALIDACION] Eliminados {eliminados:,} registros con edades invalidas")
    
    return df_valido


def crear_fecha_epidemiologica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea una columna de fecha a partir del año y semana epidemiológica.
    
    Args:
        df: DataFrame con columnas 'ano' y 'semana'
    
    Returns:
        DataFrame con columna 'fecha' agregada
    """
    df_con_fecha = df.copy()
    
    if 'ano' in df_con_fecha.columns and 'semana' in df_con_fecha.columns:
        # Crear fecha aproximada (primer día de la semana epidemiológica)
        df_con_fecha['fecha'] = pd.to_datetime(
            df_con_fecha['ano'].astype(str) + '-W' + df_con_fecha['semana'].astype(str).str.zfill(2) + '-1',
            format='%Y-W%W-%w',
            errors='coerce'
        )
        print(f"[TRANSFORMACION] Columna 'fecha' creada exitosamente")
    
    return df_con_fecha


def agrupar_por_semana_epidemiologica(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrupa los casos por año y semana epidemiológica.
    
    Args:
        df: DataFrame con datos de dengue
    
    Returns:
        DataFrame agrupado con conteo de casos
    """
    if 'ano' not in df.columns or 'semana' not in df.columns:
        raise ValueError("El DataFrame debe contener columnas 'ano' y 'semana'")
    
    df_agrupado = df.groupby(['ano', 'semana']).size().reset_index(name='casos')
    df_agrupado = df_agrupado.sort_values(['ano', 'semana'])
    
    print(f"[AGRUPACION] Datos agrupados por semana epidemiologica")
    print(f"Total de semanas: {len(df_agrupado):,}")
    
    return df_agrupado


def generar_reporte_limpieza(df_original: pd.DataFrame, df_limpio: pd.DataFrame) -> str:
    """
    Genera un reporte de las operaciones de limpieza realizadas.
    
    Args:
        df_original: DataFrame original
        df_limpio: DataFrame después de la limpieza
    
    Returns:
        String con el reporte
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("REPORTE DE LIMPIEZA DE DATOS")
    reporte.append("=" * 60)
    
    reporte.append(f"\nRegistros originales: {len(df_original):,}")
    reporte.append(f"Registros finales: {len(df_limpio):,}")
    reporte.append(f"Registros eliminados: {len(df_original) - len(df_limpio):,}")
    reporte.append(f"Porcentaje retenido: {(len(df_limpio)/len(df_original)*100):.2f}%")
    
    # Comparar valores nulos
    nulos_antes = df_original.isnull().sum().sum()
    nulos_despues = df_limpio.isnull().sum().sum()
    
    reporte.append(f"\nValores nulos antes: {nulos_antes:,}")
    reporte.append(f"Valores nulos despues: {nulos_despues:,}")
    reporte.append(f"Valores nulos eliminados: {nulos_antes - nulos_despues:,}")
    
    reporte.append("\n" + "=" * 60)
    
    return "\n".join(reporte)
