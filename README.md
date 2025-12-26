# 🦟 Sistema Inteligente de Análisis de Dengue en Loreto

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.52+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Sistema de análisis y predicción de casos de dengue en la región de Loreto, Perú. Dashboard interactivo con análisis exploratorio de datos, visualizaciones profesionales y modelado de series temporales SARIMA para vigilancia epidemiológica.

<!-- 
Para agregar capturas de pantalla:
1. Ejecuta: streamlit run app/dashboard.py
2. Toma capturas y guárdalas en assets/
3. Descomenta la línea siguiente
![Dashboard Preview](assets/dashboard_preview.png)
-->

## 🎯 Características

- **Dashboard Interactivo**: Interfaz profesional con Streamlit y diseño dark mode
- **Análisis Exploratorio**: Visualizaciones temporales, geográficas y demográficas
- **Modelado Predictivo**: Implementación de SARIMA para predicción de casos
- **Diseño Premium**: Glassmorphism, efectos hover y UX/UI profesional
- **Datos Reales**: Basado en datos abiertos del MINSA (2000-2024)

## 📊 Hallazgos Clave

- **Año pico**: 2011 con 21,245 casos
- **Provincia crítica**: MAYNAS (66.4% de casos)
- **Edad promedio**: 25.2 años
- **Estacionalidad**: Picos en enero-mayo (temporada de lluvias)
- **Ciclos epidémicos**: Cada 3-5 años

## 🚀 Instalación

### Requisitos Previos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/joeldevian/dengue-analytics-loreto.git
cd dengue-analytics-loreto
```

2. **Crear entorno virtual** (recomendado)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Descargar datos** (si no están incluidos)
- Descargar el dataset desde [Datos Abiertos Perú](https://www.datosabiertos.gob.pe/)
- Colocar el archivo CSV en `data/raw/`

## 💻 Uso

### Ejecutar Dashboard
```bash
streamlit run app/dashboard.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

### Ejecutar Scripts de Análisis

**Validación de datos:**
```bash
python scripts/validar_datos.py
```

**Limpieza de datos:**
```bash
python scripts/limpiar_datos.py
```

**Análisis exploratorio:**
```bash
python scripts/ejecutar_eda.py
```

**Modelado SARIMA:**
```bash
python scripts/ejecutar_modelado_simple.py
```

## 📁 Estructura del Proyecto

```
dengue-analytics-loreto/
├── app/
│   └── dashboard.py          # Dashboard Streamlit
├── data/
│   ├── raw/                  # Datos originales
│   └── processed/            # Datos procesados
├── src/
│   ├── ingestion.py          # Carga y validación
│   ├── cleaning.py           # Limpieza de datos
│   ├── eda.py                # Análisis exploratorio
│   └── modeling.py           # Modelado SARIMA
├── scripts/                  # Scripts ejecutables
├── visualizations/           # Gráficos generados
├── models/                   # Modelos entrenados
├── notebooks/                # Jupyter notebooks
└── requirements.txt          # Dependencias
```

## 🛠️ Tecnologías

- **Backend**: Python, Pandas, NumPy
- **Visualización**: Matplotlib, Seaborn, Plotly
- **Dashboard**: Streamlit
- **Modelado**: Statsmodels (SARIMA)
- **Diseño**: CSS personalizado, Material Icons

<!-- 
## 📸 Capturas de Pantalla

Agrega capturas ejecutando el dashboard y guardándolas en assets/

### Dashboard Principal
![Dashboard](assets/dashboard_main.png)

### Análisis Temporal
![Temporal](assets/temporal_analysis.png)

### Análisis Geográfico
![Geografico](assets/geographic_analysis.png)
-->

## 🎨 Características de Diseño

- **Glassmorphism**: Efecto de vidrio esmerilado en tarjetas
- **Iconos diferenciados**: Colores únicos por métrica (azul, ámbar, verde, púrpura)
- **Efectos hover**: Elevación y animaciones suaves
- **Dark mode**: Paleta institucional profesional
- **Responsive**: Adaptable a diferentes tamaños de pantalla

## 📈 Próximos Pasos

- [ ] Optimizar entrenamiento del modelo SARIMA
- [ ] Integrar predicciones en tiempo real
- [ ] Agregar exportación de reportes PDF
- [ ] Implementar alertas automáticas
- [ ] Expandir análisis a otras regiones del Perú

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👤 Autor

**Joel Ircañaupa**

- GitHub: [@joeldevian](https://github.com/joeldevian)
- LinkedIn: [Joel Ircañaupa](https://linkedin.com/in/tu-perfil)

## 🙏 Agradecimientos

- MINSA - Ministerio de Salud del Perú por los datos abiertos
- Comunidad de Streamlit por la excelente documentación
- Región Loreto por ser el piloto de este sistema

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
