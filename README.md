# 📊 Análisis del Mercado Laboral Argentino — EPH T3-2025

**Portfolio de Data Science · Ciencias de Datos, UBA**  
Universidad de Buenos Aires · Facultad de Ciencias Exactas y Naturales (FCEyN)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davidpalacio1/mercado-laboral-argentino-EPH-data-analysis/blob/main/Mercado_laboral_argentino_EPH_data_analysis.ipynb)

---

## 📋 Descripción

Análisis completo de la **Encuesta Permanente de Hogares (EPH)** del tercer trimestre de 2025, relevada por el INDEC. La EPH es la principal fuente de información sobre el mercado laboral argentino: registra datos socioeconómicos de **44.946 individuos** en los principales aglomerados urbanos del país.

El proyecto aplica técnicas de machine learning no supervisado y supervisado para responder preguntas concretas sobre la estructura del empleo en Argentina: ¿qué perfiles laborales existen en la población?, ¿se puede predecir si una persona trabaja en el sector formal, informal o en servicio doméstico?, ¿qué factores determinan el ingreso?

Este proyecto forma parte del portfolio de Data Science de **David Palacio Velásquez**, estudiante de Ciencias de Datos y Ciencias Matemáticas en la UBA.

---

## 🗂️ Estructura del repositorio

```
mercado-laboral-argentino-EPH-data-analysis/
│
├── Mercado_laboral_argentino_EPH_data_analysis.ipynb   # Notebook principal
├── usu_individual_T325.txt                              # Base de personas EPH T3-2025 (INDEC)
└── README.md
```

> `usu_individual_T325.txt` es de acceso público en el sitio del INDEC. Ver instrucciones de descarga abajo.

---

## 📊 Contenido del análisis

### 1. Limpieza y preprocesamiento
- Filtrado de entrevistas completas: de 44.946 a **39.999 registros** (`H15 = 1`)
- Selección de 45 variables relevantes sobre condición laboral, educación e ingresos
- Imputación de NaN con criterio semántico: ausencias en variables laborales para no-ocupados representan cero actividad
- Tratamiento justificado de `SECTOR` (49.8% de NaN estructurales — no se eliminan para evitar sesgo)
- Codificación dummy con `drop_first=True` → 113 variables finales
- Recodificaciones: estado civil → `SOLTERO` (45.3%), alfabetismo → `LEE` (99.0%), nivel educativo (escala 0–6)
- Eliminación de registros NS/NR en `PP04C`: **37.312 individuos en `df_clean`**

### 2. Clustering — Perfiles socioeconómicos (no supervisado)
- Normalización con `StandardScaler` y reducción dimensional con PCA (2 componentes: **21.4% de varianza explicada**)
- Justificación de K-Means sobre DBSCAN: maldición de la dimensionalidad con n=37.312 y p=116
- Selección de **K=4** por método del codo: la reducción marginal de inercia cae −58% al pasar de K=4 a K=5
- **4 perfiles identificados:**

| Cluster | n | % | Perfil | Ingreso prom. | Hs./semana |
|---|---|---|---|---|---|
| 0 | 18.704 | 50.1% | No ocupados con ingresos no laborales | $250.562 | 0 |
| 1 | 14.240 | 38.2% | Trabajadores activos (pleno empleo) | $933.985 | 38.5 |
| 2 | 3.141 | 8.4% | Jornada reducida / subocupados | $490.782 | 28.1 |
| 3 | 1.227 | 3.3% | Inactivos jóvenes sin ingresos propios | $148.520 | 0 |

### 3. Clasificación — Sector de empleo (supervisado)
- Variable objetivo: Formal (64.8%) / Informal (26.8%) / Servicio doméstico (8.4%)
- Transformación `log(P47T)`: asimetría de 10.25 → −0.53
- División estratificada 80/20 con `stratify=y` para preservar proporciones de clase
- K-Nearest Neighbors con **K óptimo = 17**, seleccionado por Cross-Validation 5-fold (accuracy CV = 0.9070)
- **Accuracy en test: 91.1%** (vs. 64.8% del clasificador trivial)
- Hallazgo clave: el **servicio doméstico** es la clase más fácil de clasificar (F1 = 0.98, precision = 1.00); el **sector informal** es el más difícil (recall = 0.78) porque comparte características observables con el formal
- Experimento de ablación: eliminar `log(P47T)`, edad y `EMPLEO` → caída de 4.9 puntos de accuracy (−5.4% relativo)

