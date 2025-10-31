import sqlite3
import pandas as pd
import json
from collections import defaultdict
import os

# --- Configuration ---
DLT_CSV = 'dlt_lottery_data.csv'
SSQ_CSV = 'ssq_lottery_data.csv'
DLT_DB = 'dlt_results.db'
SSQ_DB = 'ssq_results.db'
DLT_MODEL_JSON = 'dlt_markov_model_features.json'
SSQ_MODEL_JSON = 'ssq_markov_model_features.json'

# --- Database Update Functions ---

def create_dlt_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draw_results (
            issue_number TEXT PRIMARY KEY,
            draw_date TEXT,
            red_ball_1 INTEGER,
            red_ball_2 INTEGER,
            red_ball_3 INTEGER,
            red_ball_4 INTEGER,
            red_ball_5 INTEGER,
            blue_ball_1 INTEGER,
            blue_ball_2 INTEGER,
            sales_amount TEXT,
            jackpot_amount TEXT
        )
    """)
    conn.commit()

def create_ssq_table(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS draw_results (
            issue_number TEXT PRIMARY KEY,
            draw_date TEXT,
            red_ball_1 INTEGER,
            red_ball_2 INTEGER,
            red_ball_3 INTEGER,
            red_ball_4 INTEGER,
            red_ball_5 INTEGER,
            red_ball_6 INTEGER,
            blue_ball_1 INTEGER,
            sales_amount TEXT,
            jackpot_amount TEXT
        )
    """)
    conn.commit()

def update_database(csv_path, db_path, create_table_func, lottery_type):
    print(f"--- Updating {lottery_type} Database: {db_path} ---")
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return

    conn = sqlite3.connect(db_path)
    create_table_func(conn)
    cursor = conn.cursor()
    
    # Prepare data for insertion
    if lottery_type == 'dlt':
        df = df[["issue_number", "draw_date", "red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5", "blue_ball_1", "blue_ball_2", "sales_amount", "jackpot_amount"]]
        insert_sql = """
            INSERT OR REPLACE INTO draw_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    elif lottery_type == 'ssq':
        df = df[["issue_number", "draw_date", "red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5", "red_ball_6", "blue_ball_1", "sales_amount", "jackpot_amount"]]
        insert_sql = """
            INSERT OR REPLACE INTO draw_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
    else:
        print(f"Unknown lottery type: {lottery_type}")
        conn.close()
        return

    # Insert data
    inserted_count = 0
    for row in df.itertuples(index=False):
        try:
            cursor.execute(insert_sql, tuple(row))
            inserted_count += 1
        except sqlite3.IntegrityError:
            # This should not happen with INSERT OR REPLACE, but good for debugging
            print(f"Integrity Error for issue {row[0]}")
            pass
    
    conn.commit()
    conn.close()
    print(f"Successfully inserted/updated {inserted_count} records in {db_path}.")

# --- Markov Model Training Functions ---

def get_number_features(number, max_val):
    features = []
    if number % 2 == 0: features.append('even')
    else: features.append('odd')
    if number <= max_val / 2: features.append('small')
    else: features.append('large')
    return frozenset(features)

def train_markov_model(df, red_cols, blue_cols, red_max, blue_max):
    red_model = defaultdict(lambda: defaultdict(int))
    blue_model = defaultdict(lambda: defaultdict(int))
    
    # Train Red Ball Model
    all_red_balls = []
    for index, row in df.iterrows():
        balls = sorted([row[col] for col in red_cols])
        all_red_balls.extend(balls)

    # Use features of the sorted red balls as the state sequence
    red_features_sequence = [get_number_features(ball, red_max) for ball in all_red_balls]
    
    for i in range(len(red_features_sequence) - 1):
        current_state = str(red_features_sequence[i])
        next_state = str(red_features_sequence[i+1])
        red_model[current_state][next_state] += 1
        
    # Convert counts to probabilities
    final_red_model = {}
    for current_state, next_states in red_model.items():
        total_transitions = sum(next_states.values())
        final_red_model[current_state] = {
            next_state: count / total_transitions
            for next_state, count in next_states.items()
        }

    # Train Blue Ball Model
    all_blue_balls = []
    for index, row in df.iterrows():
        balls = sorted([row[col] for col in blue_cols])
        all_blue_balls.extend(balls)
        
    # Use features of the sorted blue balls as the state sequence
    blue_features_sequence = [get_number_features(ball, blue_max) for ball in all_blue_balls]
    
    for i in range(len(blue_features_sequence) - 1):
        current_state = str(blue_features_sequence[i])
        next_state = str(blue_features_sequence[i+1])
        blue_model[current_state][next_state] += 1
        
    # Convert counts to probabilities
    final_blue_model = {}
    for current_state, next_states in blue_model.items():
        total_transitions = sum(next_states.values())
        final_blue_model[current_state] = {
            next_state: count / total_transitions
            for next_state, count in next_states.items()
        }

    return {
        'red_balls': final_red_model,
        'blue_balls': final_blue_model
    }

def retrain_models():
    print("--- Retraining Markov Models ---")
    
    # --- DLT Model ---
    try:
        dlt_df = pd.read_csv(DLT_CSV)
        dlt_red_cols = ["red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5"]
        dlt_blue_cols = ["blue_ball_1", "blue_ball_2"]
        dlt_model = train_markov_model(dlt_df, dlt_red_cols, dlt_blue_cols, 35, 12)
        with open(DLT_MODEL_JSON, 'w', encoding='utf-8') as f:
            json.dump(dlt_model, f, ensure_ascii=False, indent=4)
        print(f"Successfully retrained and saved DLT model to {DLT_MODEL_JSON}.")
    except FileNotFoundError:
        print(f"Error: DLT CSV file not found at {DLT_CSV}. Skipping DLT model retraining.")
    
    # --- SSQ Model ---
    try:
        ssq_df = pd.read_csv(SSQ_CSV)
        ssq_red_cols = ["red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5", "red_ball_6"]
        ssq_blue_cols = ["blue_ball_1"]
        ssq_model = train_markov_model(ssq_df, ssq_red_cols, ssq_blue_cols, 33, 16)
        with open(SSQ_MODEL_JSON, 'w', encoding='utf-8') as f:
            json.dump(ssq_model, f, ensure_ascii=False, indent=4)
        print(f"Successfully retrained and saved SSQ model to {SSQ_MODEL_JSON}.")
    except FileNotFoundError:
        print(f"Error: SSQ CSV file not found at {SSQ_CSV}. Skipping SSQ model retraining.")


# --- Main Execution ---

if __name__ == '__main__':
    # Change directory to src so paths are correct
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Update Databases
    update_database(DLT_CSV, DLT_DB, create_dlt_table, 'dlt')
    update_database(SSQ_CSV, SSQ_DB, create_ssq_table, 'ssq')
    
    # 2. Retrain Models
    retrain_models()

    print("Database and Model Update Process Complete.")
