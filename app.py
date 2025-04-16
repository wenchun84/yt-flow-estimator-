import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 設定 Google Sheets API scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 將 st.secrets 轉為 dict（避免 AttrDict 問題）
creds_dict = dict(st.secrets["google_sheets"])

# 授權 Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(credentials)

# 讀取你的 Google Sheets 網址或 ID
sheet_url = "https://docs.google.com/spreadsheets/d/你的_Sheet_ID/"  # 👈請換成你的網址

# 抓取資料並轉為 DataFrame
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示結果
st.title("📊 Google Sheets 資料表")
st.dataframe(df)
