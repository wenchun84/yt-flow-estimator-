import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 設定 Google Sheets 權限 scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 從 secrets.toml 載入金鑰
creds_dict = dict(st.secrets["google_sheets"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# 授權並打開 Sheet
gc = gspread.authorize(credentials)

# ✅ 使用 Sheet ID 開啟
sheet_id = "1ABCdEfGhiJkLmNopQRstuvWxyZ0123456789abcdEFg"  # << 替換成你的
sh = gc.open_by_key(sheet_id)

# 開啟指定工作表
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示內容
st.title("📊 Google Sheets 資料表")
st.dataframe(df)
