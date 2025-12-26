"""
Script de verificación de datos procesados
Muestra estadísticas de los archivos generados
"""

import pandas as pd
from pathlib import Path


def main():
    """Función principal de verificación"""
    
    print("=" * 60)
    print("VERIFICACION DE DATOS PROCESADOS")
    print("=" * 60)
    
    # Rutas
    ruta_limpio = Path(__file__).parent.parent / 'data' / 'processed' / 'dengue_loreto_limpio.csv'
    ruta_serie = Path(__file__).parent.parent / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv'
    
    # Cargar datos limpios
    print("\n[1/2] Verificando datos limpios...")
    df_limpio = pd.read_csv(ruta_limpio)
    
    print(f"\nArchivo: dengue_loreto_limpio.csv")
    print(f"  - Total de registros: {len(df_limpio):,}")
    print(f"  - Total de columnas: {len(df_limpio.columns)}")
    print(f"  - Periodo: {df_limpio['ano'].min()} - {df_limpio['ano'].max()}")
    print(f"  - Provincias: {df_limpio['provincia'].nunique()}")
    print(f"  - Valores nulos totales: {df_limpio.isnull().sum().sum():,}")
    
    # Cargar serie temporal
    print("\n[2/2] Verificando serie temporal...")
    df_serie = pd.read_csv(ruta_serie)
    
    print(f"\nArchivo: dengue_loreto_serie_temporal.csv")
    print(f"  - Total de semanas: {len(df_serie):,}")
    print(f"  - Periodo: {df_serie['ano'].min()} - {df_serie['ano'].max()}")
    print(f"  - Total de casos: {df_serie['casos'].sum():,}")
    print(f"  - Promedio casos/semana: {df_serie['casos'].mean():.2f}")
    print(f"  - Maximo casos/semana: {df_serie['casos'].max()}")
    print(f"  - Minimo casos/semana: {df_serie['casos'].min()}")
    
    # Semana con más casos
    idx_max = df_serie['casos'].idxmax()
    ano_max = df_serie.loc[idx_max, 'ano']
    semana_max = df_serie.loc[idx_max, 'semana']
    casos_max = df_serie.loc[idx_max, 'casos']
    
    print(f"\nSemana con mas casos:")
    print(f"  - Ano: {ano_max}")
    print(f"  - Semana: {semana_max}")
    print(f"  - Casos: {casos_max}")
    
    print("\n" + "=" * 60)
    print("VERIFICACION COMPLETADA")
    print("=" * 60)
    
    print("\nPrimeras 10 semanas de la serie temporal:")
    print(df_serie.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
