import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_NAME = os.path.join(BASE_DIR, 'ssq_results.db')
DATA_FILE_PATH = os.path.join(BASE_DIR, 'ssq_lottery_data.csv')

def insert_ssq_data():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        df = pd.read_csv(DATA_FILE_PATH)
    except FileNotFoundError:
        print(f"错误: 未找到数据文件 {DATA_FILE_PATH}。请先运行 scraper.py。")
        return

    for index, row in df.iterrows():
        try:
            issue_number = str(row['issue_number'])
            draw_date = str(row['draw_date'])
            red_balls = [row[f'red_ball_{i}'] for i in range(1, 7)]
            blue_ball = row['blue_ball_1']
            sales_amount = str(row['sales_amount']).replace(',', '')
            jackpot_amount = str(row['jackpot_amount']).replace(',', '')

            cursor.execute("""
                INSERT OR REPLACE INTO draw_results (
                    issue_number, draw_date,
                    red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5, red_ball_6,
                    blue_ball_1, sales_amount, jackpot_amount
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                issue_number, draw_date,
                red_balls[0], red_balls[1], red_balls[2], red_balls[3], red_balls[4], red_balls[5],
                blue_ball, sales_amount, jackpot_amount
            ))
        except Exception as e:
            print(f"Skipping row {index} due to error: {e}")
            print(f"Row data: {row.to_dict()}")

    conn.commit()
    conn.close()
    print("双色球数据已从CSV文件导入到数据库。")

if __name__ == '__main__':
    insert_ssq_data()

