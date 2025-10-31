import json
import sqlite3
from collections import defaultdict
import random

DATABASE_DLT = 'dlt_results.db'
DATABASE_SSQ = 'ssq_results.db'

def load_model(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_draws(db_name, num_red_balls, num_blue_balls):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    if db_name == DATABASE_DLT:
        cursor.execute("SELECT red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5, blue_ball_1, blue_ball_2 FROM draw_results ORDER BY issue_number ASC")
    elif db_name == DATABASE_SSQ:
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

def evaluate_markov_model_with_features(model, draws, num_red_balls, num_blue_balls, red_max, blue_max):
    red_model = model['red_balls']
    blue_model = model['blue_balls']

    red_feature_prediction_accuracy = defaultdict(int)
    blue_feature_prediction_accuracy = defaultdict(int)
    total_red_feature_predictions = 0
    total_blue_feature_predictions = 0

    for i in range(len(draws) - 1):
        current_red_balls = sorted(draws[i][0:num_red_balls])
        next_red_balls = sorted(draws[i+1][0:num_red_balls])
        current_blue_balls = sorted(draws[i][num_red_balls:num_red_balls+num_blue_balls])
        next_blue_balls = sorted(draws[i+1][num_red_balls:num_red_balls+num_blue_balls])

        # Evaluate red ball feature predictions
        for current_rb in current_red_balls:
            current_features = str(get_number_features(current_rb, red_max))
            if current_features in red_model:
                total_red_feature_predictions += 1
                most_probable_next_features = None
                max_prob = -1
                for next_features_str, prob in red_model[current_features].items():
                    if prob > max_prob:
                        max_prob = prob
                        most_probable_next_features = next_features_str
                
                # Check if any of the next red balls match the predicted features
                matched = False
                for next_rb in next_red_balls:
                    if str(get_number_features(next_rb, red_max)) == most_probable_next_features:
                        matched = True
                        break
                if matched:
                    red_feature_prediction_accuracy['hit'] += 1
                else:
                    red_feature_prediction_accuracy['miss'] += 1

        # Evaluate blue ball feature predictions
        for current_bb in current_blue_balls:
            current_features = str(get_number_features(current_bb, blue_max))
            if current_features in blue_model:
                total_blue_feature_predictions += 1
                most_probable_next_features = None
                max_prob = -1
                for next_features_str, prob in blue_model[current_features].items():
                    if prob > max_prob:
                        max_prob = prob
                        most_probable_next_features = next_features_str
                
                # Check if any of the next blue balls match the predicted features
                matched = False
                for next_bb in next_blue_balls:
                    if str(get_number_features(next_bb, blue_max)) == most_probable_next_features:
                        matched = True
                        break
                if matched:
                    blue_feature_prediction_accuracy['hit'] += 1
                else:
                    blue_feature_prediction_accuracy['miss'] += 1

    return red_feature_prediction_accuracy, blue_feature_prediction_accuracy

if __name__ == '__main__':
    print("\n--- 大乐透模型（基于特征）评估 ---")
    dlt_model_features = load_model('dlt_markov_model_features.json')
    dlt_draws = get_draws(DATABASE_DLT, 5, 2)
    dlt_red_accuracy_features, dlt_blue_accuracy_features = evaluate_markov_model_with_features(dlt_model_features, dlt_draws, 5, 2, 35, 12)
    print(f"大乐透红球特征预测: {dlt_red_accuracy_features}")
    print(f"大乐透蓝球特征预测: {dlt_blue_accuracy_features}")

    print("\n--- 双色球模型（基于特征）评估 ---")
    ssq_model_features = load_model('ssq_markov_model_features.json')
    ssq_draws = get_draws(DATABASE_SSQ, 6, 1)
    ssq_red_accuracy_features, ssq_blue_accuracy_features = evaluate_markov_model_with_features(ssq_model_features, ssq_draws, 6, 1, 33, 16)
    print(f"双色球红球特征预测: {ssq_red_accuracy_features}")
    print(f"双色球蓝球特征预测: {ssq_blue_accuracy_features}")

