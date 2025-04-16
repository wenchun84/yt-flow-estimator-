import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# ====== 設定 API 金鑰與 Sheets 憑證 ======
YOUTUBE_API_KEY = "AIzaSyB-vJVbuZAu7-4pHUqt8JaGdhfKle8m4cI"

# Google Sheet 連結與名稱
SHEET_NAME = "YouTube流量紀錄"
SHEET_URL = "https://docs.google.com/spreadsheets/d/12U90TfY6uJyrqfaCjYs0zW8uMYgdaDomzzJYlpfV-bE"

# ====== 載入 Google Sheets 憑證 ======
# 將金鑰 json 放到本地或 Render，並透過環境變數指向
creds_dict = json.loads(st.secrets["google_sheets"])
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url(SHEET_URL).sheet1

# ====== YouTube 分析功能 ======
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

st.title("📺 YouTube 影片流量分析器")

video_url = st.text_input("請輸入 YouTube 影片連結")

def get_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return None

if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        res = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        if res["items"]:
            video = res["items"][0]
