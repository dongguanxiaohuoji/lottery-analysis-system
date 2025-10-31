import sqlite3
import csv

DATABASE_NAME = 'dlt_results.db'
CSV_FILE_PATH = 'dlt_lottery_data.csv'

def insert_data_from_csv():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO draw_results (
                        issue_number, draw_date, 
                        red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5,
                        blue_ball_1, blue_ball_2, 
                        sales_amount, jackpot_amount
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['issue_number'], row['draw_date'],
                    int(row['red_ball_1']), int(row['red_ball_2']), int(row['red_ball_3']), int(row['red_ball_4']), int(row['red_ball_5']),
                    int(row['blue_ball_1']), int(row['blue_ball_2']),
                    int(row['sales_amount']), int(row['jackpot_amount'])
                ))
            except ValueError as e:
                print(f"Skipping row due to data conversion error: {row} - {e}")
            except sqlite3.Error as e:
                print(f"Skipping row due to database error: {row} - {e}")

    conn.commit()
    conn.close()
    print("数据已从CSV文件导入到数据库。")

if __name__ == '__main__':
    insert_data_from_csv()
