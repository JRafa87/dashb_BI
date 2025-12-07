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

# Convertir 'MesAnoRenuncia' a formato string (Mes-Año)
data_renuncias['MesAnoRenuncia'] = data_renuncias['MesAnoRenuncia'].dt.strftime('%b-%Y')  # Ej: "Jan-2023"

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
    data_filtered = data_renuncias.copy()  # Crear una copia de data_renuncias para aplicar filtros

    if genero != 'All':
        data_filtered = data_filtered[data_filtered['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]

    # Gráfico de Renuncias por Mes (sin mostrar el año, ordenado)
    data_filtered['Mes'] = data_filtered['FechaSalida'].dt.month_name()  # Extraemos el nombre del mes
    mes_ordenado = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    renuncias_mes = data_filtered.groupby('Mes').size().reindex(mes_ordenado).reset_index(name='Renuncias')
    fig1 = px.line(renuncias_mes, x='Mes', y='Renuncias', title='Renuncias por Mes')
    st.plotly_chart(fig1)

    # Gráfico de Renuncias por Año
    renuncias_ano = data_filtered.groupby('AñoRenuncia').size().reset_index(name='Renuncias')
    fig2 = px.bar(renuncias_ano, x='AñoRenuncia', y='Renuncias', title='Renuncias por Año')
    st.plotly_chart(fig2)

    # Gráfico de Job Role con más Renuncias
    job_role_renuncias = data_filtered['JobRole'].value_counts().reset_index()
    job_role_renuncias.columns = ['JobRole', 'Renuncias']
    fig3 = px.bar(job_role_renuncias, x='JobRole', y='Renuncias', title="Job Role con Más Renuncias")
    st.plotly_chart(fig3)

    # Gráfico de Distribución de Antigüedad
    fig5 = px.histogram(data_filtered, x='Antigüedad', nbins=20, title="Distribución de Antigüedad de Empleados que Renunciaron")
    st.plotly_chart(fig5)

# Página - Condiciones Laborales
elif selection == "Condiciones Laborales":
    st.title("Análisis de Condiciones Laborales")
    
    # Filtros para Condiciones Laborales (por género y departamento)
    genero = st.selectbox("Selecciona el Género", ['All'] + list(data_renuncias['Gender'].unique()))
    departamento = st.selectbox("Selecciona el Departamento", ['All'] + list(data_renuncias['Department'].unique()))

    # Filtrar los datos según los filtros seleccionados
    data_filtered = data_renuncias.copy()  # Crear una copia de data_renuncias para aplicar filtros

    if genero != 'All':
        data_filtered = data_filtered[data_filtered['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]

    # Filtrar solo los empleados con contrato Indefinido o Temporal
    tipo_contrato = data_filtered[data_filtered['tipo_contrato'].isin(['indefinido', 'temporal'])]  # Filtrar solo Indefinido y Temporal
    tipo_contrato_count = tipo_contrato['tipo_contrato'].value_counts().reset_index()
    tipo_contrato_count.columns = ['Tipo de Contrato', 'Cantidad de Renuncias']  # Renombramos la columna a "Cantidad de Renuncias"

    # Gráfico circular de tipo de contrato
    fig3 = px.pie(tipo_contrato_count, names='Tipo de Contrato', values='Cantidad de Renuncias', title="Distribución de Tipo de Contrato")
    st.plotly_chart(fig3)

    # Gráfico de Última Promoción
    ultima_promocion = data_filtered['YearsSinceLastPromotion'].value_counts().reset_index()
    ultima_promocion.columns = ['Años Desde Última Promoción', 'Renuncias']
    fig6 = px.bar(ultima_promocion, x='Años Desde Última Promoción', y='Renuncias', title="Renuncias por Años Desde Última Promoción")
    st.plotly_chart(fig6)

    # Gráfico de Carga Laboral Percibida
    carga_laboral = data_filtered['JobSatisfaction'].value_counts().reset_index()
    carga_laboral.columns = ['Satisfacción Laboral', 'Renuncias']
    fig7 = px.bar(carga_laboral, x='Satisfacción Laboral', y='Renuncias', title="Renuncias por Carga Laboral Percibida")
    st.plotly_chart(fig7)

# Página - Demográficos
elif selection == "Demográficos":
    st.title("Análisis Demográfico de Empleados que Renunciaron")
    
    # Filtros para Demográficos (por género y departamento)
    genero = st.selectbox("Selecciona el Género", ['All'] + list(data_renuncias['Gender'].unique()))
    departamento = st.selectbox("Selecciona el Departamento", ['All'] + list(data_renuncias['Department'].unique()))

    # Filtrar los datos según los filtros seleccionados
    data_filtered = data_renuncias.copy()  # Crear una copia de data_renuncias para aplicar filtros

    if genero != 'All':
        data_filtered = data_filtered[data_filtered['Gender'] == genero]
    if departamento != 'All':
        data_filtered = data_filtered[data_filtered['Department'] == departamento]

    # Gráfico de Estado Civil
    estado_civil = data_filtered['MaritalStatus'].value_counts().reset_index()
    estado_civil.columns = ['Estado Civil', 'Renuncias']
    fig4 = px.pie(estado_civil, names='Estado Civil', values='Renuncias', title="Distribución de Estado Civil de los Empleados que Renunciaron")
    st.plotly_chart(fig4)

    # Gráfico de Distribución por Edad
    fig5 = px.histogram(data_filtered, x='Age', nbins=15, title="Distribución de Edad de Empleados que Renunciaron")
    st.plotly_chart(fig5)
    
    # Gráfico de Distancia desde Casa
    fig6 = px.scatter(data_filtered, x='DistanceFromHome', y='Antigüedad', title="Relación entre Distancia desde Casa y Antigüedad")
    st.plotly_chart(fig6)















