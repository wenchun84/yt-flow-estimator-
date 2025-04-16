# analytics.py
from datetime import datetime

def estimate_traffic(data):
    view_count = data["viewCount"]
    like_count = data["likeCount"]
    comment_count = data["commentCount"]
    publish_time = datetime.strptime(data["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.utcnow()

    # ⏳ 影片存活天數
    days_since_upload = max((now - publish_time).days, 1)

    # ⚡ 計算互動率：每千觀看多少互動
    interaction = (like_count + comment_count) / view_count if view_count else 0
    interaction_score = min(interaction * 1000, 100)  # capped

    # 📈 成長潛力模型（簡化）：越新、互動率越高、總流量潛力越大
    trend_factor = max(1 + (7 - days_since_upload) * 0.2, 1)
    estimated_total_views = int(view_count * (1 + interaction_score / 100) * trend_factor)

    return {
        "分析時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "影片連結": f"https://www.youtube.com/watch?v={data['videoId']}",
        "影片ID": data["videoId"],
        "標題": data["title"],
        "觀看數": view_count,
        "按讚數": like_count,
        "留言數": comment_count,
        "上傳時間": publish_time.strftime("%Y-%m-%d %H:%M:%S"),
        "預估總流量": estimated_total_views
    }
