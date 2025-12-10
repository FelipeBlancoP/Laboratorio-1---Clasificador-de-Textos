import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import seaborn as sns

sys.path.append(os.path.join(os.path.dirname(__file__), 'streamlit'))


from exploratory_streamlit import run_eda,plot_sensor_trend
from model_1_streamlit import run_model_1
from model_2_streamlit import run_model_2
from r_streamlit import classify_days


@st.cache_data
def load_data(path="data/processed/AirQuality_processed.csv"):
    """Carga el DataFrame y realiza la limpieza/conversión inicial."""
    try:
        df = pd.read_csv(path)
        df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
        df['month'] = pd.to_numeric(df['month'], errors='coerce')
        df['is_weekend'] = pd.to_numeric(df['is_weekend'], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error(f"Error: Archivo de datos procesados no encontrado en {path}. Asegúrate de ejecutar main.py primero.")
        return pd.DataFrame()

df_original = load_data()


# APLICACIÓN PRINCIPAL DE STREAMLIT

def main_app():
    
    if df_original.empty:
        return
    
    with st.spinner("Calculando modelos de calibración y deriva..."):
        model_1_results = run_model_1(df_original)

        model_2_results = run_model_2(df_original)


    st.title("Descifrando la Respiración de la Ciudad: Calidad del Aire")
    st.subheader("Laboratorio 3: Programación Científica")
    st.markdown("""
    Cada hora, durante un año, unos pequeños sensores respiraron el aire de una de las calles más contaminadas de Italia. 
    Lo registró todo: gases tóxicos, cambios de temperatura, humedad y hasta sus propias fallas. 
    Ese pulso urbano quedó guardado en un dataset de 9.358 registros horarios, el cual hoy se transforma en el corazón de este dashboard.
    El desafío es tomar esas señales crudas, ruidosas, inestables, con desgaste temporal y convertirlas en conocimiento. 
    """)
    st.markdown("---")

    

    #EXPLORACIÓN

    st.header("1. Exploración de Datos y Tendencias")
    st.subheader("1.1. Tendencia Temporal de Sensores MOX (Filtrable por Fecha)")
    st.write("Este gráfico muestra la evolución temporal de los sensores MOX.")


    min_date = df_original['DateTime'].min().date()
    max_date = df_original['DateTime'].max().date()

    date_range = st.slider(
        'Rango de Fechas para Zoom Temporal',
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY/MM/DD",
        key='slider_fechas',
        help="Permite hacer zoom en un periodo específico para ver las mediciones MOX."
     )
    
    df_filtered_dates = df_original[
    (df_original['DateTime'].dt.date >= date_range[0]) &
    (df_original['DateTime'].dt.date <= date_range[1])
    ]


    #Grafico filtrable por fecha de mediciones de mox

    if df_filtered_dates.empty:
        st.warning("No hay datos en el rango seleccionado.")
    else:
        fig_sensores = plot_sensor_trend(df_filtered_dates)
        st.pyplot(fig_sensores)
        plt.close(fig_sensores)


    
    st.subheader("1.2. Matriz de Correlación")
    st.write("Muestra la relación entre sensores, contaminantes (GT) y variables ambientales.")
    
    correlation_cols = ['CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)', 'T', 'RH', 'AH']
    corr_matrix = df_original[correlation_cols].corr()
    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='viridis', linewidths=.5, ax=ax_heatmap)
    ax_heatmap.set_title('Matriz de Correlación Completa')
    st.pyplot(fig_heatmap)
    plt.close(fig_heatmap)


    st.subheader("1.3. Tendencias Temporales de GT")
    st.write("Visualización del cambio en las concentraciones reales (GT) a lo largo del tiempo.")
    
    gt_cols = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df_trend = df_original[['DateTime'] + gt_cols].set_index('DateTime').copy()
    df_smooth = df_trend.rolling(window=168, min_periods=1).mean()

    fig_trend, ax_trend = plt.subplots(figsize=(15, 6))
    df_smooth.plot(ax=ax_trend, linewidth=1.5)
    ax_trend.set_title('Tendencia Temporal de Concentraciones Reales (GT)', fontsize=14)
    ax_trend.set_xlabel('Fecha')
    ax_trend.set_ylabel('Concentración')
    ax_trend.legend(title='Contaminante')
    st.pyplot(fig_trend)
    plt.close(fig_trend)

    date_range

    st.markdown("---")


    # 3. MODELAMIENTO I y II
    st.header("2. Calibración y Modelamiento del Desgaste (Drift)")
    
    
    st.subheader("2.1. Modelamiento I: Calibración Univariable")
    
    st.info("Modelo 1: PT08.S1 (CO) vs CO(GT) (Lineal)")
    st.code(f"Ecuación: {model_1_results['equations']['univariable_1']}")
    st.pyplot(model_1_results['figures']['univariable_1']) 
    
    st.info("Modelo 2: PT08.S2 (NMHC) vs NMHC(GT) (Cuadrático)")
    st.code(f"Ecuación: {model_1_results['equations']['univariable_2']}")
    st.pyplot(model_1_results['figures']['univariable_2'])

    st.info("Modelo 3: PT08.S3 (NOx) vs NOx(GT) (Lineal)")
    st.code(f"Ecuación: {model_1_results['equations']['univariable_3']}")
    st.pyplot(model_1_results['figures']['univariable_3']) 

    st.subheader("2.1.2. Modelamiento I: Regresión Multivariable")
    st.pyplot(model_1_results['figures']['multivariable']) 
    
    

    st.subheader("2.2. Modelamiento II: Cambio del Sensor en el tiempo (PT08.S1)")
    st.write("El modelo polinomial (Grado 2) cuantifica el cambio sistemático en la respuesta del sensor a lo largo del tiempo.")
    

    st.code(f"R²: {model_2_results['metrics']['R2']:.4f}, RMSE: {model_2_results['metrics']['RMSE']:.4f}")
    
    st.pyplot(model_2_results['figure']) 

    
    st.markdown("---")





    st.header("3. Clasificación de Calidad del Aire")
    st.write("""
    En esta sección se categorizan las mediciones individuales según sus niveles de contaminación
    y además se clasifica cada día completo como **Normal** o **Contaminado** según el promedio diario de CO.
    """)

    st.subheader("Configurar Umbral para Clasificación")
    umbral = st.slider(
        "Umbral de CO(GT) para definir 'Mala' calidad del aire (mg/m3)",
        min_value=0.5,
        max_value=5.0,
        value=1.5,
        step=0.1
    )

    df_original["air_quality"] = df_original["CO(GT)"].apply(
        lambda x: "Buena" if x <= umbral else "Mala"
    )


    daily = df_original.groupby("Date")["CO(GT)"].mean().reset_index()
    daily["day_type"] = daily["CO(GT)"].apply(
        lambda x: "Bueno" if x <= umbral else "Malo"
    )

    st.subheader("Distribución por categoría (todos los registros)")
    counts = df_original["air_quality"].value_counts()


    fig1, ax1 = plt.subplots()
    wedges1, texts1, autotexts1 = ax1.pie(
        counts.values,
        labels=counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax1.axis("equal")
    ax1.legend(
        wedges1,
        counts.index,
        title="Categorías",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    st.pyplot(fig1)


    st.subheader("Clasificación de Días (Promedio Diario)")

    day_counts = daily["day_type"].value_counts().sort_index()
    total_days = day_counts.sum()

    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(day_counts.index, day_counts.values)


    ax.set_ylabel("Cantidad de días")
    ax.set_title("Días Buenos vs Días Malos")


    for bar in bars:
        height = bar.get_height()
        pct = (height / total_days) * 100
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{int(height)} días\n({pct:.1f}%)",
            ha='center',
            va='bottom',
            fontsize=10
        )

    st.pyplot(fig)
  
    st.markdown("---")
    

if __name__ == "__main__":
    main_app()