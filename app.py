import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# 設定 scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# 讀取並轉為 dict
creds_dict = dict(st.secrets["google_sheets"])
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# 授權
gc = gspread.authorize(credentials)

# 指定 Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1dYgABCDE1234567890EfGhIJKLmnopQRstuVWxyz/edit#gid=0"
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# 顯示
st.title("📊 Google Sheets 資料表")
st.dataframe(df)
