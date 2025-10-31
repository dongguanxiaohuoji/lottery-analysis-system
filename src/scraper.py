import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

def scrape_dlt_data():
    print("开始抓取大乐透数据...")
    base_url = "http://datachart.500.com/dlt/history/newinc/history.php?start=07001&end="
    
    # Try to get the latest issue number from the main history page
    try:
        response = requests.get("http://datachart.500.com/dlt/history/history.shtml")
        response.encoding = "gb2312"
        soup = BeautifulSoup(response.text, "html.parser")
        latest_issue_element = soup.find("div", class_="chart_title").find("span").text
        latest_issue = re.search(r"\d+", latest_issue_element).group(0)
    except (AttributeError, IndexError, TypeError):
        print("无法从主历史页面获取最新大乐透期号，使用默认值。")
        latest_issue = "25140" # Fallback to a reasonable max issue

    full_url = base_url + latest_issue 
    print(f"访问大乐透数据URL: {full_url}")
    response = requests.get(full_url)
    response.encoding = "gb2312"
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("tbody", id="tdata")
    if not table:
        print("未找到大乐透数据表格，请检查网页结构或URL。")
        return

    data = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) > 10:  # Ensure it's a valid data row
            issue_number = cols[0].text.strip()
            draw_date = cols[12].text.strip() # 开奖日期在第13列 (索引12)
            red_balls = [int(c.text.strip()) for c in cols[1:6]] # 红球在第2-6列 (索引1-5)
            blue_balls = [int(c.text.strip()) for c in cols[6:8]] # 蓝球在第7-8列 (索引6-7)
            jackpot_amount = cols[8].text.strip().replace(",", "") # 奖池奖金在第9列 (索引8)
            sales_amount = cols[11].text.strip().replace(",", "") # 总投注额在第12列 (索引11)

            data.append([
                issue_number, draw_date, 
                *red_balls,
                *blue_balls,
                sales_amount, jackpot_amount
            ])
    
    df = pd.DataFrame(data, columns=[
        "issue_number", "draw_date", 
        "red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5",
        "blue_ball_1", "blue_ball_2",
        "sales_amount", "jackpot_amount"
    ])
    df.to_csv("/home/ubuntu/dlt_project/src/dlt_lottery_data.csv", index=False, encoding="utf-8")
    print(f"大乐透数据抓取完成，并保存到 dlt_lottery_data.csv 文件中。共抓取 {len(df)} 条数据。")

def scrape_ssq_data():
    print("开始抓取双色球数据...")
    base_url = "http://datachart.500.com/ssq/history/newinc/history.php?start=03001&end="
    
    # Try to get the latest issue number from the main history page
    try:
        response = requests.get("http://datachart.500.com/ssq/history/history.shtml")
        response.encoding = "gb2312"
        soup = BeautifulSoup(response.text, "html.parser")
        latest_issue_element = soup.find("div", class_="chart_title").find("span").text
        latest_issue = re.search(r"\d+", latest_issue_element).group(0)
    except (AttributeError, IndexError, TypeError):
        print("无法从主历史页面获取最新双色球期号，使用默认值。")
        latest_issue = "25140" # Fallback to a reasonable max issue

    full_url = base_url + latest_issue 
    print(f"访问双色球数据URL: {full_url}")
    response = requests.get(full_url)
    response.encoding = "gb2312"
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("tbody", id="tdata")
    if not table:
        print("未找到双色球数据表格，请检查网页结构或URL。")
        return

    data = []
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) > 10:  # Ensure it's a valid data row
            issue_number = cols[0].text.strip()
            draw_date = cols[12].text.strip() # 开奖日期在第13列 (索引12)
            red_balls = [int(c.text.strip()) for c in cols[1:7]] # 红球在第2-7列 (索引1-6)
            blue_ball = int(cols[7].text.strip()) # 蓝球在第8列 (索引7)
            jackpot_amount = cols[8].text.strip().replace(",", "") # 奖池奖金在第9列 (索引8)
            sales_amount = cols[11].text.strip().replace(",", "") # 总投注额在第12列 (索引11)

            data.append([
                issue_number, draw_date, 
                *red_balls,
                blue_ball,
                sales_amount, jackpot_amount
            ])
    
    df = pd.DataFrame(data, columns=[
        "issue_number", "draw_date", 
        "red_ball_1", "red_ball_2", "red_ball_3", "red_ball_4", "red_ball_5", "red_ball_6",
        "blue_ball_1",
        "sales_amount", "jackpot_amount"
    ])
    df.to_csv("/home/ubuntu/dlt_project/src/ssq_lottery_data.csv", index=False, encoding="utf-8")
    print(f"双色球数据抓取完成，并保存到 ssq_lottery_data.csv 文件中。共抓取 {len(df)} 条数据。")

if __name__ == "__main__":
    scrape_dlt_data()
    scrape_ssq_data()

