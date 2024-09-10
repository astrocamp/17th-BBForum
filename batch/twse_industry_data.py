import os
import time
from datetime import datetime

import pandas as pd
import requests
import schedule
from bs4 import BeautifulSoup
from sqlalchemy import create_engine

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def fetch_and_store_data():
    engine = create_engine(
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    urls = [
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=4",
        "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    session = requests.Session()
    session.headers.update(headers)

    all_data = []

    for url in urls:
        print(f"Processing URL: {url}")
        try:
            response = session.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", {"class": "h4"})

            if table:
                rows = []
                for tr in table.find_all("tr"):
                    cells = [td.text.strip() for td in tr.find_all("td")]
                    if cells:
                        rows.append(cells)

                if len(rows) > 1:
                    headers = rows[0]
                    data_rows = rows[1:]
                    df = pd.DataFrame(data_rows, columns=headers)
                    all_data.append(df)
                else:
                    print(f"表格數據不足於 URL: {url}")
            else:
                print(f"未能找到產業別資料表格於 URL: {url}")
        except requests.RequestException as e:
            print(f"請求失敗，錯誤信息：{e}")

    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        print("Data combined successfully.")

        filtered_df = combined_df[combined_df["CFICode"] == "ESVUFR"]

        if not filtered_df.empty:
            selected_columns = ["有價證券代號及名稱", "產業別"]
            if all(col in filtered_df.columns for col in selected_columns):
                df_selected = filtered_df[selected_columns]

                df_selected[["security_code", "name"]] = df_selected[
                    "有價證券代號及名稱"
                ].str.extract(r"(\S+)\s*(.*)", expand=True)

                df_selected = df_selected.drop(columns=["有價證券代號及名稱"])
                df_selected = df_selected.rename(columns={"產業別": "industry"})
                df_selected = df_selected[["security_code", "name", "industry"]]

                df_selected = df_selected.drop_duplicates(
                    subset="security_code", keep="first"
                )

                table_name = "twse_industry_data"
                df_selected.to_sql(
                    table_name, engine, if_exists="append", index=False, method="multi"
                )
                print(f"選定的產業別資料已保存到 PostgreSQL 表 '{table_name}'")
            else:
                print("選定的列標題不在 DataFrame 中。")
        else:
            print("未找到 CFICode 為 ESVUFR 的數據。")
    else:
        print("未獲取任何有效數據。")


fetch_and_store_data()

# 以下code為定期跑，暫時先註解

# def job():
#     print("Starting scheduled job...")
#     fetch_and_store_data()
#     print("Job finished.")


# def check_monthly_job():
#     now = datetime.now()
#     # 檢查是否是每月的第一天
#     if now.day == 1:
#         job()


# schedule.every().day.at("00:00").do(check_monthly_job)

# print("Scheduler started...")

# while True:
#     schedule.run_pending()
#     time.sleep(60)
