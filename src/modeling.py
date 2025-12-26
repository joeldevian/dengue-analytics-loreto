"""
Módulo de Modelado de Series Temporales
Sistema de Análisis de Dengue en Perú - SARIMA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Tuple, Dict
import warnings
warnings.filterwarnings('ignore')


def preparar_serie_temporal(df_serie: pd.DataFrame) -> pd.Series:
    """
    Prepara la serie temporal para modelado SARIMA.
    
    Args:
        df_serie: DataFrame con columnas 'ano', 'semana', 'casos'
    
    Returns:
        Serie temporal indexada por fecha
    """
    # Crear fecha
    df_serie['fecha'] = pd.to_datetime(
        df_serie['ano'].astype(str) + '-W' + df_serie['semana'].astype(str).str.zfill(2) + '-1',
        format='%Y-W%W-%w',
        errors='coerce'
    )
    
    # Eliminar valores nulos
    df_serie = df_serie.dropna(subset=['fecha'])
    
    # Crear serie temporal
    serie = df_serie.set_index('fecha')['casos']
    serie = serie.sort_index()
    
    print(f"[PREPARACION] Serie temporal creada")
    print(f"  - Periodo: {serie.index.min()} a {serie.index.max()}")
    print(f"  - Total de observaciones: {len(serie)}")
    print(f"  - Frecuencia: Semanal")
    
    return serie


def test_estacionariedad(serie: pd.Series) -> Dict:
    """
    Realiza el test de Dickey-Fuller para verificar estacionariedad.
    
    Args:
        serie: Serie temporal
    
    Returns:
        Diccionario con resultados del test
    """
    resultado = adfuller(serie.dropna())
    
    resultados = {
        'estadistico_adf': resultado[0],
        'p_valor': resultado[1],
        'valores_criticos': resultado[4],
        'es_estacionaria': resultado[1] < 0.05
    }
    
    print(f"\n[TEST ESTACIONARIEDAD]")
    print(f"  - Estadistico ADF: {resultados['estadistico_adf']:.4f}")
    print(f"  - P-valor: {resultados['p_valor']:.4f}")
    print(f"  - Es estacionaria: {'SI' if resultados['es_estacionaria'] else 'NO'}")
    
    return resultados


def diferenciar_serie(serie: pd.Series, orden: int = 1, estacional: bool = False, s: int = 52) -> pd.Series:
    """
    Aplica diferenciación a la serie temporal.
    
    Args:
        serie: Serie temporal
        orden: Orden de diferenciación
        estacional: Si True, aplica diferenciación estacional
        s: Periodo estacional
    
    Returns:
        Serie diferenciada
    """
    serie_diff = serie.copy()
    
    # Diferenciación regular
    for i in range(orden):
        serie_diff = serie_diff.diff().dropna()
    
    # Diferenciación estacional
    if estacional:
        serie_diff = serie_diff.diff(s).dropna()
    
    print(f"[DIFERENCIACION] Aplicada diferenciacion orden={orden}, estacional={estacional}")
    
    return serie_diff


def graficar_acf_pacf(serie: pd.Series, lags: int = 52, guardar: bool = False, ruta: str = None):
    """
    Grafica ACF y PACF para identificar parámetros.
    
    Args:
        serie: Serie temporal
        lags: Número de lags a mostrar
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))
    
    # ACF
    plot_acf(serie.dropna(), lags=lags, ax=axes[0])
    axes[0].set_title('Autocorrelación (ACF)', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # PACF
    plot_pacf(serie.dropna(), lags=lags, ax=axes[1])
    axes[1].set_title('Autocorrelación Parcial (PACF)', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] ACF/PACF guardado en: {ruta}")
    
    plt.close()


def dividir_train_test(serie: pd.Series, test_size: int = 52) -> Tuple[pd.Series, pd.Series]:
    """
    Divide la serie en entrenamiento y prueba.
    
    Args:
        serie: Serie temporal completa
        test_size: Número de observaciones para prueba (por defecto 1 año = 52 semanas)
    
    Returns:
        Tupla (serie_train, serie_test)
    """
    split_point = len(serie) - test_size
    
    serie_train = serie.iloc[:split_point]
    serie_test = serie.iloc[split_point:]
    
    print(f"\n[DIVISION DATOS]")
    print(f"  - Entrenamiento: {len(serie_train)} observaciones ({serie_train.index.min()} a {serie_train.index.max()})")
    print(f"  - Prueba: {len(serie_test)} observaciones ({serie_test.index.min()} a {serie_test.index.max()})")
    
    return serie_train, serie_test


def entrenar_sarima(serie_train: pd.Series, order: Tuple, seasonal_order: Tuple) -> SARIMAX:
    """
    Entrena un modelo SARIMA.
    
    Args:
        serie_train: Serie de entrenamiento
        order: Parámetros (p, d, q)
        seasonal_order: Parámetros estacionales (P, D, Q, s)
    
    Returns:
        Modelo SARIMA entrenado
    """
    print(f"\n[ENTRENAMIENTO SARIMA]")
    print(f"  - Parametros (p,d,q): {order}")
    print(f"  - Parametros estacionales (P,D,Q,s): {seasonal_order}")
    
    modelo = SARIMAX(
        serie_train,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    
    resultado = modelo.fit(disp=False)
    
    print(f"  - AIC: {resultado.aic:.2f}")
    print(f"  - BIC: {resultado.bic:.2f}")
    print(f"[OK] Modelo entrenado exitosamente")
    
    return resultado


def predecir(modelo: SARIMAX, steps: int) -> pd.Series:
    """
    Realiza predicciones con el modelo.
    
    Args:
        modelo: Modelo SARIMA entrenado
        steps: Número de pasos a predecir
    
    Returns:
        Serie con predicciones
    """
    predicciones = modelo.forecast(steps=steps)
    
    print(f"\n[PREDICCION]")
    print(f"  - Pasos predichos: {steps}")
    print(f"  - Rango predicciones: {predicciones.min():.2f} - {predicciones.max():.2f}")
    
    return predicciones


def evaluar_modelo(y_true: pd.Series, y_pred: pd.Series) -> Dict:
    """
    Evalúa el desempeño del modelo.
    
    Args:
        y_true: Valores reales
        y_pred: Valores predichos
    
    Returns:
        Diccionario con métricas
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    r2 = r2_score(y_true, y_pred)
    
    metricas = {
        'MAE': mae,
        'RMSE': rmse,
        'MAPE': mape,
        'R2': r2
    }
    
    print(f"\n[METRICAS DE EVALUACION]")
    print(f"  - MAE (Error Absoluto Medio): {mae:.2f}")
    print(f"  - RMSE (Raiz del Error Cuadratico Medio): {rmse:.2f}")
    print(f"  - MAPE (Error Porcentual Absoluto Medio): {mape:.2f}%")
    print(f"  - R2 (Coeficiente de Determinacion): {r2:.4f}")
    
    return metricas


def graficar_predicciones(serie_train: pd.Series, serie_test: pd.Series, 
                          predicciones: pd.Series, guardar: bool = False, ruta: str = None):
    """
    Grafica los resultados del modelo.
    
    Args:
        serie_train: Serie de entrenamiento
        serie_test: Serie de prueba
        predicciones: Predicciones del modelo
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar
    """
    fig, ax = plt.subplots(figsize=(16, 6))
    
    # Datos de entrenamiento
    ax.plot(serie_train.index, serie_train.values, label='Entrenamiento', color='blue', alpha=0.7)
    
    # Datos de prueba (reales)
    ax.plot(serie_test.index, serie_test.values, label='Valores Reales', color='green', linewidth=2)
    
    # Predicciones
    ax.plot(serie_test.index, predicciones.values, label='Predicciones', 
            color='red', linestyle='--', linewidth=2)
    
    ax.set_title('Modelo SARIMA: Predicciones vs Valores Reales', fontsize=16, fontweight='bold')
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Casos de Dengue', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Predicciones guardado en: {ruta}")
    
    plt.close()


def graficar_residuos(modelo: SARIMAX, guardar: bool = False, ruta: str = None):
    """
    Grafica el análisis de residuos del modelo.
    
    Args:
        modelo: Modelo SARIMA entrenado
        guardar: Si True, guarda el gráfico
        ruta: Ruta donde guardar
    """
    residuos = modelo.resid
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Residuos en el tiempo
    axes[0, 0].plot(residuos)
    axes[0, 0].set_title('Residuos en el Tiempo', fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel('Observación')
    axes[0, 0].set_ylabel('Residuo')
    axes[0, 0].grid(True, alpha=0.3)
    
    # Histograma de residuos
    axes[0, 1].hist(residuos, bins=30, edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Distribución de Residuos', fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel('Residuo')
    axes[0, 1].set_ylabel('Frecuencia')
    axes[0, 1].grid(True, alpha=0.3)
    
    # ACF de residuos
    plot_acf(residuos, lags=40, ax=axes[1, 0])
    axes[1, 0].set_title('ACF de Residuos', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    # Q-Q plot
    from scipy import stats
    stats.probplot(residuos, dist="norm", plot=axes[1, 1])
    axes[1, 1].set_title('Q-Q Plot', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if guardar and ruta:
        plt.savefig(ruta, dpi=300, bbox_inches='tight')
        print(f"[GRAFICO] Residuos guardado en: {ruta}")
    
    plt.close()


def generar_reporte_modelo(metricas: Dict, order: Tuple, seasonal_order: Tuple) -> str:
    """
    Genera un reporte del modelo entrenado.
    
    Args:
        metricas: Diccionario con métricas de evaluación
        order: Parámetros (p, d, q)
        seasonal_order: Parámetros estacionales (P, D, Q, s)
    
    Returns:
        String con el reporte
    """
    reporte = []
    reporte.append("=" * 60)
    reporte.append("REPORTE DE MODELO SARIMA")
    reporte.append("=" * 60)
    
    reporte.append(f"\nParametros del modelo:")
    reporte.append(f"  - (p, d, q): {order}")
    reporte.append(f"  - (P, D, Q, s): {seasonal_order}")
    
    reporte.append(f"\nMetricas de evaluacion:")
    reporte.append(f"  - MAE: {metricas['MAE']:.2f} casos")
    reporte.append(f"  - RMSE: {metricas['RMSE']:.2f} casos")
    reporte.append(f"  - MAPE: {metricas['MAPE']:.2f}%")
    reporte.append(f"  - R2: {metricas['R2']:.4f}")
    
    reporte.append("\n" + "=" * 60)
    
    return "\n".join(reporte)
