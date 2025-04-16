import streamlit as st
from googleapiclient.discovery import build
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ====== 參數設定 ======
YOUTUBE_API_KEY = "AIzaSyB-vJVbuZAu7-4pHUqt8JaGdhfKle8m4cI"
SHEET_URL = "https://docs.google.com/spreadsheets/d/12U90TfY6uJyrqfaCjYs0zW8uMYgdaDomzzJYlpfV-bE"

# ====== Google Sheets 認證 ======
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = st.secrets["google_sheets"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_url(SHEET_URL).sheet1

# ====== YouTube API 初始化 ======
youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

# ====== Streamlit UI ======
st.set_page_config(page_title="YouTube 流量分析器", page_icon="📊")
st.title("📊 YouTube 流量分析器")

video_url = st.text_input("請貼上 YouTube 影片連結：")

# ====== 擷取影片 ID ======
def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return None

# ====== 分析主流程 ======
if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("❌ 無法擷取影片 ID，請確認網址正確")
    else:
        try:
            response = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            ).execute()

            if not response["items"]:
                st.warning("⚠️ 找不到影片，請確認是否為公開影片")
            else:
                item = response["items"][0]
                snippet = item["snippet"]
                stats = item["statistics"]

                title = snippet["title"]
                published_at = snippet["publishedAt"]
                views = int(stats.get("viewCount", 0))
                likes = int(stats.get("likeCount", 0))
                comments = int(stats.get("commentCount", 0))
                published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                now = datetime.utcnow()
                days_online = max((now - published_date).days, 1)
                avg_per_day = views / days_online
                predicted_30d = int(avg_per_day * 30)

                # ====== 顯示分析結果 ======
                st.success("✅ 影片資料讀取成功")
                st.write(f"📌 標題：**{title}**")
                st.write(f"🗓 上傳時間：{published_date.strftime('%Y-%m-%d %H:%M')}")
                st.write(f"▶️ 觀看數：{views:,}")
                st.write(f"👍 喜歡數：{likes:,}")
                st.write(f"💬 留言數：{comments:,}")
                st.write(f"📈 平均每日觀看數：約 {int(avg_per_day):,}")
                st.write(f"📊 預估 30 天流量：約 **{predicted_30d:,}**")

                # ====== 寫入 Google Sheet ======
                sheet.append_row([
                    datetime.now().strftime("%Y/%m/%d %H:%M"),
                    video_url,
                    video_id,
                    title,
                    views,
                    likes,
                    comments,
                    published_date.strftime("%Y/%m/%d %H:%M"),
                    predicted_30d
                ])
                st.success("✅ 已寫入 Google Sheet！")

        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
