"""
Módulo de ingesta y validación de datos
Sistema de Análisis de Dengue en Perú
"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict
from pathlib import Path


def cargar_datos_dengue(ruta_archivo: str, sep: str = ';') -> pd.DataFrame:
    """
    Carga el dataset de dengue desde un archivo CSV.
    
    Args:
        ruta_archivo: Ruta al archivo CSV
        sep: Separador del CSV (por defecto ';')
    
    Returns:
        DataFrame con los datos cargados
    """
    try:
        df = pd.read_csv(ruta_archivo, sep=sep, encoding='utf-8', low_memory=False)
        print(f"[OK] Datos cargados exitosamente")
        print(f"Total de registros: {len(df):,}")
        print(f"Total de columnas: {len(df.columns)}")
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"[ERROR] No se encontro el archivo: {ruta_archivo}")
    except Exception as e:
        raise Exception(f"[ERROR] Error al cargar los datos: {str(e)}")


def validar_integridad(df: pd.DataFrame) -> Dict:
    """
    Valida la integridad del dataset.
    
    Args:
        df: DataFrame a validar
    
    Returns:
        Diccionario con métricas de validación
    """
    validacion = {
        'total_registros': len(df),
        'total_columnas': len(df.columns),
        'columnas': list(df.columns),
        'valores_nulos': df.isnull().sum().to_dict(),
        'porcentaje_nulos': ((df.isnull().sum() / len(df)) * 100).to_dict(),
        'tipos_datos': df.dtypes.to_dict()
    }
    
    return validacion


def filtrar_por_departamento(df: pd.DataFrame, departamento: str) -> pd.DataFrame:
    """
    Filtra el dataset por departamento.
    
    Args:
        df: DataFrame original
        departamento: Nombre del departamento (ej: 'LORETO')
    
    Returns:
        DataFrame filtrado
    """
    df_filtrado = df[df['departamento'] == departamento.upper()].copy()
    
    print(f"\n[FILTRO] Departamento: {departamento.upper()}")
    print(f"Total de registros: {len(df_filtrado):,}")
    print(f"Porcentaje del total: {(len(df_filtrado)/len(df)*100):.2f}%")
    
    return df_filtrado


def obtener_resumen_temporal(df: pd.DataFrame) -> pd.Series:
    """
    Obtiene un resumen de la distribución temporal de casos.
    
    Args:
        df: DataFrame con datos de dengue
    
    Returns:
        Serie con casos por año
    """
    if 'ano' not in df.columns:
        raise ValueError("La columna 'ano' no existe en el DataFrame")
    
    return df['ano'].value_counts().sort_index()


def obtener_resumen_geografico(df: pd.DataFrame, nivel: str = 'provincia') -> pd.Series:
    """
    Obtiene un resumen de la distribución geográfica de casos.
    
    Args:
        df: DataFrame con datos de dengue
        nivel: Nivel geográfico ('departamento', 'provincia', 'distrito')
    
    Returns:
        Serie con casos por ubicación
    """
    if nivel not in df.columns:
        raise ValueError(f"La columna '{nivel}' no existe en el DataFrame")
    
    return df[nivel].value_counts()


def guardar_datos_procesados(df: pd.DataFrame, ruta_salida: str) -> None:
    """
    Guarda el DataFrame procesado en un archivo CSV.
    
    Args:
        df: DataFrame a guardar
        ruta_salida: Ruta del archivo de salida
    """
    try:
        # Crear directorio si no existe
        Path(ruta_salida).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"[OK] Datos guardados en: {ruta_salida}")
    except Exception as e:
        raise Exception(f"[ERROR] Error al guardar los datos: {str(e)}")


def generar_reporte_validacion(validacion: Dict) -> str:
    """
    Genera un reporte de texto con los resultados de validación.
    
    Args:
        validacion: Diccionario con métricas de validación
    
    Returns:
        String con el reporte formateado
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("REPORTE DE VALIDACION DE DATOS")
    reporte.append("=" * 60)
    reporte.append(f"\nTotal de registros: {validacion['total_registros']:,}")
    reporte.append(f"Total de columnas: {validacion['total_columnas']}")
    
    reporte.append("\nColumnas del dataset:")
    for i, col in enumerate(validacion['columnas'], 1):
        reporte.append(f"  {i}. {col}")
    
    reporte.append("\nValores nulos:")
    nulos_encontrados = {k: v for k, v in validacion['valores_nulos'].items() if v > 0}
    if nulos_encontrados:
        for col, cantidad in nulos_encontrados.items():
            porcentaje = validacion['porcentaje_nulos'][col]
            reporte.append(f"  - {col}: {cantidad:,} ({porcentaje:.2f}%)")
    else:
        reporte.append("  [OK] No se encontraron valores nulos")
    
    reporte.append("\n" + "=" * 60)
    
    return "\n".join(reporte)