### 4. Regresión — Predicción de ingreso (supervisado)
- Variable objetivo: `log(P47T)` sobre **13.856 personas ocupadas** con ingreso positivo
- Ingreso mediano real T3-2025: **$800.000** | promedio: $1.055.249
- Tres modelos comparados en test:

| Modelo | R² test | RMSE test |
|---|---|---|
| Ridge (α = 500) ✓ | 0.5073 | 0.5901 |
| OLS (todas las variables) | 0.5073 | 0.5901 |
| OLS (3 variables: edad, educación, sector) | 0.2023 | 0.7508 |

- Ridge ≈ OLS: resultado metodológicamente esperado con ~97 observaciones por parámetro y baja multicolinealidad
- RMSE = 0.59 → factor de **1.80x en pesos** (sobre $800.000: error típico de ±$440K / ±$244K)
- Efectos estimados (por unidad adicional): nivel educativo → **+15.6%** de ingreso | edad → **+11.3%** | jerarquía → **+3.0%**
- Interpretación consistente con la teoría del capital humano (Becker, 1964) y el perfil ingreso-experiencia de Mincer (1974)

---

## 🔍 Hallazgos principales

- La principal dimensión de variación en el mercado laboral argentino es la **condición de actividad**: ocupados plenos vs. no ocupados. El clustering la captura como la separación más relevante.
- El modelo KNN clasifica el sector de empleo con **91.1% de accuracy**. Los errores se concentran en la frontera formal-informal, que comparten muchas características observables en la EPH.
- El **nivel educativo** es el predictor de ingreso más potente: cada escalón adicional se asocia con +15.6% de ingreso, consistente con décadas de literatura en economía laboral.
- La **regularización Ridge no mejora sobre OLS** en este dataset — un resultado que se explica y justifica metodológicamente en el análisis.

---

## 🛠️ Stack tecnológico

| Herramienta | Uso |
|---|---|
| `pandas` | Manipulación, limpieza y transformación |
| `numpy` | Operaciones numéricas y transformación logarítmica |
| `matplotlib` | Histogramas, scatter plots, barras, residuos |
| `sklearn.preprocessing.StandardScaler` | Normalización (fit en train, transform en test) |
| `sklearn.decomposition.PCA` | Reducción dimensional para visualización |
| `sklearn.cluster.KMeans` | Clustering no supervisado |
| `sklearn.neighbors.KNeighborsClassifier` | Clasificación supervisada |
| `sklearn.linear_model.LinearRegression, Ridge` | Regresión lineal y regularizada L2 |
| `sklearn.model_selection.cross_val_score` | CV 5-fold para selección de hiperparámetros |
| `sklearn.metrics.ConfusionMatrixDisplay` | Matriz de confusión |
| `sklearn.metrics.classification_report` | Precision, recall y F1 por clase |

---

## 📦 Dataset

| Fuente | Descripción |
|---|---|
| [INDEC — EPH Microdatos](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos) | Base usuaria individual, EPH 3° trimestre 2025 · 44.946 individuos · 235 variables |

### Cómo obtener el dataset

1. Ir a [INDEC Microdatos](https://www.indec.gob.ar/indec/web/Institucional-Indec-BasesDeDatos)
2. Seleccionar: *Encuesta Permanente de Hogares → 3° Trimestre 2025 → Base usuaria individual*
3. Descargar y descomprimir
4. Ubicar `usu_individual_T325.txt` en el mismo directorio que el notebook

---

## 🚀 Cómo ejecutar

### Opción 1 — Google Colab (sin instalación)
Clic en el badge al principio de este README.

### Opción 2 — Local
```bash
git clone https://github.com/davidpalacio1/mercado-laboral-argentino-EPH-data-analysis.git
cd mercado-laboral-argentino-EPH-data-analysis
pip install pandas numpy matplotlib scikit-learn jupyter
jupyter notebook Mercado_laboral_argentino_EPH_data_analysis.ipynb
```

> Requiere `usu_individual_T325.txt` en el mismo directorio (descarga desde INDEC, ver arriba).

---

## 👤 Autor

**David Palacio Velásquez**  
Estudiante de Ciencias de Datos y Ciencias Matemáticas — UBA  
[LinkedIn](https://www.linkedin.com/in/davidpalacio-velasquez-3864b6298) · davidpalacio1@gmail.com  
[Ver otros proyectos](https://github.com/davidpalacio1)

---

## 📄 Licencia

Los datos son de acceso público, provistos por el INDEC bajo sus términos de uso. Este proyecto es de uso académico y no comercial.
