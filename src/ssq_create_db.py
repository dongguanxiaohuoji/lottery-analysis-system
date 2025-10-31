import sqlite3

DATABASE_NAME = 'ssq_results.db'

def create_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # 删除旧表（如果存在）
    cursor.execute('DROP TABLE IF EXISTS draw_results;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS draw_results (
            issue_number TEXT PRIMARY KEY,
            draw_date TEXT NOT NULL,
            red_ball_1 INTEGER NOT NULL,
            red_ball_2 INTEGER NOT NULL,
            red_ball_3 INTEGER NOT NULL,
            red_ball_4 INTEGER NOT NULL,
            red_ball_5 INTEGER NOT NULL,
            red_ball_6 INTEGER NOT NULL,
            blue_ball_1 INTEGER NOT NULL,
            sales_amount INTEGER,
            jackpot_amount INTEGER
        );
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("双色球数据库和表已创建或更新成功。")
