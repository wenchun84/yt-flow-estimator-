# app.py
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
from urllib.parse import urlparse, parse_qs
from analytics import estimate_traffic

# ✅ 初始化 YouTube API
api_key = st.secrets["youtube"]["api_key"]
youtube = build("youtube", "v3", developerKey=api_key)

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
            st.dataframe(pd.DataFrame([result]))
        else:
            st.warning("⚠️ 找不到影片資料，可能該影片不存在或設為私人。")
