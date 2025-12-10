import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

def run_model_2(df: pd.DataFrame):
    
    results = {'figure': None, 'metrics': {}, 'coefficients': {}}

    SENSOR_COL = 'PT08.S1(CO)'
    TIME_COL = 'DateTime'
    
    df_drift = df.copy()
    df_drift[TIME_COL] = pd.to_datetime(df_drift[TIME_COL], errors='coerce')
    df_drift = df_drift.dropna(subset=[SENSOR_COL, TIME_COL])


    start_time = df_drift[TIME_COL].min()
    df_drift['Days_Elapsed'] = (df_drift[TIME_COL] - start_time).dt.total_seconds() / (60 * 60 * 24)
    
    X = df_drift['Days_Elapsed'].values.reshape(-1, 1) 
    Y = df_drift[SENSOR_COL].values 
    
    
    DEGREE = 2
    
    poly_features = PolynomialFeatures(degree=DEGREE)
    X_poly = poly_features.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, Y)
    Y_drift_pred = model.predict(X_poly)


    rmse = np.sqrt(mean_squared_error(Y, Y_drift_pred))
    r2 = r2_score(Y, Y_drift_pred)
    
    
    results['metrics']['RMSE'] = rmse
    results['metrics']['R2'] = r2
    
    results['coefficients']['Intercepto'] = model.intercept_
    results['coefficients']['Grado_1_Lineal'] = model.coef_[1]
    if DEGREE >= 2:
        results['coefficients']['Grado_2_Curvatura'] = model.coef_[2]
    

    df_plot = pd.DataFrame({'Time': X.flatten(), 'Actual': Y, 'Predicted': Y_drift_pred})
    df_plot = df_plot.sort_values(by='Time')

    fig, ax = plt.subplots(figsize=(15, 6))
    
    
    df_smooth = df_drift[[TIME_COL, SENSOR_COL]].set_index(TIME_COL).rolling(window=168, min_periods=1).mean()
    ax.plot(df_smooth.index, df_smooth[SENSOR_COL], label='Señal del Sensor (Suavizada)', alpha=0.6, color='skyblue')


    ax.plot(df_drift[TIME_COL].iloc[df_plot['Time'].index], df_plot['Predicted'], 
             color='red', linewidth=3, label=f'Curva de Deriva Ajustada (Grado {DEGREE})')

    ax.set_title(f'Modelamiento del Sensor Drift: {SENSOR_COL} vs. Tiempo', fontsize=16)
    ax.set_xlabel('Fecha', fontsize=12)
    ax.set_ylabel('Señal del Sensor', fontsize=12)
    ax.legend()
    ax.grid(True)
    
    results['figure'] = fig
    
    plt.close(fig)
    
    return results