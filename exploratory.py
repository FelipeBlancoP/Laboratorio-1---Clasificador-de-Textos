import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#df = pd.read_csv("data/processed/AirQuality_processed.csv")

def run_eda(df):
    print("Matriz de correlacion solo de datos de sensores y T, RH, AH")
    correlation_cols = [
        'CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)',
        'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
        'PT08.S5(O3)', 'T', 'RH', 'AH'
    ]
    corr_matrix = df[correlation_cols].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap='viridis',
        linewidths=.5,
        cbar_kws={'label': 'Coeficiente de Correlación de Pearson'}
    )
    plt.title('Matriz de Correlación entre Sensores, Concentraciones y Ambiente')
    plt.show()



    print("Gráfico: Tendencia temporal de todas las concentraciones GT")

    gt_cols = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df_trend = df[['DateTime'] + gt_cols].set_index('DateTime').copy()

    df_smooth = df_trend.rolling(window=168, min_periods=1).mean()

    plt.figure(figsize=(15, 6))
    df_smooth.plot(ax=plt.gca(), linewidth=1.5)

    plt.title('Tendencia Temporal de Concentraciones Reales (GT)', fontsize=14)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Concentración (Normalizada en la Gráfica)', fontsize=12)
    plt.legend(title='Contaminante')
    plt.grid(True)
    plt.show()



    print("Gráfico: Tendencia temporal de lecturas de sensores MOX")

    sensor_cols = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)']
    df_trend_sensors = df[['DateTime'] + sensor_cols].set_index('DateTime').copy()

    df_smooth_sensors = df_trend_sensors.rolling(window=168, min_periods=1).mean()

    plt.figure(figsize=(15, 6))
    df_smooth_sensors.plot(ax=plt.gca(), linewidth=1.5)

    plt.title('Tendencia Temporal de Lecturas de Sensores MOX', fontsize=14)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Señal del Sensor (Valor Crudo)', fontsize=12)
    plt.legend(title='Sensor')
    plt.grid(True)
    plt.show()




    print("Gráfico: Concentraciones reales(GT) vs Días laborales/Fines de semana")
    gt_cols = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    titles = {
        'CO(GT)': 'Monóxido de Carbono (mg/m³)',
        'C6H6(GT)': 'Benceno (µg/m³)',
        'NOx(GT)': 'Óxidos de Nitrógeno (ppb)',
        'NO2(GT)': 'Dióxido de Nitrógeno (µg/m³)'
    }

    fig, axes = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axes = axes.flatten() 

    plt.suptitle('Comparación de Concentraciones Reales (GT): Días Laborales vs. Fines de Semana', fontsize=16, y=1.02)

    for i, col in enumerate(gt_cols):
        ax = axes[i]
        
        sns.boxplot(
            x='is_weekend',
            y=col,
            data=df.dropna(subset=[col, 'is_weekend']),
            palette=['lightcoral', 'skyblue'],
            ax=ax
        )
        
        ax.set_title(f'{col} ({titles[col]})', fontsize=12)
        ax.set_xlabel('') 
        ax.set_ylabel('Concentración', fontsize=10)
        ax.set_xticklabels(['Día Laboral', 'Fin de Semana'])

    axes[2].set_xlabel('Tipo de Día (0=Laboral, 1=Fin de Semana)', fontsize=12)
    axes[3].set_xlabel('Tipo de Día (0=Laboral, 1=Fin de Semana)', fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 
    plt.show()
