import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

from scipy import stats # aqui esta el sktest

st.title("Aplicación con botones independientes")

# Inicializar estados si no existen
if 'btn1' not in st.session_state:
    st.session_state.btn1 = {'activo': True, 'archivo_valido': False, 'data': None}
    st.session_state.btn2 = {'activo': False, 'resultado': None}
    st.session_state.btn3 = {'activo': False, 'resultado': None}
    st.session_state.btn4 = {'activo': False, 'resultado': None}
    st.session_state.selected_col = None

def reset():
    st.session_state.btn1 = {'activo': True, 'archivo_valido': False, 'data': None}
    st.session_state.btn2 = {'activo': False, 'resultado': None}
    st.session_state.btn3 = {'activo': False, 'resultado': None}
    st.session_state.btn4 = {'activo': False, 'resultado': None}
    st.session_state.selected_col = None

# Paso 1: Cargar archivo
st.write("### Paso 1: Cargar archivo")
file = st.file_uploader("Selecciona un archivo Excel o CSV", type=["xlsx", "xls", "csv"])

if file:
    try:
        # Reiniciar todos los estados
        reset()

        # Leer el archivo
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            xls = pd.ExcelFile(file)
            if len(xls.sheet_names) != 1:
                st.error("El archivo Excel debe tener solo una hoja.")
                df = None
            else:
                df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])

        # Validar datos
        if df is not None and not df.empty:
            st.session_state.btn1['archivo_valido'] = True
            st.session_state.btn1['data'] = df

            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                st.session_state.btn2['activo'] = True
            else:
                st.warning("El archivo no contiene columnas numéricas.")
        else:
            st.error("El archivo no contiene datos válidos.")
            st.session_state.btn1['archivo_valido'] = False
            st.session_state.btn1['data'] = None

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
        st.session_state.btn1['archivo_valido'] = False
        st.session_state.btn1['data'] = None

# Mostrar contenido si es válido
if st.session_state.btn1.get('archivo_valido') and st.session_state.btn1.get('data') is not None:
    st.success("Archivo cargado y validado correctamente.")
    st.dataframe(st.session_state.btn1['data'])

    # Paso 2: seleccionar columna numérica
    numeric_cols = st.session_state.btn1['data'].select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        selected = st.selectbox("Selecciona una columna numérica para continuar", numeric_cols)
        if selected:
            st.session_state.selected_col = selected
    else:
        st.warning("No hay columnas numéricas disponibles.")

# Botón 2
if st.session_state.btn2['activo'] and st.session_state.selected_col:
    if st.button(r"Normal Analysis & Cpk"):
        st.session_state.btn2['resultado'] = "Ejecutado"
        st.session_state.btn3['activo'] = True
        st.session_state.btn4['activo'] = True
    st.write(f"Resultado Botón 2: {st.session_state.btn2.get('resultado')}")

    if st.session_state.btn2['resultado'] == "Ejecutado":
        col1, col2 = st.columns([1, 2])

        # Estadísticas descriptivas en la columna izquierda
        with col1:
            st.subheader("Estadísticas Descriptivas")
            col_data = st.session_state.btn1['data'][st.session_state.selected_col]

            norm_dist = getattr(stats, 'norm')
            norm_params = norm_dist.fit(col_data)
            _, p_value = stats.kstest(col_data, 'norm', args=norm_params)

            print(p_value)
            is_normal = True if p_value > 0.05 else False

            st.write(col_data.describe())
            print(is_normal)
        # Gráficos en la columna derecha
        with col2:
            st.subheader("Visualización")

            fig_row1 = plt.figure(figsize=(12, 4))
            ax1 = fig_row1.add_subplot(1, 3, 1)
            sm.qqplot(col_data, ax=ax1)
            ax1.set_title("QQ Plot")

            ax2 = fig_row1.add_subplot(1, 3, 2)
            sns.histplot(col_data, color = 'g' if is_normal else 'r', kde=True, ax=ax2)
            ax2.set_title("Histograma con Densidad")

            ax3 = fig_row1.add_subplot(1, 3, 3)
            sns.boxplot(y=col_data, ax=ax3, color='lightgreen' if is_normal else 'pink') #, 'Hypothetical Data': 'lightgreen' if is_normal else 'pink'})
            ax3.set_title("Box Plot")

            st.pyplot(fig_row1)

            fig_row2 = plt.figure(figsize=(12, 3))
            ax4 = fig_row2.add_subplot(1, 1, 1)
            ax4.plot(col_data.reset_index(drop=True))
            ax4.set_title("Serie de Tiempo")
            ax4.set_xlabel("Índice")
            ax4.set_ylabel(st.session_state.selected_col)

            st.pyplot(fig_row2)   

# Botón 3
if st.session_state.btn3['activo']:
    if st.button(r"Non-Normal Analysis & Ppk"):
        st.session_state.btn3['resultado'] = "Ejecutado"
        st.session_state.btn4['activo'] = True
    st.write(f"Resultado Botón 3: {st.session_state.btn3.get('resultado')}")

# Botón 4
if st.session_state.btn4['activo']:
    if st.button(r"Simulation Analysis w. Monte Carlo"):
        st.session_state.btn4['resultado'] = "Ejecutado"
    st.write(f"Resultado Botón 4: {st.session_state.btn4.get('resultado')}")
