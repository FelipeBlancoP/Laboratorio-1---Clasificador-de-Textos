import pandas as pd
import random
import ollama 
from datetime import datetime, timedelta

### 1.1. Generar datos de Logs para cada Servidor

def generate_logs(hosts_df, num_logs=5000):
    logs = []
    request_types = ['GET', 'POST', 'PUT', 'DELETE']
    status_codes = [200, 201, 400, 401, 403, 404, 500]
    
    for i in range(num_logs):
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



### 1.2. Generar datos de Mantenimientos a los Servidores

def generate_note_with_ollama():
    try:
        response = ollama.chat(
            model="qwen2.5:1.5b",
            messages=[{
                "role": "user",
                "content": (
                    "Generate exactly one short maintenance note. One sentence, max 10 words."
                    "Example: Server rebooted successfully."
                )
            }]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        print(f"[WARN] Ollama failed: {e}")
        return "Maintenance completed successfully" 

def generate_maintenance(hosts_df, num_maintenance=200):
    maintenance = []
    types = ['Patch', 'Incident', 'Upgrade', 'Security', 'Network']

    for i in range(num_maintenance):
        id_server = random.choice(hosts_df['id'].values)
        date = datetime.now() - timedelta(days=random.randint(0, 180))

        note = generate_note_with_ollama()
        print(i,note)

        maintenance.append({
            'id_maintenance': i,
            'id_server': id_server,
            'date': date,
            'type': random.choice(types),
            'duration_min': random.randint(5, 420),
            'technician': f"tech{random.randint(1, 999):03d}",
            'notes': note
        })
    
    return pd.DataFrame(maintenance)