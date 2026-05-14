# 📊 Análisis del Mercado Laboral Argentino — EPH T3-2025

**Ciencias de Datos, UBA**  
Universidad de Buenos Aires · Facultad de Ciencias Exactas y Naturales (FCEyN)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/davidpalacio1/mercado-laboral-argentino-EPH-data-analysis/blob/main/Mercado_laboral_argentino_EPH_data_analysis.ipynb)

---

## 📋 Descripción

Análisis completo de la **Encuesta Permanente de Hogares (EPH)** del tercer trimestre de 2025, relevada por el INDEC. La EPH es la principal fuente de información sobre el mercado laboral argentino: registra datos socioeconómicos de **44.946 individuos** en los principales aglomerados urbanos del país.

El proyecto aplica técnicas de machine learning no supervisado y supervisado para responder preguntas concretas sobre la estructura del empleo en Argentina:
- ¿Qué perfiles laborales existen en la población activa?
- ¿Se puede predecir si una persona trabaja en el sector formal, informal o en servicio doméstico?
- ¿Qué factores determinan el ingreso — y cuánto explican?

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

- Filtrado de entrevistas completas: de 44.946 → **37.312 registros limpios** (`H15 = 1`, sin NS/NR en `PP04C`)
- Selección de 45 variables relevantes sobre condición laboral, educación e ingresos
- Imputación semántica de NaN: ausencias en variables laborales para no-ocupados representan cero actividad, **no datos faltantes**
- Tratamiento justificado de `SECTOR` (49.8% de NaN estructurales — eliminación sesgaía la muestra hacia ocupados, por lo que se conservan)
- Codificación dummy con `drop_first=True` → **113 variables finales**
- Recodificaciones: estado civil → `SOLTERO` (45.3%), alfabetismo → `LEE` (99.0%), nivel educativo en escala ordinal 0–6

---

### 2. Clustering — Perfiles socioeconómicos (no supervisado)

Normalización con `StandardScaler` + reducción dimensional con PCA (2 componentes: **21.4% de varianza explicada**) + **K=4** seleccionado por método del codo (caída de inercia marginal: −58% al pasar de K=4 a K=5).

**Justificación K-Means sobre DBSCAN:** con n=37.312 y p=116 variables, DBSCAN sufre la maldición de la dimensionalidad — las distancias euclidianas se vuelven uniformes y los clusters pierden separación. K-Means con PCA previo evita este problema.

**Los 4 perfiles del mercado laboral argentino:**

| Cluster | n | % | Perfil | Ingreso mensual promedio | Hs./semana |
|---|---|---|---|---|---|
| 0 | 18.704 | 50.1% | No ocupados con ingresos no laborales (jubilados, rentistas) | $250.562 | 0 |
| 1 | 14.240 | 38.2% | Trabajadores activos en pleno empleo | $933.985 | 38.5 |
| 2 | 3.141 | 8.4% | Jornada reducida / subocupados | $490.782 | 28.1 |
| 3 | 1.227 | 3.3% | Inactivos jóvenes sin ingresos propios | $148.520 | 0 |

> El ingreso del Cluster 1 casi **cuadruplica** al del Cluster 3. La principal dimensión de variación en el mercado laboral argentino no es el sector ni el nivel educativo — es la **condición de actividad** misma.

---

### 3. Clasificación — Sector de empleo (supervisado)

**Variable objetivo:** Formal (64.8%) / Informal (26.8%) / Servicio doméstico (8.4%)

**Preprocesamiento:** transformación `log(P47T)` — asimetría reducida de 10.25 → −0.53. División estratificada 80/20.

**Modelo:** K-Nearest Neighbors con **K óptimo = 17**, seleccionado por Cross-Validation 5-fold.

| Métrica | Valor |
|---|---|
| Accuracy en test | **91.1%** |
| Baseline trivial (siempre "Formal") | 64.8% |
| Accuracy CV (validación) | 90.7% |

**Resultados por clase:**

| Sector | Precision | Recall | F1 |
|---|---|---|---|
| Formal | 0.91 | 0.96 | 0.93 |
| Informal | 0.89 | 0.78 | 0.83 |
| Servicio doméstico | **1.00** | **0.96** | **0.98** |

**Hallazgo clave:** el servicio doméstico es la clase más fácil de clasificar (F1 = 0.98) porque tiene características observables muy distintas. El sector **informal es el más difícil** (recall = 0.78): comparte nivel educativo, edad y tipo de tarea con el formal — la diferencia está en variables que la EPH no captura directamente, como el registro en AFIP.

**Experimento de ablación:** eliminar `log(P47T)`, edad y `EMPLEO` → caída de **4.9 puntos de accuracy** (−5.4% relativo). Confirma que el ingreso declarado es la variable con mayor poder predictivo individual.

---

### 4. Regresión — Predicción de ingreso (supervisado)

**Variable objetivo:** `log(P47T)` sobre **13.856 personas ocupadas** con ingreso positivo.

- Ingreso mediano real T3-2025: **$800.000** | promedio: $1.055.249

**Comparación de modelos en test:**

| Modelo | R² test | RMSE (log) | Error típico en pesos |
|---|---|---|---|
| Ridge (α = 500) ✓ | **0.5073** | 0.5901 | ±$440K sobre la mediana |
| OLS (todas las variables) | 0.5073 | 0.5901 | ±$440K |
| OLS (3 vars: edad, educación, sector) | 0.2023 | 0.7508 | ±$600K |

**Ridge ≈ OLS:** resultado metodológicamente esperado con ~97 observaciones por parámetro y baja multicolinealidad. No hay ganancia por regularización cuando el sistema no está sobredeterminado.

**Efectos estimados (por unidad adicional):**
- Nivel educativo: **+15.6%** de ingreso por escalón (escala 0–6)
- Edad: **+11.3%** por cada 10 años adicionales
- Jerarquía ocupacional: **+3.0%** por nivel
- R² = 0.50 → educación, edad y sector explican la mitad de la varianza del ingreso; la otra mitad corresponde a factores no observados (redes, suerte, negociación salarial)

> Resultados consistentes con la teoría del capital humano (Becker, 1964) y el perfil ingreso-experiencia de Mincer (1974).

---

## 🔍 Conclusiones

**¿Qué aprendemos sobre el mercado laboral argentino en T3-2025?**

1. **La mitad de la población relevada (50.1%) no trabaja**, pero recibe ingresos no laborales — mayormente jubilaciones. Esto refleja el peso del sistema previsional como sostén de ingresos en la economía argentina, y explica por qué la condición de actividad emerge como la dimensión de variación más importante.

2. **El acceso al empleo formal casi cuadruplica el ingreso** respecto a los inactivos jóvenes ($933K vs $148K). La formalidad laboral no es solo una categoría administrativa — es el principal determinante del bienestar económico individual.

3. **El nivel educativo es el predictor de ingreso más potente (+15.6% por escalón)**, pero solo explica junto a edad y sector la mitad de la varianza. El 50% restante no está en los datos de la EPH, lo que plantea preguntas importantes sobre movilidad social y desigualdad estructural.

4. **El sector informal es el más difícil de identificar** (recall = 0.78), lo que refleja una realidad del mercado laboral: la informalidad no tiene un perfil único — convive con el formal en las mismas ocupaciones, edades y niveles educativos.

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
Clic en el badge al comienzo de este README.

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
