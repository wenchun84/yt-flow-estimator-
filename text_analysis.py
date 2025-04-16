def generate_analysis_text(result):
    view = result["觀看數"]
    like = result["按讚數"]
    comment = result["留言數"]
    estimated = result["預估總流量"]

    interaction_rate = (like + comment) / view if view else 0
    growth_factor = estimated / view if view else 1

    text = "### 🔎 影片潛力分析摘要：\n\n"

    # 分析互動率
    if interaction_rate > 0.04:
        text += "- 互動率：高（超過平均），觀眾參與度強。\n"
    elif interaction_rate > 0.015:
        text += "- 互動率：中等，有不錯的參與，但仍有提升空間。\n"
    else:
        text += "- 互動率：偏低，建議改善影片前段吸引力。\n"

    # 分析成長潛力
    if growth_factor > 5:
        text += "- 預估總流量遠高於目前觀看數，有爆紅潛力！\n"
    elif growth_factor > 2:
        text += "- 有一定成長空間，建議持續觀察成長速度。\n"
    else:
        text += "- 成長幅度有限，可能已接近流量高峰。\n"

    # 建議
    if interaction_rate > 0.03 and growth_factor > 3:
        text += "\n📈 綜合判斷：建議強化推播、投放廣告或發文引流！\n"
    elif interaction_rate < 0.01:
        text += "\n🔧 建議：優化縮圖與標題來提升點擊與互動率。\n"

    return text
