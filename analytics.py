from datetime import datetime

def estimate_traffic(video_data):
    upload_time = datetime.strptime(video_data['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
    now = datetime.now()
    days_online = (now - upload_time).days or 1
    estimated_views = int(video_data['viewCount']) / days_online * 30

    return {
        "分析時間": now.strftime("%Y-%m-%d %H:%M:%S"),
        "影片連結": f"https://www.youtube.com/watch?v={video_data['videoId']}",
        "影片ID": video_data['videoId'],
        "標題": video_data['title'],
        "觀看數": video_data['viewCount'],
        "按讚數": video_data['likeCount'],
        "留言數": video_data['commentCount'],
        "上傳時間": upload_time.strftime("%Y-%m-%d %H:%M:%S"),
        "預估總流量": int(estimated_views)
    }
