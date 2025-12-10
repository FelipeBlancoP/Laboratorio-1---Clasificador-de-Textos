import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def run_model_1(df: pd.DataFrame):


    numerical_cols = [
        'CO(GT)', 'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)',
        'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)',
        'PT08.S5(O3)', 'T', 'RH', 'AH'
    ]

    df_model = df.dropna(subset=numerical_cols).copy()


    #MODELOS UNIVARIABLES
    
    def linear_func(X, a, b):
        return a * X + b

    def quadratic_func(X, a, b, c):
        return a * X**2 + b * X + c

    modelos_univariables = [
        ('PT08.S1(CO)', 'CO(GT)', linear_func, 'Lineal'),
        ('PT08.S2(NMHC)', 'NMHC(GT)', quadratic_func, 'Cuadrático'),
        ('PT08.S3(NOx)', 'NOx(GT)', linear_func, 'Lineal')
    ]

    print("\n--- Modelos Univariables ---")

    for sensor, gt_col, func, model_type in modelos_univariables:
        X = df_model[sensor]
        Y = df_model[gt_col]

        try:
            popt, pcov = curve_fit(func, X, Y)
        except RuntimeError:
            print(f"Error: No se pudo ajustar la curva para {sensor} vs {gt_col}")
            continue

        Y_pred = func(X, *popt)
        rmse = np.sqrt(mean_squared_error(Y, Y_pred))
        r2 = r2_score(Y, Y_pred)

        print(f"\n[MODELO] {sensor} vs {gt_col} ({model_type})")
        

        if model_type == 'Lineal':
            print(f"Ecuación: {gt_col} = {popt[0]:.4f} * {sensor} + {popt[1]:.4f}")
        elif model_type == 'Cuadrático':
            print(f"Ecuación: {gt_col} = {popt[0]:.4f} * {sensor}^2 + {popt[1]:.4f} * {sensor} + {popt[2]:.4f}")
            
        print(f"RMSE: {rmse:.4f}, R^2: {r2:.4f}")

        plt.figure(figsize=(8, 6))
        plt.scatter(X, Y, label='Datos Reales', alpha=0.3)
        
        x_fit = np.linspace(X.min(), X.max(), 100)
        y_fit = func(x_fit, *popt)
        plt.plot(x_fit, y_fit, color='red', linewidth=3, label=f'Ajuste {model_type}')
        
        plt.title(f'Calibración Univariable: {sensor} vs {gt_col} ($R^2={r2:.2f}$)')
        plt.xlabel(f'Señal del Sensor ({sensor})')
        plt.ylabel(f'Concentración Real ({gt_col})')
        plt.legend()
        plt.show()

    
    # MODELO MULTIVARIABLE

    TARGET_COL = 'CO(GT)'
    FEATURE_COLS = [
        'PT08.S1(CO)', 'PT08.S2(NMHC)', 'PT08.S5(O3)', 
        'T', 'RH', 'AH' 
    ]
    
    print("\nModelo Multivariable (Regresión Lineal Múltiple)")

    X = df_model[FEATURE_COLS]
    Y = df_model[TARGET_COL]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

    model = LinearRegression()
    model.fit(X_train, Y_train)

    Y_pred = model.predict(X_test)
    rmse_multi = np.sqrt(mean_squared_error(Y_test, Y_pred))
    r2_multi = r2_score(Y_test, Y_pred)

    print("\nResultados del Modelo:")
    print(f"Intercepto (b): {model.intercept_:.4f}")
    print("Coeficients:")
    for feature, coef in zip(FEATURE_COLS, model.coef_):
        print(f"  - {feature}: {coef:.4f}")

    print(f"\nMétricas: RMSE={rmse_multi:.4f}, R^2={r2_multi:.4f}")

    plt.figure(figsize=(8, 6))
    plt.scatter(Y_test, Y_pred, alpha=0.5)
    plt.plot([Y.min(), Y.max()], [Y.min(), Y.max()], 'r--', lw=2) 
    plt.title(f'Modelo Multivariable: Predicción vs Real ({TARGET_COL})')
    plt.xlabel(f'Concentración Real ({TARGET_COL})')
    plt.ylabel(f'Concentración Predicha ({TARGET_COL})')
    plt.grid(True)
    plt.show()

    print("Fin Modelo 1")