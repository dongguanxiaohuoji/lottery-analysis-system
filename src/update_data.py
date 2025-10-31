import requests
from bs4 import BeautifulSoup
import sqlite3
import re

DATABASE_DLT = 'dlt_results.db'
DATABASE_SSQ = 'ssq_results.db'

def scrape_zhcw_dlt():
    url = 'https://www.zhcw.com/kjxx/dlt/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    draws = []
    # Find the table containing the lottery results
    table = soup.find('table')
    if not table:
        print("大乐透：未找到开奖结果表格")
        return []

    rows = table.find_all('tr')[2:12] # Skip header rows, get latest 10
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 12:
            try:
                issue_number = cols[0].text.strip()
                draw_date = cols[1].text.strip().split('（')[0] # Remove day of week
                
                red_balls_str = cols[2].text.strip()
                blue_balls_str = cols[3].text.strip()
                
                red_balls = [int(rb) for rb in re.findall(r'\d{2}', red_balls_str)]
                blue_balls = [int(bb) for bb in re.findall(r'\d{2}', blue_balls_str)]

                sales_amount_str = cols[4].text.strip().replace(',', '')
                sales_amount = int(float(sales_amount_str)) if sales_amount_str else 0

                jackpot_amount_str = cols[11].text.strip().replace(',', '')
                jackpot_amount = int(float(jackpot_amount_str)) if jackpot_amount_str else 0

                draws.append({
                    'issue_number': issue_number,
                    'draw_date': draw_date,
                    'red_balls': red_balls,
                    'blue_balls': blue_balls,
                    'sales_amount': sales_amount,
                    'jackpot_amount': jackpot_amount
                })
            except Exception as e:
                print(f"大乐透：解析行数据时出错: {row.text.strip()} - {e}")
    return draws

def scrape_zhcw_ssq():
    url = 'https://www.zhcw.com/kjxx/ssq/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    draws = []
    table = soup.find('table')
    if not table:
        print("双色球：未找到开奖结果表格")
        return []

    rows = table.find_all('tr')[2:12] # Skip header rows, get latest 10
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 10:
            try:
                issue_number = cols[0].text.strip()
                draw_date = cols[1].text.strip().split('（')[0] # Remove day of week
                
                red_balls_str = cols[2].text.strip()
                blue_ball_str = cols[3].text.strip()
                
                red_balls = [int(rb) for rb in re.findall(r'\d{2}', red_balls_str)]
                blue_ball = [int(bb) for bb in re.findall(r'\d{2}', blue_ball_str)]

                sales_amount_str = cols[4].text.strip().replace(',', '')
                sales_amount = int(float(sales_amount_str)) if sales_amount_str else 0

                jackpot_amount_str = cols[9].text.strip().replace(',', '')
                jackpot_amount = int(float(jackpot_amount_str)) if jackpot_amount_str else 0

                draws.append({
                    'issue_number': issue_number,
                    'draw_date': draw_date,
                    'red_balls': red_balls,
                    'blue_balls': blue_ball,
                    'sales_amount': sales_amount,
                    'jackpot_amount': jackpot_amount
                })
            except Exception as e:
                print(f"双色球：解析行数据时出错: {row.text.strip()} - {e}")
    return draws

def update_dlt_database(draws):
    conn = sqlite3.connect(DATABASE_DLT)
    cursor = conn.cursor()
    for draw in draws:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO draw_results (
                    issue_number, draw_date,
                    red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5,
                    blue_ball_1, blue_ball_2, sales_amount, jackpot_amount
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                draw['issue_number'], draw['draw_date'],
                draw['red_balls'][0], draw['red_balls'][1], draw['red_balls'][2], draw['red_balls'][3], draw['red_balls'][4],
                draw['blue_balls'][0], draw['blue_balls'][1], draw['sales_amount'], draw['jackpot_amount']
            ))
        except IndexError as e:
            print(f"大乐透：号码数量不匹配，跳过期号 {draw['issue_number']}: {e}")
        except sqlite3.Error as e:
            print(f"大乐透：数据库插入错误，期号 {draw['issue_number']}: {e}")
    conn.commit()
    conn.close()
    print(f"大乐透数据库更新完成，共插入/更新 {len(draws)} 条记录。")

def update_ssq_database(draws):
    conn = sqlite3.connect(DATABASE_SSQ)
    cursor = conn.cursor()
    for draw in draws:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO draw_results (
                    issue_number, draw_date,
                    red_ball_1, red_ball_2, red_ball_3, red_ball_4, red_ball_5, red_ball_6,
                    blue_ball_1, sales_amount, jackpot_amount
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                draw['issue_number'], draw['draw_date'],
                draw['red_balls'][0], draw['red_balls'][1], draw['red_balls'][2], draw['red_balls'][3], draw['red_balls'][4], draw['red_balls'][5],
                draw['blue_balls'][0], draw['sales_amount'], draw['jackpot_amount']
            ))
        except IndexError as e:
            print(f"双色球：号码数量不匹配，跳过期号 {draw['issue_number']}: {e}")
        except sqlite3.Error as e:
            print(f"双色球：数据库插入错误，期号 {draw['issue_number']}: {e}")
    conn.commit()
    conn.close()
    print(f"双色球数据库更新完成，共插入/更新 {len(draws)} 条记录。")

if __name__ == '__main__':
    print("开始更新大乐透数据...")
    dlt_latest_draws = scrape_zhcw_dlt()
    if dlt_latest_draws:
        update_dlt_database(dlt_latest_draws)
    else:
        print("未获取到大乐透最新开奖数据。")

    print("\n开始更新双色球数据...")
    ssq_latest_draws = scrape_zhcw_ssq()
    if ssq_latest_draws:
        update_ssq_database(ssq_latest_draws)
    else:
        print("未获取到双色球最新开奖数据。")

    print("\n数据更新任务完成。")
