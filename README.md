# Process Capability Analysis App

Aplicacion Streamlit para analizar la capacidad de un proceso a partir de datos tabulares. Permite cargar archivos, seleccionar una variable numerica, evaluar normalidad, calcular indices de capacidad y simular escenarios objetivo mediante Monte Carlo.

## Funciones principales

- Carga de archivos `.csv` y `.xlsx`.
- Validacion estricta para archivos `.xlsx`.
- Seleccion de columnas numericas analizables.
- Analisis normal con Cpk.
- Analisis no-normal con Ppk.
- Busqueda automatica de distribuciones candidatas.
- Ranking de las 10 distribuciones con mejor ajuste.
- Timeout por distribucion para evitar que un ajuste estadistico deje pegada la app.
- Remocion configurable de outliers.
- Graficos comparativos entre datos reales y datos simulados.
- Simulacion Monte Carlo para comparar capacidad real vs capacidad objetivo.

## Requisitos de los archivos

### CSV

El archivo `.csv` debe contener datos en formato tabular, con encabezados en la primera fila.

### XLSX

El archivo `.xlsx` debe cumplir estas restricciones:

1. Debe tener exactamente una hoja.
2. La informacion debe estar dentro de una tabla de Excel.
3. Debe existir exactamente una tabla en la hoja.
4. No debe haber datos fuera de esa tabla.
5. La tabla debe tener encabezados no vacios y no repetidos.

Los archivos `.xlsm`, `.xls` u otros formatos no estan soportados. Para usarlos, guarda una copia como `.xlsx` sin macros o exporta la tabla como `.csv`.

## Flujo de uso

1. Carga un archivo `.csv` o `.xlsx`.
2. Revisa la vista previa de los datos.
3. Selecciona una columna numerica.
4. Ejecuta el analisis normal.
5. Define IL/LSL y/o UL/USL para calcular capacidad.
6. Ajusta el porcentaje de outliers si necesitas recalcular el analisis.
7. Si los datos no distribuyen normal, o si quieres comparar alternativas, ejecuta el analisis no-normal.
8. Si existe un buen fit, entra al modulo Monte Carlo para simular escenarios objetivo.

## Analisis normal

El modulo **Normal & Cpk** evalua la columna seleccionada como una distribucion normal.

Incluye:

- Test Kolmogorov-Smirnov contra normal ajustada.
- Estadisticas descriptivas.
- Calculo de Cp y Cpk.
- Soporte para dos limites de especificacion o solo un limite.
- Clasificacion del proceso segun Cpk.
- Q-Q plot.
- Density plot.
- Box plot.
- Serie de tiempo.

Los graficos comparan los datos reales con una normal ideal simulada. Si el test indica normalidad, la referencia simulada se muestra en verde; si no, se muestra en rojo.

## Analisis no-normal

El modulo **No normal & Ppk** ajusta hasta 100 distribuciones candidatas de `scipy.stats`.

Incluye:

- Ranking top 10 por AIC.
- P-value KS para distinguir el mejor fit relativo de un buen fit estadistico.
- Indicador de buen fit cuando `p-value > 0.05`.
- Calculo de Ppk usando percentiles de la distribucion ajustada.
- Timeout configurable por distribucion.
- Lista de distribuciones saltadas por timeout.
- Los mismos graficos comparativos del analisis normal.

El timeout evita que una distribucion lenta o numericamente inestable bloquee el analisis completo.

## Monte Carlo

El modulo **Monte Carlo** se desbloquea cuando existe un buen fit normal o no-normal.

Permite:

- Recuperar la distribucion seleccionada y sus parametros.
- Definir IL/LSL y/o UL/USL.
- Definir el Cpk o Ppk objetivo.
- Simular la distribucion real esperada.
- Simular una distribucion objetivo compatible con la capacidad deseada.
- Comparar ambas curvas en un density plot.

## Clasificacion de capacidad

La app clasifica el proceso usando el indice Cpk o Ppk calculado:

- `< 1`: Se debe mejorar.
- `1 a 2`: Susceptible a mejora.
- `> 2`: Proceso capaz.

## Instalacion local

Clona el repositorio:

```bash
git clone https://github.com/sspratz96/Process-Capability-Analysis-App.git
cd Process-Capability-Analysis-App
```

Crea y activa un ambiente virtual:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

Ejecuta la app:

```bash
streamlit run app_analysis.py
```

## Dependencias

Las dependencias se declaran en `requirements.txt`:

- `streamlit`
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `statsmodels`
- `scipy`
- `openpyxl`

`openpyxl` es necesario para validar tablas reales dentro de archivos `.xlsx`.

## Archivo principal

La aplicacion vive en:

```text
app_analysis.py
```

## Notas tecnicas

- El analisis de distribuciones usa `multiprocessing` para aislar ajustes lentos.
- Si una distribucion excede el tiempo maximo configurado, se termina el worker y se continua con la siguiente.
- El test de ajuste usa Kolmogorov-Smirnov sobre distribuciones congeladas de SciPy para evitar incompatibilidades entre versiones.
- El modulo no-normal usa AIC para ordenar los mejores candidatos y p-value KS para evaluar si el fit es estadisticamente aceptable.

## Limitaciones actuales

- La calidad del fit depende del tamano y calidad de la muestra.
- El uso de KS con parametros estimados es una aproximacion practica, no una prueba perfecta para todos los contextos.
- El calculo no-normal de Ppk usa percentiles de la distribucion ajustada.
- La simulacion objetivo no-normal escala la dispersion de la distribucion ajustada; puede requerir refinamiento para casos industriales especificos.
