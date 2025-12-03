import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from wordcloud import WordCloud
from config.config import DB_PATH

def run_report():
    conn = sqlite3.connect(DB_PATH)
    
    hosts_df = pd.read_sql_query("SELECT * FROM hosts", conn)
    logs_df = pd.read_sql_query("SELECT * FROM logs", conn)
    maintenance_df = pd.read_sql_query("SELECT * FROM maintenance", conn)
    
    conn.close()
    
    print("=== REPORTE 3.2: PANDAS + MATPLOTLIB ===")
    
    fig, axes = plt.subplots(2, 2, figsize=(18, 10))
    ax1, ax2, ax3, ax4 = axes.flatten()

    #1) OS por país (gráfico de barras)
    os_country = pd.crosstab(hosts_df['country'], hosts_df['os'])
    os_country.plot(kind='bar', ax=ax1)
    ax1.set_title("Sistemas Operativos por País")
    ax1.set_xlabel("País")
    ax1.set_ylabel("Cantidad de Hosts")
    ax1.legend(title="OS")
    ax1.tick_params(axis='x', rotation=45)


    #2) Pie chart de sistemas operativos totales
    total_os = hosts_df['os'].value_counts()
    ax2.pie(total_os, labels=total_os.index, autopct='%1.2f%%')
    ax2.set_title("Total de Sistemas Operativos")

    #3) Total hosts por país (barras horizontal)
    hosts_by_country = hosts_df['country'].value_counts().sort_values()
    hosts_by_country.plot(kind='barh', ax=ax3, color='lightgreen')
    ax3.set_title("Total hosts por país")
    ax3.set_xlabel("Cantidad de Hosts")
    ax3.set_ylabel("País")

    #4) Hosts por país agrupados por environment
    env_country = pd.crosstab(hosts_df['environment'], hosts_df['country'])
    env_country.plot(kind='bar', ax=ax4)
    ax4.set_title("Servidores por país agrupados por entorno")
    ax4.set_xlabel("Entorno")
    ax4.set_ylabel("Cantidad de Servidores")
    ax4.legend(title="País")
    ax4.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()
    
    
    logs_df['hour'] = pd.to_datetime(logs_df['timestamp']).dt.hour
    plt.figure(figsize=(10, 6))
    plt.scatter(logs_df['hour'], logs_df['response_time_ms'], alpha=0.3, s=10)
    plt.xlabel('Hora del día')
    plt.ylabel('Tiempo de respuesta (ms)')
    plt.title('Tiempo de respuesta por hora del día')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    text = ' '.join(maintenance_df['notes'].dropna())
    if text.strip():
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Nube de palabras - Notas de mantenimiento')
        plt.show()
    else:
        print("No hay notas de mantenimiento para generar nube de palabras")
    
    merged = pd.merge(logs_df, hosts_df, left_on='id_server', right_on='id')
    country_response = merged.groupby('country')['response_time_ms'].mean()
    maintenance_with_hosts = pd.merge(maintenance_df, hosts_df, left_on='id_server', right_on='id')
    country_maintenance = maintenance_with_hosts.groupby('country')['duration_min'].mean()
    
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    bars = ax1.bar(country_response.index, country_response.values, alpha=0.7, label='Tiempo respuesta (ms)', color='lightblue')
    ax1.set_ylabel('Tiempo respuesta (ms)', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xlabel('País')
    
    ax2 = ax1.twinx()
    line = ax2.plot(country_maintenance.index, country_maintenance.values, color='red', marker='o', linewidth=2, label='Duración mantenimiento (min)')
    ax2.set_ylabel('Duración mantenimiento (min)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')
    
    plt.title('Relación mantenimientos vs tiempos de respuesta por país')
    plt.xticks(rotation=45)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    logs_df['month'] = pd.to_datetime(logs_df['timestamp']).dt.to_period('M')
    monthly_response = logs_df.groupby('month')['response_time_ms'].mean()
    
    plt.figure(figsize=(12, 6))
    monthly_response.plot(kind='line', marker='o', linewidth=2)
    plt.title('Tiempo de respuesta promedio por mes')
    plt.ylabel('Tiempo de respuesta (ms)')
    plt.xlabel('Mes')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()