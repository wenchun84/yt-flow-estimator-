
from datetime import datetime
import math

def estimate_traffic(data):
    view_count = data["viewCount"]
    like_count = data["likeCount"]
    comment_count = data["commentCount"]
    title = data["title"].lower()
    video_id = data["videoId"]
    publish_time = datetime.strptime(data["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    
    now = datetime.utcnow()
    days_online = (now - publish_time).days or 1

    # 判斷是否為 Shorts
    is_shorts = "shorts" in title or len(video_id) <= 12  # YouTube Shorts ID 通常較短

    # 🔹 互動率估算（按讚 + 留言 / 觀看數）
    interaction_rate = (like_count + comment_count) / view_count if view_count > 0 else 0

    # 🔸 Shorts 與 Longs 採不同基準
    if is_shorts:
        base_growth = 0.015
        multiplier = 3.5
        max_growth = 0.1
    else:
        base_growth = 0.008
        multiplier = 2.5
        max_growth = 0.06

    # 調整後每日成長率
    daily_growth_rate = min(max(interaction_rate * multiplier, base_growth), max_growth)

    # 🔹 預估 30 天後總觀看數
    projected_views = view_count
    for _ in range(30 - days_online):
        projected_views += projected_views * daily_growth_rate

    return {
        "分析時間": now.strftime("%Y-%m-%d %H:%M:%S"),
        "影片連結": f"https://www.youtube.com/watch?v={data['videoId']}",
        "影片ID": data["videoId"],
        "標題": data["title"],
        "觀看數": view_count,
        "按讚數": like_count,
        "留言數": comment_count,
        "上傳時間": publish_time.strftime("%Y-%m-%d %H:%M:%S"),
        "預估總流量": int(projected_views)
    }
