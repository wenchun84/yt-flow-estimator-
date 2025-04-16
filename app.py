import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# 掛載認證
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)

# 打開 Google Sheet（請換成你自己的 Sheet URL 或名稱）
SPREADSHEET_NAME = "你的試算表名稱"
sheet = client.open(SPREADSHEET_NAME).sheet1
data = sheet.get_all_records()

# 顯示資料
df = pd.DataFrame(data)
st.title("📊 Google Sheets 資料預覽")
st.dataframe(df)
