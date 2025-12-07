import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar el dataset
file_path = 'dataset_empleados.csv'  # Asegúrate de que el archivo CSV esté en la misma carpeta que app.py
data = pd.read_csv(file_path)

# Convertir las fechas a tipo datetime
data['FechaIngreso'] = pd.to_datetime(data['FechaIngreso'])
data['FechaSalida'] = pd.to_datetime(data['FechaSalida'])

# Filtrar solo los empleados que renunciaron
data_renuncias = data[data['Attrition'] == 'Yes']

# Calcular antigüedad
data_renuncias['Antigüedad'] = (data_renuncias['FechaSalida'] - data_renuncias['FechaIngreso']).dt.days / 365

# Crear una columna de mes y año de la fecha de salida
data_renuncias['MesAnoRenuncia'] = data_renuncias['FechaSalida'].dt.to_period('M')

# Agregar una columna con el año de la renuncia
data_renuncias['AñoRenuncia'] = data_renuncias['FechaSalida'].dt.year

# Crear el menú de navegación
st.sidebar.title('Navegación')
selection = st.sidebar.radio("Selecciona una sección", ["Dashboard General", "Condiciones Laborales", "Demográficos"])

# Página de inicio - Dashboard General
if selection == "Dashboard General":
    st.title("Dashboard General: Tendencias de Renuncias")
    
    # Filtros para Dashboard General (por género y departamento)
    genero = st.selectbox("Selecciona el Género", ['All'] + list(data_renuncias['Gender'].unique()))
    departamento = st.selectbox("Selecciona el Departamento", ['All'] + list(data_renuncias['Department'].unique()))

    # Filtrar los datos según los filtros seleccionados
    if genero != 'All':
        data_filtered = data_renuncias[data_renuncias['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]

    # Gráfico de Tasa de Rotación (Renuncias por mes y año)
    renuncias_mes_ano = data_filtered.groupby('MesAnoRenuncia').size().reset_index(name='Renuncias')
    fig1 = px.line(renuncias_mes_ano, x='MesAnoRenuncia', y='Renuncias', title='Renuncias por Mes y Año')
    st.plotly_chart(fig1)

    # Gráfico de distribución de antigüedad
    fig2 = px.histogram(data_filtered, x='Antigüedad', nbins=20, title="Distribución de Antigüedad de Empleados que Renunciaron")
    st.plotly_chart(fig2)

# Página - Condiciones Laborales
elif selection == "Condiciones Laborales":
    st.title("Análisis de Condiciones Laborales")
    
    # Filtros para Condiciones Laborales (por género y departamento)
    genero = st.selectbox("Selecciona el Género", ['All'] + list(data_renuncias['Gender'].unique()))
    departamento = st.selectbox("Selecciona el Departamento", ['All'] + list(data_renuncias['Department'].unique()))

    # Filtrar los datos según los filtros seleccionados
    if genero != 'All':
        data_filtered = data_renuncias[data_renuncias['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]
    
    # Gráfico circular de tipo de contrato
    tipo_contrato = data_filtered['StockOptionLevel'].value_counts().reset_index()
    fig3 = px.pie(tipo_contrato, names='index', values='StockOptionLevel', title="Distribución de Tipo de Contrato")
    st.plotly_chart(fig3)
    
    # Gráfico de satisfacción salarial
    fig4 = px.box(data_filtered, x='SatisfaccionSalarial', y='Antigüedad', title="Satisfacción Salarial vs. Antigüedad")
    st.plotly_chart(fig4)

# Página - Demográficos
elif selection == "Demográficos":
    st.title("Análisis Demográfico de Empleados que Renunciaron")
    
    # Filtros para Demográficos (por género y departamento)
    genero = st.selectbox("Selecciona el Género", ['All'] + list(data_renuncias['Gender'].unique()))
    departamento = st.selectbox("Selecciona el Departamento", ['All'] + list(data_renuncias['Department'].unique()))

    # Filtrar los datos según los filtros seleccionados
    if genero != 'All':
        data_filtered = data_renuncias[data_renuncias['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]

    # Gráfico de distribución por edad
    fig5 = px.histogram(data_filtered, x='Age', nbins=15, title="Distribución de Edad de Empleados que Renunciaron")
    st.plotly_chart(fig5)
    
    # Gráfico de distancia desde casa
    fig6 = px.scatter(data_filtered, x='DistanceFromHome', y='Antigüedad', title="Relación entre Distancia desde Casa y Antigüedad")
    st.plotly_chart(fig6)

