import pandas as pd
import sqlite3
from config.config import DB_PATH

def run_report():
    conn = sqlite3.connect(DB_PATH)
    
    hosts_df = pd.read_sql_query("SELECT * FROM hosts", conn)
    logs_df = pd.read_sql_query("SELECT * FROM logs", conn)
    maintenance_df = pd.read_sql_query("SELECT * FROM maintenance", conn)
    
    conn.close()
    
    print("=== REPORTE 3.1: PANDAS ===")
    
    # 1. Servidores por país y entorno
    q1 = hosts_df.groupby(['country', 'environment']).size().reset_index(name='count')
    print("\n1. Servidores por país y entorno:")
    print(q1.to_string(index=False))
    
    # 2. Porcentaje de servidores Linux
    linux_count = (hosts_df['os'] == 'Linux').sum()
    linux_percent = (linux_count / len(hosts_df)) * 100
    print(f"\n2. Porcentaje de servidores Linux: {linux_percent:.2f}%")
    
    # 3. Servidores con mayor tiempo promedio de respuesta
    avg_response = logs_df.groupby('id_server')['response_time_ms'].mean().sort_values(ascending=False)
    print("\n3. Top 5 servidores con mayor tiempo promedio de respuesta:")
    print(avg_response.head().to_string())
    
    # 4. Tipo de request más lento
    slowest_request = logs_df.groupby('request_type')['response_time_ms'].mean().sort_values(ascending=False)
    print("\n4. Tipo de request más lento:")
    print(slowest_request.to_string())
    
    # 5. Porcentaje de solicitudes fallidas por servidor y país
    logs_with_hosts = pd.merge(logs_df, hosts_df, left_on='id_server', right_on='id')
    failed_requests = logs_with_hosts[logs_with_hosts['status_code'] >= 400]
    failed_percent = failed_requests.groupby(['id_server', 'country']).size() / logs_with_hosts.groupby(['id_server', 'country']).size() * 100
    print("\n5. Top 5 porcentaje de solicitudes fallidas por servidor y país:")
    print(failed_percent.head().to_string())
    
    # 6. Tipo de mantenimiento más largo
    longest_maintenance = maintenance_df.groupby('type')['duration_min'].mean().sort_values(ascending=False)
    print("\n6. Tipo de mantenimiento más largo (promedio):")
    print(longest_maintenance.to_string())
    
    # 7. Técnico con más intervenciones
    top_technician = maintenance_df['technician'].value_counts().head(1)
    print("\n7. Técnico con más intervenciones:")
    print(top_technician.to_string())
    
    # 8. Horas de mantenimiento por servidor
    maintenance_hours = maintenance_df.groupby('id_server')['duration_min'].sum() / 60
    print("\n8. Top 5 horas de mantenimiento por servidor:")
    print(maintenance_hours.head().to_string())