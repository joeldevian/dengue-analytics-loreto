"""
Script de ejecución de Modelado SARIMA
Entrena y evalúa el modelo de predicción
"""

import sys
from pathlib import Path

# Agregar src al path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

import pandas as pd
from modeling import (
    preparar_serie_temporal,
    test_estacionariedad,
    diferenciar_serie,
    graficar_acf_pacf,
    dividir_train_test,
    entrenar_sarima,
    predecir,
    evaluar_modelo,
    graficar_predicciones,
    graficar_residuos,
    generar_reporte_modelo
)


def main():
    """Función principal de modelado"""
    
    print("=" * 60)
    print("MODELADO SARIMA - DENGUE LORETO")
    print("=" * 60)
    
    # Rutas
    base_path = Path(__file__).parent.parent
    ruta_serie = base_path / 'data' / 'processed' / 'dengue_loreto_serie_temporal.csv'
    ruta_viz = base_path / 'visualizations'
    ruta_modelos = base_path / 'models'
    ruta_modelos.mkdir(exist_ok=True)
    
    # 1. Cargar y preparar datos
    print("\n[1/10] Cargando y preparando datos...")
    df_serie = pd.read_csv(ruta_serie)
    serie = preparar_serie_temporal(df_serie)
    
    # 2. Test de estacionariedad
    print("\n[2/10] Test de estacionariedad...")
    test_est = test_estacionariedad(serie)
    
    # 3. Graficar ACF y PACF de la serie original
    print("\n[3/10] Graficando ACF y PACF...")
    graficar_acf_pacf(
        serie, 
        lags=104,  # 2 años
        guardar=True, 
        ruta=str(ruta_viz / 'acf_pacf_original.png')
    )
    
    # 4. Aplicar diferenciación si es necesario
    if not test_est['es_estacionaria']:
        print("\n[4/10] Aplicando diferenciacion...")
        serie_diff = diferenciar_serie(serie, orden=1, estacional=True, s=52)
        
        # Test de estacionariedad de serie diferenciada
        test_est_diff = test_estacionariedad(serie_diff)
        
        # Graficar ACF y PACF de serie diferenciada
        graficar_acf_pacf(
            serie_diff, 
            lags=104,
            guardar=True, 
            ruta=str(ruta_viz / 'acf_pacf_diferenciada.png')
        )
    else:
        print("\n[4/10] Serie ya es estacionaria, no se requiere diferenciacion")
    
    # 5. Dividir en train y test
    print("\n[5/10] Dividiendo datos...")
    serie_train, serie_test = dividir_train_test(serie, test_size=52)  # 1 año de prueba
    
    # 6. Entrenar modelo SARIMA
    print("\n[6/10] Entrenando modelo SARIMA...")
    # Parámetros basados en el análisis EDA:
    # - Estacionalidad anual (s=52)
    # - Diferenciación regular y estacional
    # - Componentes AR y MA moderados
    
    order = (1, 1, 1)  # (p, d, q)
    seasonal_order = (1, 1, 1, 52)  # (P, D, Q, s)
    
    modelo = entrenar_sarima(serie_train, order, seasonal_order)
    
    # 7. Realizar predicciones
    print("\n[7/10] Realizando predicciones...")
    predicciones = predecir(modelo, steps=len(serie_test))
    
    # 8. Evaluar modelo
    print("\n[8/10] Evaluando modelo...")
    metricas = evaluar_modelo(serie_test, predicciones)
    
    # 9. Graficar resultados
    print("\n[9/10] Generando graficos...")
    graficar_predicciones(
        serie_train, 
        serie_test, 
        predicciones,
        guardar=True, 
        ruta=str(ruta_viz / 'predicciones_sarima.png')
    )
    
    # Graficar residuos
    graficar_residuos(
        modelo,
        guardar=True, 
        ruta=str(ruta_viz / 'analisis_residuos.png')
    )
    
    # 10. Generar reporte
    print("\n[10/10] Generando reporte...")
    reporte = generar_reporte_modelo(metricas, order, seasonal_order)
    print("\n" + reporte)
    
    # Guardar reporte
    ruta_reporte = ruta_modelos / 'reporte_sarima.txt'
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        f.write(reporte)
    print(f"\n[OK] Reporte guardado en: {ruta_reporte}")
    
    # Guardar predicciones
    df_predicciones = pd.DataFrame({
        'fecha': serie_test.index,
        'casos_reales': serie_test.values,
        'casos_predichos': predicciones.values
    })
    ruta_pred = ruta_modelos / 'predicciones_sarima.csv'
    df_predicciones.to_csv(ruta_pred, index=False)
    print(f"[OK] Predicciones guardadas en: {ruta_pred}")
    
    print("\n" + "=" * 60)
    print("MODELADO SARIMA COMPLETADO")
    print("=" * 60)
    print(f"\nArchivos generados:")
    print(f"  1. {ruta_viz / 'acf_pacf_original.png'}")
    print(f"  2. {ruta_viz / 'acf_pacf_diferenciada.png'}")
    print(f"  3. {ruta_viz / 'predicciones_sarima.png'}")
    print(f"  4. {ruta_viz / 'analisis_residuos.png'}")
    print(f"  5. {ruta_modelos / 'reporte_sarima.txt'}")
    print(f"  6. {ruta_modelos / 'predicciones_sarima.csv'}")
    
    return modelo, metricas


if __name__ == "__main__":
    modelo, metricas = main()
