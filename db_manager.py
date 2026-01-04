import sqlite3
import json

DB_FILE = "predictions.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                results TEXT NOT NULL
            );
        """)
        conn.commit()

def save_predictions(dataset_name, predictions_dict):
    """Saves predictions as JSON object with team as key."""
    with sqlite3.connect(DB_FILE) as conn:
        results_json = json.dumps(predictions_dict, ensure_ascii=False)
        conn.execute("INSERT INTO predictions (name, results) VALUES (?, ?)", (dataset_name, results_json))
        conn.commit()

def get_all_datasets():
    with sqlite3.connect(DB_FILE) as conn:
        return conn.execute("SELECT id, name, results FROM predictions ORDER BY id DESC").fetchall()
