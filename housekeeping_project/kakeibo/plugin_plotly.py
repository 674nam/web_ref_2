# グラフ作成用のクラス、ダッシュボードページ装飾
# ビューから値を受け取り、グラフをhtmlにしてビューに返却する処理
import plotly.graph_objects as go

class GraphGenerator: # ビューから呼び出され、グラフをhtmlにして返す

    def month_pie(self, labels, values): # 月間支出のパイチャート
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=labels,
                             values=values))

        return fig.to_html(include_plotlyjs=False)

    def month_daily_bar(self, x_list, y_list):# 月間支出の日別バーチャート
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
        ))

        return fig.to_html(include_plotlyjs=False) # グラフ情報をhtml化