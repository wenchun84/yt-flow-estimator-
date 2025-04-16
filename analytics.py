from datetime import datetime
import math

def estimate_traffic(data):
    # 解析資料
    view_count = data["viewCount"]
    like_count = data["likeCount"]
    comment_count = data["commentCount"]
    publish_time = datetime.strptime(data["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
    
    now = datetime.utcnow()
    days_online = (now - publish_time).days or 1  # 避免除以 0

    # 互動率計算
    interaction_rate = (like_count + comment_count) / view_count

    # 日成長率估算（視互動率、日均觀看數推估）
    daily_growth_rate = min(max(interaction_rate * 3, 0.01), 0.08)  # 限制在 1%~8%

    # 預估未來 30 天
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
