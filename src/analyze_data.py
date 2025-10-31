import sqlite3
import json

DATABASE_NAME = 'dlt_results.db'

def analyze_ball_frequencies():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    red_ball_counts = {}
    blue_ball_counts = {}

    # 统计红球频率
    for i in range(1, 6):
        cursor.execute(f'SELECT red_ball_{i} FROM draw_results;')
        results = cursor.fetchall()
        for row in results:
            ball = row[0]
            red_ball_counts[ball] = red_ball_counts.get(ball, 0) + 1

    # 统计蓝球频率
    for i in range(1, 3):
        cursor.execute(f'SELECT blue_ball_{i} FROM draw_results;')
        results = cursor.fetchall()
        for row in results:
            ball = row[0]
            blue_ball_counts[ball] = blue_ball_counts.get(ball, 0) + 1

    conn.close()

    # 按频率降序排序（出现次数最多到最少）
    sorted_red_balls = sorted(red_ball_counts.items(), key=lambda item: item[1], reverse=True)
    sorted_blue_balls = sorted(blue_ball_counts.items(), key=lambda item: item[1], reverse=True)

    return sorted_red_balls, sorted_blue_balls

def save_analysis_results(red_balls, blue_balls):
    results = {
        'red_ball_frequencies_most_frequent': red_balls,
        'blue_ball_frequencies_most_frequent': blue_balls
    }
    with open('dlt_analysis_most_frequent_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("分析结果（出现次数最多）已保存到 dlt_analysis_most_frequent_results.json")

if __name__ == '__main__':
    red_freq, blue_freq = analyze_ball_frequencies()
    save_analysis_results(red_freq, blue_freq)
    print("大乐透号码频率统计（出现次数最多）完成。")
