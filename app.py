import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 設定 scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 取得 secrets 並轉為一般 dict
import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 設定 scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# 取得 secrets 並轉為一般 dict
creds_dict = dict(st.secrets["google_sheets"])

# 授權並開啟 Google Sheet
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
gc = gspread.authorize(credentials)

# ✅ 替換成你自己的 Google Sheet 網址或 ID
sheet_url = "https://docs.google.com/spreadsheets/d/你的_Sheet_ID/"

# 開啟並讀取資料
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示資料
st.title("📊 Google Sheets 資料表")
st.dataframe(df)


# ✅ 替換成你自己的 Google Sheet 網址或 ID
sheet_url = "https://docs.google.com/spreadsheets/d/你的_Sheet_ID/"

# 開啟並讀取資料
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示資料
st.title("📊 Google Sheets 資料表")
st.dataframe(df)
