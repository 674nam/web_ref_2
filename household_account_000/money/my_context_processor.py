# 月間グラフ用
# 現在年と現在月の共通contextの設定
# settings.pyのTEMPLATESに追記あり
# 月間支出ページのurlにも表示⇒urls.py記載
from django.utils import timezone

def common(request): # 家計簿アプリの共通コンテクスト
    now = timezone.now()

    return {"now_year": now.year,
            "now_month": now.month}