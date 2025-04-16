import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime

# 讀取 API Key
import os
API_KEY = os.environ.get("YOUTUBE_KEY")

# YouTube API 初始化
youtube = build("youtube", "v3", developerKey=API_KEY)

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
            title = video["snippet"]["title"]
            channel = video["snippet"]["channelTitle"]
            published = video["snippet"]["publishedAt"]
            views = int(video["statistics"].get("viewCount", 0))
            likes = int(video["statistics"].get("likeCount", 0))
            comments = int(video["statistics"].get("commentCount", 0))
            published_dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
            age_days = (datetime.utcnow() - published_dt).days + 1

            st.subheader("🎬 影片資訊")
            st.write(f"標題：{title}")
            st.write(f"頻道：{channel}")
            st.write(f"上傳時間：{published_dt.strftime('%Y-%m-%d %H:%M')}")
            st.write(f"觀看數：{views:,}")
            st.write(f"按讚數：{likes:,}")
            st.write(f"留言數：{comments:,}")
            st.write(f"已上線天數：{age_days} 天")

            # 預估：平均每日觀看數 × 30 天
            daily_avg = views / age_days
            predicted_total = daily_avg * 30
            st.subheader("📈 流量推估")
            st.write(f"目前平均每日觀看：約 {int(daily_avg):,} 次")
            st.write(f"預估 30 天總觀看數：約 {int(predicted_total):,} 次")
        else:
            st.error("查無影片資訊，請確認網址正確")
    else:
        st.error("無法解析影片 ID")
