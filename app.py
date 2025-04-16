import streamlit as st
from googleapiclient.discovery import build

# YouTube API 金鑰（來自 secrets.toml）
API_KEY = st.secrets["youtube"]["api_key"]

# 建立 YouTube API 服務
youtube = build("youtube", "v3", developerKey=API_KEY)

# Streamlit 介面
st.title("📺 YouTube 影片流量預估工具")
video_url = st.text_input("請輸入 YouTube 影片連結", "")

if video_url:
    try:
        # 解析影片 ID
        if "v=" in video_url:
            video_id = video_url.split("v=")[-1].split("&")[0]
        elif "youtu.be/" in video_url:
            video_id = video_url.split("youtu.be/")[-1].split("?")[0]
        else:
            st.error("⚠️ 無法解析影片 ID，請確認連結格式正確")
            st.stop()

        # 呼叫 YouTube API 取得影片資訊
        response = youtube.videos().list(
            part="snippet,statistics",
            id=video_id
        ).execute()

        if response["items"]:
            video = response["items"][0]
            snippet = video["snippet"]
            stats = video["statistics"]

            # 顯示影片資訊
            st.subheader(snippet["title"])
            st.image(snippet["thumbnails"]["high"]["url"])
            st.write("🧾 頻道名稱：", snippet["channelTitle"])
            st.write("👁️‍🗨️ 觀看數：", stats.get("viewCount", "N/A"))
            st.write("👍 喜歡數：", stats.get("likeCount", "N/A"))
            st.write("💬 留言數：", stats.get("commentCount", "N/A"))

        else:
            st.warning("⚠️ 找不到該影片，請確認影片 ID 是否正確")

    except Exception as e:
        st.error(f"🚨 錯誤：{e}")
