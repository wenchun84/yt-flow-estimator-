# app.py
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from analytics import estimate_traffic
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import matplotlib.pyplot as plt
from text_analysis import generate_analysis_text


# ✅ 初始化 YouTube API
api_key = st.secrets["youtube"]["api_key"]
youtube = build("youtube", "v3", developerKey=api_key)

# ✅ 初始化 Google Sheets API
gscope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["google_sheets"], gscope)
gc = gspread.authorize(creds)
sheet = gc.open_by_key(st.secrets["google_sheets"]["sheet_id"]).sheet1

# 🎯 影片ID解析函式
def extract_video_id(url):
    parsed = urlparse(url)
    if "youtu.be" in url:
        return parsed.path.lstrip('/')
    elif "youtube.com" in url:
        return parse_qs(parsed.query).get("v", [None])[0]
    return None

# 📡 呼叫 API 抓影片資訊
def fetch_video_data(video_id):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if not response["items"]:
        return None

    item = response["items"][0]
    snippet = item["snippet"]
    stats = item["statistics"]

    return {
        "videoId": video_id,
        "title": snippet.get("title"),
        "channelTitle": snippet.get("channelTitle"),
        "publishedAt": snippet.get("publishedAt"),
        "viewCount": int(stats.get("viewCount", 0)),
        "likeCount": int(stats.get("likeCount", 0)),
        "commentCount": int(stats.get("commentCount", 0))
    }

# 📈 畫成長曲線圖
def plot_growth(df):
    fig, ax = plt.subplots()
    ax.plot(df["分析時間"], df["觀看數"], marker='o', linestyle='-')
    ax.set_title("每日觀看數變化")
    ax.set_xlabel("分析時間")
    ax.set_ylabel("觀看數")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

# 🖥️ Streamlit 介面
st.title("📊 YouTube 流量預估檢測站")
video_url = st.text_input("請輸入 YouTube 影片連結：")

if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ 無法解析影片 ID，請確認連結格式。")
    else:
        video_data = fetch_video_data(video_id)
        if video_data:
            result = estimate_traffic(video_data)

            # 顯示在畫面上
            st.dataframe(pd.DataFrame([result]))
            st.markdown(generate_analysis_text(result))


            # ✅ 寫入 Google Sheets
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            values = [
                now,
                video_url,
                video_data["videoId"],
                video_data["title"],
                video_data["viewCount"],
                video_data["likeCount"],
                video_data["commentCount"],
                video_data["publishedAt"],
                result["預估總流量"]
            ]
            sheet.append_row(values)

            # 📈 擷取歷史紀錄並繪圖
            history = pd.DataFrame(sheet.get_all_records())
            if not history.empty and "分析時間" in history and "觀看數" in history:
                history["分析時間"] = pd.to_datetime(history["分析時間"])
                plot_growth(history[history["影片ID"] == video_id])
        else:
            st.warning("⚠️ 找不到影片資料，可能該影片不存在或設為私人。")
