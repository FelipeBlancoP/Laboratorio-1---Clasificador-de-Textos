import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def run_eda(df):
    
    results = {}
    
    # 1. Matriz de Correlación
    
    correlation_cols = [
        'CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)',
        'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
        'PT08.S5(O3)', 'T', 'RH', 'AH'
    ]
    df_corr = df.dropna(subset=correlation_cols).copy()
    corr_matrix = df_corr[correlation_cols].corr()

    fig_heatmap, ax_heatmap = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap='viridis',
        linewidths=.5,
        cbar_kws={'label': 'Coeficiente de Correlación de Pearson'},
        ax=ax_heatmap
    )
    ax_heatmap.set_title('Matriz de Correlación entre Sensores, Concentraciones y Ambiente')
    results['heatmap'] = fig_heatmap
    results['corr_matrix_df'] = corr_matrix


    # 2. Tendencia temporal de Concentraciones GT

    gt_cols = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    df_trend_gt = df[['DateTime'] + gt_cols].set_index('DateTime').copy()

    df_trend_gt.replace([np.inf, -np.inf], np.nan, inplace=True) 
    df_smooth_gt = df_trend_gt.rolling(window=168, min_periods=1).mean()

    fig_gt, ax_gt = plt.subplots(figsize=(15, 6))
    df_smooth_gt.plot(ax=ax_gt, linewidth=1.5)

    ax_gt.set_title('Tendencia Temporal de Concentraciones Reales (GT)', fontsize=14)
    ax_gt.set_xlabel('Fecha', fontsize=12)
    ax_gt.set_ylabel('Concentración (Promedio Móvil)', fontsize=12)
    ax_gt.legend(title='Contaminante')
    ax_gt.grid(True)
    results['trend_gt'] = fig_gt


    # 3. Tendencia temporal de Lecturas de Sensores MOX

    sensor_cols = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)']
    df_trend_sensors = df[['DateTime'] + sensor_cols].set_index('DateTime').copy()

    df_trend_sensors.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_smooth_sensors = df_trend_sensors.rolling(window=168, min_periods=1).mean()

    fig_sensors, ax_sensors = plt.subplots(figsize=(15, 6))
    df_smooth_sensors.plot(ax=ax_sensors, linewidth=1.5)

    ax_sensors.set_title('Tendencia Temporal de Lecturas de Sensores MOX', fontsize=14)
    ax_sensors.set_xlabel('Fecha', fontsize=12)
    ax_sensors.set_ylabel('Señal del Sensor (Promedio Móvil)', fontsize=12)
    ax_sensors.legend(title='Sensor')
    ax_sensors.grid(True)
    results['trend_sensors'] = fig_sensors


    # 4. Concentraciones reales(GT) vs Días laborales/Fines de semana
    
    gt_cols_box = ['CO(GT)', 'C6H6(GT)', 'NOx(GT)', 'NO2(GT)']
    titles = {
        'CO(GT)': 'Monóxido de Carbono (mg/m³)',
        'C6H6(GT)': 'Benceno (µg/m³)',
        'NOx(GT)': 'Óxidos de Nitrógeno (ppb)',
        'NO2(GT)': 'Dióxido de Nitrógeno (µg/m³)'
    }

    fig_box, axes_box = plt.subplots(2, 2, figsize=(14, 10), sharex=True)
    axes_box = axes_box.flatten() 

    fig_box.suptitle('Comparación de Concentraciones Reales (GT): Días Laborales vs. Fines de Semana', fontsize=16, y=1.02)

    for i, col in enumerate(gt_cols_box):
        ax = axes_box[i]
        
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

    axes_box[2].set_xlabel('Tipo de Día (0=Laboral, 1=Fin de Semana)', fontsize=12)
    axes_box[3].set_xlabel('Tipo de Día (0=Laboral, 1=Fin de Semana)', fontsize=12)
    plt.tight_layout(rect=[0, 0, 1, 0.98]) 
    results['boxplots_gt'] = fig_box
    
    
    plt.close('all')

    return results

def plot_sensor_trend(df):
    sensor_cols = ['PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S3(NOx)', 'PT08.S4(NO2)', 'PT08.S5(O3)']
    
    df_trend_sensors = df[['DateTime'] + sensor_cols].set_index('DateTime').copy()

    df_trend_sensors.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_smooth_sensors = df_trend_sensors.rolling(window=168, min_periods=1).mean()

    fig_sensors, ax_sensors = plt.subplots(figsize=(15, 6))
    df_smooth_sensors.plot(ax=ax_sensors, linewidth=1.5)

    ax_sensors.set_title("Tendencia Temporal de Lecturas de Sensores MOX")
    ax_sensors.set_xlabel("Fecha")
    ax_sensors.set_ylabel("Promedio Móvil")
    ax_sensors.grid(True)
    ax_sensors.legend(title="Sensor")

    return fig_sensors