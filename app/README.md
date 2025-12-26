# Instrucciones para ejecutar el Dashboard

## Requisitos Previos

Asegúrate de tener instaladas todas las dependencias:

```bash
pip install streamlit plotly
```

## Ejecutar el Dashboard

Desde la raíz del proyecto, ejecuta:

```bash
streamlit run app/dashboard.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Características del Dashboard

### 📊 Métricas Principales
- Total de casos
- Años de datos disponibles
- Número de provincias
- Edad promedio de casos

### 🔍 Filtros Interactivos
- **Rango de años**: Selecciona el periodo a analizar
- **Provincia**: Filtra por provincia específica o ver todas

### 📈 Análisis Temporal
- Serie temporal completa (2000-2024)
- Casos por año con gráfico de barras
- Estadísticas: año con más casos, promedio anual

### 🗺️ Análisis Geográfico
- Distribución de casos por provincia
- Top 10 distritos más afectados

### 👥 Análisis Demográfico
- Distribución de casos por edad (histograma)
- Distribución por sexo (gráfico de pastel)
- Estadísticas: edad promedio, mediana, mínima, máxima

### 🔥 Mapa de Calor
- Visualización de casos por año y semana epidemiológica
- Identificación de patrones estacionales

## Navegación

El dashboard está organizado en 4 pestañas principales:
1. **Análisis Temporal**
2. **Análisis Geográfico**
3. **Análisis Demográfico**
4. **Mapa de Calor**

## Notas

- Los gráficos son interactivos (zoom, pan, hover)
- Los filtros se aplican en tiempo real
- Los datos se cargan en caché para mejor rendimiento
