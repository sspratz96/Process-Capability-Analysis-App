# Deploy en Streamlit Community Cloud

Guia para preparar dependencias, probar la aplicacion localmente y publicarla en Streamlit Community Cloud.

## 1. Revisar `requirements.txt`

Streamlit Cloud instala las librerias desde `requirements.txt`. Antes de hacer deploy, confirma que el archivo exista en la raiz del repositorio y contenga todas las dependencias necesarias:

```text
streamlit
pandas
numpy
matplotlib
seaborn
statsmodels
scipy
openpyxl
```

Para esta app, `openpyxl` es importante porque permite leer y validar archivos `.xlsx` con tablas de Excel.

## 2. Probar instalacion en ambiente limpio

Desde la carpeta del proyecto:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

Si alguna dependencia falla, corrige `requirements.txt` antes de subir cambios.

## 3. Probar la app localmente

Ejecuta:

```bash
streamlit run app_analysis_2.py
```

Luego abre la URL local que entrega Streamlit, normalmente:

```text
http://localhost:8501
```

Antes de hacer deploy, prueba al menos:

- Cargar un `.csv` valido.
- Cargar un `.xlsx` valido con una sola tabla.
- Intentar cargar un `.xlsm` y confirmar que aparece el error esperado.
- Ejecutar analisis normal.
- Ejecutar analisis no-normal.
- Confirmar que el timeout por distribucion no deja pegada la app.
- Ejecutar Monte Carlo cuando exista un buen fit.

## 4. Confirmar estructura del repositorio

La raiz del repositorio debe verse asi:

```text
Process-Capability-Analysis-App/
  app_analysis_2.py
  requirements.txt
  README.md
  STREAMLIT_DEPLOY.md
```

El archivo principal para Streamlit es:

```text
app_analysis_2.py
```

## 5. Subir cambios a GitHub

Revisa cambios:

```bash
git status
```

Agrega archivos:

```bash
git add app_analysis_2.py requirements.txt README.md STREAMLIT_DEPLOY.md
```

Crea commit:

```bash
git commit -m "Update process capability app and docs"
```

Sube a GitHub:

```bash
git push
```

## 6. Crear o actualizar app en Streamlit Cloud

1. Entra a [Streamlit Community Cloud](https://share.streamlit.io/).
2. Inicia sesion con GitHub.
3. Selecciona **New app**.
4. Elige el repositorio:

```text
sspratz96/Process-Capability-Analysis-App
```

5. Selecciona la rama que quieres publicar, normalmente `main`.
6. En **Main file path**, escribe:

```text
app_analysis_2.py
```

7. Haz clic en **Deploy**.

Streamlit instalara dependencias desde `requirements.txt` y luego ejecutara el archivo principal.

## 7. Si ya existe una app publicada

Si la app ya existe en Streamlit Cloud:

1. Sube los cambios a GitHub.
2. Entra a la app en Streamlit Cloud.
3. Usa **Manage app**.
4. Selecciona **Reboot app** si no se actualiza automaticamente.

En general, Streamlit redeploya automaticamente cuando detecta cambios en la rama conectada.

## 8. Problemas comunes

### Falta una dependencia

Sintoma:

```text
ModuleNotFoundError: No module named 'openpyxl'
```

Solucion: agregar la libreria faltante a `requirements.txt`, hacer commit y subir cambios.

### La app no encuentra el archivo principal

Sintoma: Streamlit Cloud falla al iniciar y dice que no existe el script.

Solucion: confirmar que **Main file path** sea exactamente:

```text
app_analysis_2.py
```

### El analisis no-normal demora demasiado

Sintoma: el barrido de distribuciones parece quedarse en una distribucion.

Solucion: bajar el valor de:

```text
Tiempo maximo por distribucion (segundos)
```

Un valor entre 5 y 10 segundos suele ser razonable.

### El deploy falla por version de Python

Streamlit Cloud define automaticamente una version de Python compatible. Si necesitas fijarla, agrega un archivo `runtime.txt` en la raiz del repo.

Ejemplo:

```text
python-3.11
```

Usa esto solo si aparece un problema real de compatibilidad.

## 9. Checklist final antes de publicar

- `requirements.txt` esta actualizado.
- La app corre localmente con `streamlit run app_analysis_2.py`.
- El archivo principal esta en la raiz del repo.
- Los cambios estan commiteados.
- Los cambios estan subidos a GitHub.
- Streamlit Cloud apunta a la rama correcta.
- Streamlit Cloud apunta a `app_analysis_2.py`.
