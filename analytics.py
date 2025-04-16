# analytics.py
from datetime import datetime

# ✅ 精緻估算函式（加入 Shorts / 長影片分類 + 日成長衰減）
def estimate_traffic(video_data):
    views = video_data["viewCount"]
    likes = video_data["likeCount"]
    comments = video_data["commentCount"]
    published = video_data["publishedAt"]
    video_id = video_data["videoId"]
    title = video_data["title"]
    url = f"https://www.youtube.com/watch?v={video_id}"

    # 影片上傳時間
    published_time = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.utcnow()
    days_since_upload = max((now - published_time).days, 1)

    # 分類是否為 Shorts（ID ≤ 12 或網址中包含 shorts）
    is_shorts = len(video_id) <= 12 or "shorts" in url.lower()

    # 計算互動率
    interaction_rate = (likes + comments) / views if views > 0 else 0

    # 📊 分類模型參數
    if is_shorts:
        base_growth = 0.0025
        multiplier = 1.8
        max_growth = 0.015
    else:
        base_growth = 0.0015
        multiplier = 1.6
        max_growth = 0.01

    # 📈 日成長率計算（可微調）
    raw_growth = base_growth + interaction_rate * multiplier
    adjusted_growth = min(raw_growth, max_growth)

    # 📉 日成長衰減：每 5 天遞減 10%
    total_estimate = 0
    for day in range(30):
        decay_factor = 0.9 ** (day // 5)
        daily = views * adjusted_growth * decay_factor
        total_estimate += daily

    return {
        "分析時間": now.strftime("%Y-%m-%d %H:%M:%S"),
        "影片連結": url,
        "影片ID": video_id,
        "標題": title,
        "觀看數": views,
        "按讚數": likes,
        "留言數": comments,
        "上傳時間": published_time.strftime("%Y-%m-%d %H:%M:%S"),
        "互動率": round(interaction_rate * 100, 2),
        "預估總流量": int(views + total_estimate)
    }
