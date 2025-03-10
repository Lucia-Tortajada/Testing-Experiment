# STEP 1: Importar librerías
import streamlit as st
import seaborn as sns
import pandas as pd
import random
import time
import matplotlib.pyplot as plt
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- GOOGLE SHEET IMPLEMENTATION ---
# Configurar las credenciales y conexión a Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/luciatortajada/Library/CloudStorage/OneDrive-UniversitatRamónLlull/TERCERO/2ndo Quatri/Data Visualization and Decision Making/A-B-Testing-Experiment/google_credentials.json", scope)
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y seleccionar la hoja de trabajo
spreadsheet = client.open("TaxiData")  # Nombre de la hoja en Google Sheets
worksheet = spreadsheet.sheet1  # Acceder a la primera hoja


# Función para subir datos a Google Sheets
def upload_data_to_gs(df):
    worksheet.clear()  # Limpia los datos anteriores
    worksheet.append_row(["day_of_week", "num_rides"])  # Agrega encabezados
    for day, count in df["day_of_week"].value_counts().items():
        worksheet.append_row([day, count])  # Agrega cada día y su cantidad de viajes


# Función para leer datos desde Google Sheets
def read_data_from_gs():
    data = worksheet.get_all_records()  # Obtiene datos de Google Sheets
    return pd.DataFrame(data)  # Convierte en DataFrame


# --- STEP 2: Cargar y procesar el dataset ---
# Subimos los datos solo si es la primera vez
if "data_uploaded" not in st.session_state:
    df = sns.load_dataset("taxis")
    df["pickup"] = pd.to_datetime(df["pickup"])
    df["day_of_week"] = df["pickup"].dt.day_name()
    upload_data_to_gs(df)  # Subir datos a Google Sheets
    st.session_state.data_uploaded = True  # Evitar que se suban múltiples veces

# Cargamos los datos desde Google Sheets
df = read_data_from_gs()

# --- STEP 3: Título y pregunta ---
st.title("A/B Testing Experiment - Taxi Data")
st.write("### Business Question: Which day of the week records more taxi rides?")

# --- STEP 4: Funciones para graficar ---
def plot_chart_a():
    fig, ax = plt.subplots()
    sns.barplot(x=df["day_of_week"], y=df["num_rides"], order=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Bar Chart)")
    st.pyplot(fig)

def plot_chart_b():
    fig, ax = plt.subplots()
    df.set_index("day_of_week").reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])["num_rides"].plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Number of Rides per Day (Line Chart)")
    st.pyplot(fig)

# --- STEP 5: Crear tabs en la aplicación ---
tab1, tab2 = st.tabs(["Home", "About"])

with tab1:
    st.header("Experiment: Compare Two Charts")

    # Variables de estado de la sesión
    if "chart_selected" not in st.session_state:
        st.session_state.chart_selected = None
    if "start_time" not in st.session_state:
        st.session_state.start_time = None

    # Botón para mostrar un gráfico al azar
    if st.button("Show Chart"):
        st.session_state.chart_selected = random.choice(["A", "B"])
        st.session_state.start_time = time.time()  # Iniciar temporizador

    # Mostrar el gráfico seleccionado
    if st.session_state.chart_selected == "A":
        plot_chart_a()
    elif st.session_state.chart_selected == "B":
        plot_chart_b()

    # Botón para medir el tiempo de respuesta
    if st.session_state.chart_selected:
        if st.button("I answered the question"):
            end_time = time.time()
            elapsed_time = end_time - st.session_state.start_time
            st.write(f"You took {elapsed_time:.2f} seconds to answer.")

with tab2:
    st.header("About this App")
    st.write("This app compares two different visualizations to determine which one is more effective in analyzing taxi demand during a week.")
