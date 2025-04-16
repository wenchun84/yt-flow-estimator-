import streamlit as st
import gspread
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

# 設定 scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 將 st.secrets 轉換為 JSON dict
creds_dict = st.secrets["google_sheets"]
creds_json = json.dumps(creds_dict)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(creds_json), scope)

# 授權並打開 Sheet
gc = gspread.authorize(credentials)

# ✅ 請替換為你的 Google Sheet 網址或 ID
sheet_url = "https://docs.google.com/spreadsheets/d/你的_Sheet_ID/"

# 開啟並讀取資料
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示
st.title("📊 Google Sheets 資料表")
st.dataframe(df)
