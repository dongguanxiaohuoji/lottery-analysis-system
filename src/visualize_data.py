import json
import matplotlib.pyplot as plt
import matplotlib

# 设置matplotlib支持中文显示
matplotlib.rcParams["font.sans-serif"] = ["Noto Sans CJK SC"]
matplotlib.rcParams["axes.unicode_minus"] = False


JSON_FILE_PATH = 'dlt_analysis_most_frequent_results.json'

def visualize_frequencies():
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    red_balls = data['red_ball_frequencies_most_frequent']
    blue_balls = data['blue_ball_frequencies_most_frequent']

    # 绘制红球频率图
    plt.figure(figsize=(12, 6))
    red_numbers = [str(item[0]) for item in red_balls]
    red_counts = [item[1] for item in red_balls]
    plt.bar(red_numbers, red_counts, color='red')
    plt.xlabel('红球号码')
    plt.ylabel('出现次数')
    plt.title('大乐透红球出现频率（从多到少）')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('red_ball_frequencies_most_frequent.png')
    plt.close()

    # 绘制蓝球频率图
    plt.figure(figsize=(8, 6))
    blue_numbers = [str(item[0]) for item in blue_balls]
    blue_counts = [item[1] for item in blue_balls]
    plt.bar(blue_numbers, blue_counts, color='blue')
    plt.xlabel('蓝球号码')
    plt.ylabel('出现次数')
    plt.title('大乐透蓝球出现频率（从多到少）')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('blue_ball_frequencies_most_frequent.png')
    plt.close()

    print("红球和蓝球频率图已生成并保存。")

if __name__ == '__main__':
    visualize_frequencies()
