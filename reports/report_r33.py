import sqlite3
import pandas as pd
from config.config import DB_PATH

def run_report():
    conn = sqlite3.connect(DB_PATH)
    
    queries = {
        "1. Servidores por país y entorno": """
            SELECT country, environment, COUNT(*) as count 
            FROM hosts 
            GROUP BY country, environment
            ORDER BY country, environment
        """,
        
        "2. Sistemas operativos predominantes en Producción": """
            SELECT os, COUNT(*) as count 
            FROM hosts 
            WHERE environment = 'Production' 
            GROUP BY os 
            ORDER BY count DESC
        """,
        
        "3. Servidor con más mantenimientos": """
            SELECT h.hostname, COUNT(*) as maintenance_count 
            FROM maintenance m 
            JOIN hosts h ON m.id_server = h.id 
            GROUP BY m.id_server 
            ORDER BY maintenance_count DESC 
            LIMIT 5
        """,
        
        "4. Entornos con más errores HTTP": """
            SELECT h.environment, COUNT(*) as error_count 
            FROM logs l 
            JOIN hosts h ON l.id_server = h.id 
            WHERE l.status_code >= 400 
            GROUP BY h.environment 
            ORDER BY error_count DESC
        """,
        
        "5. Técnico con más servidores de producción": """
            SELECT m.technician, COUNT(DISTINCT m.id_server) as server_count 
            FROM maintenance m 
            JOIN hosts h ON m.id_server = h.id 
            WHERE h.environment = 'Production' 
            GROUP BY m.technician 
            ORDER BY server_count DESC 
            LIMIT 5
        """,
        
        "6. Solicitudes totales por país y mes": """
            SELECT h.country, strftime('%Y-%m', l.timestamp) as month, COUNT(*) as request_count 
            FROM logs l 
            JOIN hosts h ON l.id_server = h.id 
            GROUP BY h.country, month 
            ORDER BY month, country
            LIMIT 10
        """
    }
    
    print("=== REPORTE 3.3: SQL ===")
    
    for title, query in queries.items():
        print(f"\n{title}:")
        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))
        print("-" * 50)
    
    conn.close()