from generation.generation import generate_logs, generate_maintenance
from storage.storage import setup_database
from reports.report_r31 import run_report as run_r31
from reports.report_r32 import run_report as run_r32
from reports.report_r33 import run_report as run_r33
import pandas as pd
import os

def main():
    print("=== LABORATORIO 2 - ANÁLISIS DE DATOS ===")
    
    if not os.path.exists('data/hosts.csv'):
        print("ERROR: No se encuentra data/hosts.csv")
        return
    
    print("Cargando datos de hosts...")
    hosts_df = pd.read_csv('data/hosts.csv')
    
    hosts_df = hosts_df.reset_index().rename(columns={'index': 'id'})
    print(f"Se cargaron {len(hosts_df)} servidores")
    
    print("Generando logs...")
    logs_df = generate_logs(hosts_df, 5000)
    print(f"Se generaron {len(logs_df)} logs")
    
    print("Generando datos de mantenimiento...")
    maintenance_df = generate_maintenance(hosts_df, 200)
    print(f"Se generaron {len(maintenance_df)} registros de mantenimiento")
    
    print("Almacenando en base de datos...")
    setup_database(hosts_df, logs_df, maintenance_df)
    
    print("\n" + "="*50)
    run_r31()
    
    input("\nPresiona Enter para continuar con el siguiente reporte...")
    run_r32()
    
    input("\nPresiona Enter para continuar con el siguiente reporte...")
    run_r33()
    
    print("\n" + "="*50)
    print("Proceso completado!")

if __name__ == "__main__":
    main()