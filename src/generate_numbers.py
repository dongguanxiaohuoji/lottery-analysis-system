import json
import random
from collections import defaultdict

def load_model(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_number_features(number, max_val):
    features = []
    if number % 2 == 0: features.append('even')
    else: features.append('odd')
    if number <= max_val / 2: features.append('small')
    else: features.append('large')
    return frozenset(features)

def get_numbers_matching_features(target_features_str, min_val, max_val, exclude_numbers):
    matching_numbers = []
    target_features = eval(target_features_str) # Convert frozenset string back to frozenset
    for num in range(min_val, max_val + 1):
        if num in exclude_numbers: # Skip already selected numbers
            continue
        if get_number_features(num, max_val) == target_features:
            matching_numbers.append(num)
    return matching_numbers

def generate_dlt_numbers_with_features(model, num_sets=1):
    red_model = model['red_balls']
    blue_model = model['blue_balls']
    red_max = 35
    blue_max = 12

    suggested_sets = []
    for _ in range(num_sets):
        red_selection = []
        blue_selection = []

        # Generate red balls based on features
        current_red_features_str = random.choice(list(red_model.keys()))
        for _ in range(5):
            if current_red_features_str in red_model and red_model[current_red_features_str]:
                possible_next_features = list(red_model[current_red_features_str].keys())
                probabilities = list(red_model[current_red_features_str].values())
                predicted_next_features_str = random.choices(possible_next_features, weights=probabilities, k=1)[0]
            else:
                # Fallback to random features if no transitions
                predicted_next_features_str = str(random.choice([frozenset({'even', 'small'}), frozenset({'even', 'large'}), frozenset({'odd', 'small'}), frozenset({'odd', 'large'})]))
            
            matching_numbers = get_numbers_matching_features(predicted_next_features_str, 1, red_max, red_selection)
            if matching_numbers:
                selected_number = random.choice(matching_numbers)
                red_selection.append(selected_number)
                current_red_features_str = str(get_number_features(selected_number, red_max))
            else:
                # Fallback to random number if no matching number for features
                new_ball = random.randint(1, red_max)
                while new_ball in red_selection:
                    new_ball = random.randint(1, red_max)
                red_selection.append(new_ball)
                current_red_features_str = str(get_number_features(new_ball, red_max))

        red_selection = sorted(list(set(red_selection)))
        while len(red_selection) < 5:
            new_ball = random.randint(1, red_max)
            if new_ball not in red_selection:
                red_selection.append(new_ball)
                red_selection.sort()

        # Generate blue balls based on features
        current_blue_features_str = random.choice(list(blue_model.keys()))
        for _ in range(2):
            if current_blue_features_str in blue_model and blue_model[current_blue_features_str]:
                possible_next_features = list(blue_model[current_blue_features_str].keys())
                probabilities = list(blue_model[current_blue_features_str].values())
                predicted_next_features_str = random.choices(possible_next_features, weights=probabilities, k=1)[0]
            else:
                predicted_next_features_str = str(random.choice([frozenset({'even', 'small'}), frozenset({'even', 'large'}), frozenset({'odd', 'small'}), frozenset({'odd', 'large'})]))
            
            matching_numbers = get_numbers_matching_features(predicted_next_features_str, 1, blue_max, blue_selection)
            if matching_numbers:
                selected_number = random.choice(matching_numbers)
                blue_selection.append(selected_number)
                current_blue_features_str = str(get_number_features(selected_number, blue_max))
            else:
                new_ball = random.randint(1, blue_max)
                while new_ball in blue_selection:
                    new_ball = random.randint(1, blue_max)
                blue_selection.append(new_ball)
                current_blue_features_str = str(get_number_features(new_ball, blue_max))

        blue_selection = sorted(list(set(blue_selection)))
        while len(blue_selection) < 2:
            new_ball = random.randint(1, blue_max)
            if new_ball not in blue_selection:
                blue_selection.append(new_ball)
                blue_selection.sort()

        suggested_sets.append({
            'red_balls': red_selection,
            'blue_balls': blue_selection
        })
    return suggested_sets

def generate_ssq_numbers_with_features(model, num_sets=1):
    red_model = model['red_balls']
    blue_model = model['blue_balls']
    red_max = 33
    blue_max = 16

    suggested_sets = []
    for _ in range(num_sets):
        red_selection = []
        blue_selection = []

        # Generate red balls based on features
        current_red_features_str = random.choice(list(red_model.keys()))
        for _ in range(6):
            if current_red_features_str in red_model and red_model[current_red_features_str]:
                possible_next_features = list(red_model[current_red_features_str].keys())
                probabilities = list(red_model[current_red_features_str].values())
                predicted_next_features_str = random.choices(possible_next_features, weights=probabilities, k=1)[0]
            else:
                predicted_next_features_str = str(random.choice([frozenset({'even', 'small'}), frozenset({'even', 'large'}), frozenset({'odd', 'small'}), frozenset({'odd', 'large'})]))
            
            matching_numbers = get_numbers_matching_features(predicted_next_features_str, 1, red_max, red_selection)
            if matching_numbers:
                selected_number = random.choice(matching_numbers)
                red_selection.append(selected_number)
                current_red_features_str = str(get_number_features(selected_number, red_max))
            else:
                new_ball = random.randint(1, red_max)
                while new_ball in red_selection:
                    new_ball = random.randint(1, red_max)
                red_selection.append(new_ball)
                current_red_features_str = str(get_number_features(new_ball, red_max))

        red_selection = sorted(list(set(red_selection)))
        while len(red_selection) < 6:
            new_ball = random.randint(1, red_max)
            if new_ball not in red_selection:
                red_selection.append(new_ball)
                red_selection.sort()

        # Generate blue ball based on features
        current_blue_features_str = random.choice(list(blue_model.keys()))
        for _ in range(1):
            if current_blue_features_str in blue_model and blue_model[current_blue_features_str]:
                possible_next_features = list(blue_model[current_blue_features_str].keys())
                probabilities = list(blue_model[current_blue_features_str].values())
                predicted_next_features_str = random.choices(possible_next_features, weights=probabilities, k=1)[0]
            else:
                predicted_next_features_str = str(random.choice([frozenset({'even', 'small'}), frozenset({'even', 'large'}), frozenset({'odd', 'small'}), frozenset({'odd', 'large'})]))
            
            matching_numbers = get_numbers_matching_features(predicted_next_features_str, 1, blue_max, blue_selection)
            if matching_numbers:
                selected_number = random.choice(matching_numbers)
                blue_selection.append(selected_number)
                current_blue_features_str = str(get_number_features(selected_number, blue_max))
            else:
                new_ball = random.randint(1, blue_max)
                while new_ball in blue_selection:
                    new_ball = random.randint(1, blue_max)
                blue_selection.append(new_ball)
                current_blue_features_str = str(get_number_features(new_ball, blue_max))

        blue_selection = sorted(list(set(blue_selection)))
        while len(blue_selection) < 1:
            new_ball = random.randint(1, blue_max)
            if new_ball not in blue_selection:
                blue_selection.append(new_ball)
                blue_selection.sort()

        suggested_sets.append({
            'red_balls': red_selection,
            'blue_balls': blue_selection
        })
    return suggested_sets

if __name__ == '__main__':
    dlt_model = load_model('dlt_markov_model_features.json')
    ssq_model = load_model('ssq_markov_model_features.json')

    print("生成大乐透推荐号码（基于特征）：")
    dlt_suggestions = generate_dlt_numbers_with_features(dlt_model, num_sets=5)
    for i, s in enumerate(dlt_suggestions):
        print(f"方案 {i+1}: 红球 {s['red_balls']}, 蓝球 {s['blue_balls']}")

    print("\n生成双色球推荐号码（基于特征）：")
    ssq_suggestions = generate_ssq_numbers_with_features(ssq_model, num_sets=5)
    for i, s in enumerate(ssq_suggestions):
        print(f"方案 {i+1}: 红球 {s['red_balls']}, 蓝球 {s['blue_balls']}")
