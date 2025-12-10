import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt

def run_model_2(df: pd.DataFrame):

    SENSOR_COL = 'PT08.S1(CO)'
    TIME_COL = 'DateTime'
    
    df_drift = df.copy()
    df_drift[TIME_COL] = pd.to_datetime(df_drift[TIME_COL], errors='coerce')
    df_drift = df_drift.dropna(subset=[SENSOR_COL, TIME_COL])


    start_time = df_drift[TIME_COL].min()
    df_drift['Days_Elapsed'] = (df_drift[TIME_COL] - start_time).dt.total_seconds() / (60 * 60 * 24)
    
    X = df_drift['Days_Elapsed'].values.reshape(-1, 1) 
    Y = df_drift[SENSOR_COL].values 
    
    print(f"Modelando deriva para el sensor: {SENSOR_COL}")

    #Regresión Polinomial
 
    DEGREE = 2
    
    poly_features = PolynomialFeatures(degree=DEGREE)
    X_poly = poly_features.fit_transform(X)

    model = LinearRegression()
    model.fit(X_poly, Y)
    Y_drift_pred = model.predict(X_poly)


    rmse = np.sqrt(mean_squared_error(Y, Y_drift_pred))
    r2 = r2_score(Y, Y_drift_pred)
    
    print(f"\n--- Modelo Polinomial (Grado {DEGREE}) ---")
    print(f"RMSE: {rmse:.4f}")
    print(f"R^2 : {r2:.4f}")
    
    print("\nCoeficientes Polinomiales:")
    print(f"Intercepto: {model.intercept_:.4f}")
    print(f"Coeficiente Grado 1 (Lineal): {model.coef_[1]:.4f}")
    if DEGREE >= 2:
        print(f"Coeficiente Grado 2 (Curvatura): {model.coef_[2]:.4f}")
   

    df_plot = pd.DataFrame({'Time': X.flatten(), 'Actual': Y, 'Predicted': Y_drift_pred})
    df_plot = df_plot.sort_values(by='Time')

    plt.figure(figsize=(15, 6))
    

    df_smooth = df_drift[[TIME_COL, SENSOR_COL]].set_index(TIME_COL).rolling(window=168, min_periods=1).mean()
    plt.plot(df_smooth.index, df_smooth[SENSOR_COL], label='Señal del Sensor (Suavizada)', alpha=0.6, color='skyblue')


    plt.plot(df_drift[TIME_COL].iloc[df_plot['Time'].index], df_plot['Predicted'], 
             color='red', linewidth=3, label=f'Curva de Deriva Ajustada (Grado {DEGREE})')

    plt.title(f'Modelamiento del Sensor Drift: {SENSOR_COL} vs. Tiempo', fontsize=16)
    plt.xlabel('Fecha', fontsize=12)
    plt.ylabel('Señal del Sensor', fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.show()
    
    print("Fin modelamientpo 2")
