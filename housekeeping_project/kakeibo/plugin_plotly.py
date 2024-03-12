# グラフ作成用のクラス、ダッシュボードページ装飾
# ビューから値を受け取り、グラフをhtmlにしてビューに返却する処理
import plotly.graph_objects as go

class GraphGenerator: # ビューから呼び出され、グラフをhtmlにして返す
    # グラフの装飾
    pie_line_color = '#000'
    plot_bg_color = 'rgb(255,255,255)'
    paper_bg_color = 'rgb(255,255,255)'
    month_bar_color = 'indianred'
    font_color = 'dimgray'

    def month_pie(self, labels, values): # 月間支出のパイチャート
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=labels,
            values=values
        ))

        # グラフの装飾
        fig.update_traces(
            hoverinfo='label+percent',
            textinfo='value',
            textfont_size=14,
            marker=dict(line=dict(color=self.pie_line_color, width=2))
        )
        fig.update_layout(
            margin=dict(
                autoexpand=True,
                l=20, r=0, b=0, t=30,),
            height=300,
        )

        return fig.to_html(include_plotlyjs=False)


    def month_daily_bar(self, x_list, y_list): # 月間支出の日別バーチャート
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
            marker_color=self.month_bar_color, # グラフの装飾
        ))

        # グラフの装飾
        fig.update_layout(
            paper_bgcolor=self.paper_bg_color,
            plot_bgcolor=self.plot_bg_color,
            font=dict(size=14, color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0, r=0, b=20, t=10,
            ),
            yaxis=dict(
                showgrid=False,
                linewidth=1,
                rangemode='tozero'
            ))
        fig.update_yaxes(automargin=True)

        return fig.to_html(include_plotlyjs=False) # グラフ情報をhtml化