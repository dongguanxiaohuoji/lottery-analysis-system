import sqlite3
import json
from collections import defaultdict

DATABASE_DLT = 'dlt_results.db'
DATABASE_SSQ = 'ssq_results.db'

def get_dlt_draws():
    conn = sqlite3.connect(DATABASE_DLT)
    cursor = conn.cursor()
    cursor.execute("SELECT red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5, blue_ball_1, blue_ball_2 FROM draw_results ORDER BY issue_number ASC")
    draws = cursor.fetchall()
    conn.close()
    return draws

def get_ssq_draws():
    conn = sqlite3.connect(DATABASE_SSQ)
    cursor = conn.cursor()
    cursor.execute("SELECT red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5, red_ball_6, blue_ball_1 FROM draw_results ORDER BY issue_number ASC")
    draws = cursor.fetchall()
    conn.close()
    return draws

def get_number_features(number, max_val):
    features = []
    if number % 2 == 0: features.append('even')
    else: features.append('odd')
    if number <= max_val / 2: features.append('small')
    else: features.append('large')
    return frozenset(features)

def build_markov_model_with_features(draws, num_red_balls, num_blue_balls, red_max, blue_max):
    red_feature_transitions = defaultdict(lambda: defaultdict(int))
    blue_feature_transitions = defaultdict(lambda: defaultdict(int))

    for i in range(len(draws) - 1):
        current_red_balls = sorted(draws[i][0:num_red_balls])
        next_red_balls = sorted(draws[i+1][0:num_red_balls])
        current_blue_balls = sorted(draws[i][num_red_balls:num_red_balls+num_blue_balls])
        next_blue_balls = sorted(draws[i+1][num_red_balls:num_red_balls+num_blue_balls])

        # Red ball feature transitions
        for rb_curr in current_red_balls:
            curr_features = get_number_features(rb_curr, red_max)
            for rb_next in next_red_balls:
                next_features = get_number_features(rb_next, red_max)
                red_feature_transitions[str(curr_features)][str(next_features)] += 1

        # Blue ball feature transitions
        for bb_curr in current_blue_balls:
            curr_features = get_number_features(bb_curr, blue_max)
            for bb_next in next_blue_balls:
                next_features = get_number_features(bb_next, blue_max)
                blue_feature_transitions[str(curr_features)][str(next_features)] += 1

    # Convert counts to probabilities
    red_prob_matrix = {}
    for current_features, next_feature_counts in red_feature_transitions.items():
        total_transitions = sum(next_feature_counts.values())
        if total_transitions > 0:
            red_prob_matrix[current_features] = {next_features: count / total_transitions for next_features, count in next_feature_counts.items()}

    blue_prob_matrix = {}
    for current_features, next_feature_counts in blue_feature_transitions.items():
        total_transitions = sum(next_feature_counts.values())
        if total_transitions > 0:
            blue_prob_matrix[current_features] = {next_features: count / total_transitions for next_features, count in next_feature_counts.items()}

    return red_prob_matrix, blue_prob_matrix

def save_model(model, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(model, f, ensure_ascii=False, indent=4)
    print(f"马尔可夫链模型已保存到 {filename}")

if __name__ == '__main__':
    # 大乐透模型 (基于特征)
    dlt_draws = get_dlt_draws()
    dlt_red_model_features, dlt_blue_model_features = build_markov_model_with_features(dlt_draws, 5, 2, 35, 12)
    save_model({'red_balls': dlt_red_model_features, 'blue_balls': dlt_blue_model_features}, 'dlt_markov_model_features.json')

    # 双色球模型 (基于特征)
    ssq_draws = get_ssq_draws()
    ssq_red_model_features, ssq_blue_model_features = build_markov_model_with_features(ssq_draws, 6, 1, 33, 16)
    save_model({'red_balls': ssq_red_model_features, 'blue_balls': ssq_blue_model_features}, 'ssq_markov_model_features.json')

    print("大乐透和双色球马尔可夫链模型（基于特征）构建完成。")

