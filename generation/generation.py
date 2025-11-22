import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs(hosts_df, num_logs=5000):
    logs = []
    request_types = ['GET', 'POST', 'PUT', 'DELETE']
    status_codes = [200, 201, 400, 401, 403, 404, 500]
    
    for i in range(num_logs):
        # Usar la columna 'id' en lugar del índice
        id_server = random.choice(hosts_df['id'].values)
        timestamp = datetime.now() - timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        logs.append({
            'id_log': i,
            'id_server': id_server,
            'timestamp': timestamp,
            'request_type': random.choice(request_types),
            'response_time_ms': random.randint(50, 5000),
            'status_code': random.choice(status_codes),
            'user': f"user{random.randint(1, 999):03d}"
        })
    
    return pd.DataFrame(logs)

def generate_maintenance(hosts_df, num_maintenance=200):
    maintenance = []
    types = ['Patch', 'Incident', 'Upgrade', 'Security', 'Network']
    notes_examples = [
        "Server rebooted successfully",
        "Security patches applied",
        "Network configuration updated", 
        "Hardware upgrade completed",
        "Performance optimization done",
        "Backup verification successful",
        "Firewall rules updated",
        "OS update installed",
        "Memory replacement done",
        "Disk space cleaned up",
        "Database maintenance performed",
        "Application deployed",
        "Monitoring configured",
        "Security scan completed",
        "Backup restoration tested"
    ]
    
    for i in range(num_maintenance):
        # Usar la columna 'id' en lugar del índice
        id_server = random.choice(hosts_df['id'].values)
        date = datetime.now() - timedelta(days=random.randint(0, 180))
        
        maintenance.append({
            'id_maintenance': i,
            'id_server': id_server,
            'date': date,
            'type': random.choice(types),
            'duration_min': random.randint(5, 420),
            'technician': f"tech{random.randint(1, 999):03d}",
            'notes': random.choice(notes_examples)
        })
    
    return pd.DataFrame(maintenance)