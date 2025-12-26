"""
Script de modelado SARIMA optimizado
Versión simplificada para entrenamiento más rápido
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')


def main():
    """Función principal de modelado optimizado"""
    
    print("=" * 60)
    print("MODELADO SARIMA OPTIMIZADO - DENGUE LORETO")
    print("=" * 60)
    
    # Rutas
    base_path = Path(__file__).parent.parent
    ruta_serie = base_path / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv'
    ruta_viz = base_path / 'visualizations'
    ruta_modelos = base_path / 'models'
    ruta_modelos.mkdir(exist_ok=True)
    
    # 1. Cargar datos
    print("\n[1/6] Cargando datos...")
    df_serie = pd.read_csv(ruta_serie)
    
    # Crear fecha
    df_serie['fecha'] = pd.to_datetime(
        df_serie['ano'].astype(str) + '-W' + df_serie['semana'].astype(str).str.zfill(2) + '-1',
        format='%Y-W%W-%w',
        errors='coerce'
    )
    df_serie = df_serie.dropna(subset=['fecha'])
    serie = df_serie.set_index('fecha')['casos'].sort_index()
    
    print(f"Total de observaciones: {len(serie)}")
    print(f"Periodo: {serie.index.min()} a {serie.index.max()}")
    
    # 2. Dividir en train y test
    print("\n[2/6] Dividiendo datos...")
    test_size = 52  # 1 año
    split_point = len(serie) - test_size
    
    serie_train = serie.iloc[:split_point]
    serie_test = serie.iloc[split_point:]
    
    print(f"Entrenamiento: {len(serie_train)} observaciones")
    print(f"Prueba: {len(serie_test)} observaciones")
    
    # 3. Entrenar modelo SARIMA simplificado
    print("\n[3/6] Entrenando modelo SARIMA...")
    print("Parametros: (1,1,1)(0,1,1,52)")
    
    modelo = SARIMAX(
        serie_train,
        order=(1, 1, 1),
        seasonal_order=(0, 1, 1, 52),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    resultado = modelo.fit(disp=False, maxiter=100)
    
    print(f"AIC: {resultado.aic:.2f}")
    print(f"BIC: {resultado.bic:.2f}")
    print("[OK] Modelo entrenado")
    
    # 4. Predicciones
    print("\n[4/6] Realizando predicciones...")
    predicciones = resultado.forecast(steps=len(serie_test))
    
    # 5. Evaluar
    print("\n[5/6] Evaluando modelo...")
    mae = mean_absolute_error(serie_test, predicciones)
    rmse = np.sqrt(mean_squared_error(serie_test, predicciones))
    mape = np.mean(np.abs((serie_test - predicciones) / serie_test)) * 100
    
    print(f"MAE: {mae:.2f} casos")
    print(f"RMSE: {rmse:.2f} casos")
    print(f"MAPE: {mape:.2f}%")
    
    # 6. Graficar
    print("\n[6/6] Generando visualizaciones...")
    
    fig, ax = plt.subplots(figsize=(16, 6))
    ax.plot(serie_train.index, serie_train.values, label='Entrenamiento', color='blue', alpha=0.7)
    ax.plot(serie_test.index, serie_test.values, label='Valores Reales', color='green', linewidth=2)
    ax.plot(serie_test.index, predicciones.values, label='Predicciones', 
            color='red', linestyle='--', linewidth=2)
    
    ax.set_title('Modelo SARIMA: Predicciones vs Valores Reales', fontsize=16, fontweight='bold')
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Casos de Dengue', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(str(ruta_viz / 'predicciones_sarima.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"[OK] Grafico guardado en: {ruta_viz / 'predicciones_sarima.png'}")
    
    # Guardar predicciones
    df_pred = pd.DataFrame({
        'fecha': serie_test.index,
        'casos_reales': serie_test.values,
        'casos_predichos': predicciones.values
    })
    df_pred.to_csv(ruta_modelos / 'predicciones_sarima.csv', index=False)
    
    # Guardar reporte
    reporte = f"""============================================================
REPORTE DE MODELO SARIMA
============================================================

Parametros del modelo:
  - (p, d, q): (1, 1, 1)
  - (P, D, Q, s): (0, 1, 1, 52)

Metricas de evaluacion:
  - MAE: {mae:.2f} casos
  - RMSE: {rmse:.2f} casos
  - MAPE: {mape:.2f}%

Criterios de informacion:
  - AIC: {resultado.aic:.2f}
  - BIC: {resultado.bic:.2f}

============================================================
"""
    
    with open(ruta_modelos / 'reporte_sarima.txt', 'w') as f:
        f.write(reporte)
    
    print("\n" + reporte)
    
    print("=" * 60)
    print("MODELADO COMPLETADO EXITOSAMENTE")
    print("=" * 60)
    
    return resultado, {'MAE': mae, 'RMSE': rmse, 'MAPE': mape}


if __name__ == "__main__":
    modelo, metricas = main()
