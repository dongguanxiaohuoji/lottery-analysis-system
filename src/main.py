from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import random
from collections import defaultdict

# Import the number generation logic
from generate_numbers import generate_dlt_numbers_with_features as generate_dlt_numbers, generate_ssq_numbers_with_features as generate_ssq_numbers

app = Flask(__name__)

DATABASE_DLT = 'dlt_results.db'
DATABASE_SSQ = 'ssq_results.db'

def load_markov_model(lottery_type):
    try:
        if lottery_type == 'dlt':
            return json.load(open('dlt_markov_model_features.json', 'r', encoding='utf-8'))
        elif lottery_type == 'ssq':
            return json.load(open('ssq_markov_model_features.json', 'r', encoding='utf-8'))
    except FileNotFoundError:
        print(f"Error: Markov model file for {lottery_type} not found.")
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_dlt', methods=['GET'])
def generate_dlt():
    num_sets = int(request.args.get('num_sets', 1))
    dlt_model = load_markov_model('dlt')
    if not dlt_model:
        return jsonify({'error': '大乐透马尔可夫模型未加载'}), 500
    suggestions = generate_dlt_numbers(dlt_model, num_sets)
    return jsonify(suggestions)

@app.route('/generate_ssq', methods=['GET'])
def generate_ssq():
    num_sets = int(request.args.get('num_sets', 1))
    ssq_model = load_markov_model('ssq')
    if not ssq_model:
        return jsonify({'error': '双色球马尔可夫模型未加载'}), 500
    suggestions = generate_ssq_numbers(ssq_model, num_sets)
    return jsonify(suggestions)

@app.route('/query_dlt', methods=['GET'])
def query_dlt():
    issue_number = request.args.get('issue_number')
    conn = sqlite3.connect(DATABASE_DLT)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM draw_results WHERE issue_number = ?", (issue_number,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({
            'issue_number': result[0],
            'draw_date': result[1],
            'red_balls': [result[2], result[3], result[4], result[5], result[6]],
            'blue_balls': [result[7], result[8]],
            'sales_amount': result[9],
            'jackpot_amount': result[10]
        })
    return jsonify({'error': '未找到该期大乐透开奖数据'}), 404

@app.route('/query_ssq', methods=['GET'])
def query_ssq():
    issue_number = request.args.get('issue_number')
    conn = sqlite3.connect(DATABASE_SSQ)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM draw_results WHERE issue_number = ?", (issue_number,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({
            'issue_number': result[0],
            'draw_date': result[1],
            'red_balls': [result[2], result[3], result[4], result[5], result[6], result[7]],
            'blue_balls': [result[8]],
            'sales_amount': result[9],
            'jackpot_amount': result[10]
        })
    return jsonify({'error': '未找到该期双色球开奖数据'}), 404

@app.route('/latest_dlt_draws', methods=['GET'])
def latest_dlt_draws():
    conn = sqlite3.connect(DATABASE_DLT)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM draw_results ORDER BY issue_number DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    
    if results:
        latest_draws = []
        for result in results:
            latest_draws.append({
                'issue_number': result[0],
                'draw_date': result[1],
                'red_balls': [result[2], result[3], result[4], result[5], result[6]],
                'blue_balls': [result[7], result[8]],
                'sales_amount': result[9],
                'jackpot_amount': result[10]
            })
        return jsonify(latest_draws)
    return jsonify({'error': '未找到大乐透开奖数据'}), 404

@app.route('/latest_ssq_draws', methods=['GET'])
def latest_ssq_draws():
    conn = sqlite3.connect(DATABASE_SSQ)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM draw_results ORDER BY issue_number DESC LIMIT 10")
    results = cursor.fetchall()
    conn.close()
    
    if results:
        latest_draws = []
        for result in results:
            latest_draws.append({
                'issue_number': result[0],
                'draw_date': result[1],
                'red_balls': [result[2], result[3], result[4], result[5], result[6], result[7]],
                'blue_balls': [result[8]],
                'sales_amount': result[9],
                'jackpot_amount': result[10]
            })
        return jsonify(latest_draws)
    return jsonify({'error': '未找到双色球开奖数据'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

