import sqlite3
import pandas as pd
from config.config import DB_PATH

def create_tables(conn):
    schema_sql = """
    BEGIN;

    DROP TABLE IF EXISTS logs;
    DROP TABLE IF EXISTS maintenance;
    DROP TABLE IF EXISTS hosts;
    
    CREATE TABLE IF NOT EXISTS hosts (
        id INTEGER PRIMARY KEY,
        hostname TEXT NOT NULL UNIQUE,
        os TEXT NOT NULL,
        environment TEXT NOT NULL,
        country TEXT NOT NULL,
        node TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS logs (
        id_log INTEGER PRIMARY KEY,
        id_server INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        request_type TEXT NOT NULL,
        response_time_ms INTEGER NOT NULL,
        status_code INTEGER NOT NULL,
        user TEXT NOT NULL,
        FOREIGN KEY (id_server) REFERENCES hosts(id)
    );
    
    CREATE TABLE IF NOT EXISTS maintenance (
        id_maintenance INTEGER PRIMARY KEY,
        id_server INTEGER NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        duration_min INTEGER NOT NULL,
        technician TEXT NOT NULL,
        notes TEXT NOT NULL,
        FOREIGN KEY (id_server) REFERENCES hosts(id)
    );
    
    COMMIT;
    """
    conn.executescript(schema_sql)

def insert_df(name, df, conn):
    if len(df) == 0:
        return
    if 'index' in df.columns:
        df = df.drop(columns=['index'])
    df.to_sql(name, conn, if_exists="append", index=False)

def setup_database(hosts_df, logs_df, maintenance_df):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    create_tables(conn)
    
    insert_df("hosts", hosts_df, conn)
    insert_df("logs", logs_df, conn)
    insert_df("maintenance", maintenance_df, conn)
    
    conn.commit()
    conn.close()
    print("Base de datos creada exitosamente!")