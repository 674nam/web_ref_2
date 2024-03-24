# グラフ作成用
import plotly.graph_objects as go

# viewから値を受け取り、グラフをhtmlにしてviewに返却する処理
class GraphGenerator:
    # グラフの装飾
    pie_line_color = '#000'
    plot_bg_color = 'rgb(255,255,255)'
    paper_bg_color = 'rgb(255,255,255)'
    payment_color = 'indianred'
    income_color = 'royalblue'
    font_color = 'dimgray'

    # 円グラフ：月別収支
    def month_pie(self, labels, values):
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
                l=20, r=0, b=0, t=30,
            ),
            height=250, # 円グラフの高さを調整
        )
        return fig.to_html(include_plotlyjs=False)


    # 棒グラフ：日別支出
    def month_daily_bar_payment(self, x_list, y_list):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
            marker_color=self.payment_color, # 棒の色
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
            ),
            height=250  # 棒グラフの高さ調整
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(tickangle=45)  # x軸のラベルを45度傾ける
        return fig.to_html(include_plotlyjs=False) # グラフ情報をhtml化


    # 棒グラフ：日別収入
    def month_daily_bar_income(self, x_list, y_list):
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
            marker_color=self.income_color, # グラフの装飾
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
            ),
            height=250  # 棒グラフの高さ調整
        )
        fig.update_yaxes(automargin=True)
        fig.update_xaxes(tickangle=45)  # x軸のラベルを45度傾ける
        return fig.to_html(include_plotlyjs=False) # グラフ情報をhtml化

    # グラフ：月間推移
    def transition_plot(self,
                        x_list_payment=None,
                        y_list_payment=None,
                        x_list_income=None,
                        y_list_income=None):
        fig = go.Figure()

        # # 折れ線グラフ：月間支出
        # if x_list_payment and y_list_payment:
        #     fig.add_trace(go.Scatter(
        #         x=x_list_payment,
        #         y=y_list_payment,
        #         mode='lines',
        #         name='payment',
        #         opacity=0.5,
        #         line=dict(color=self.payment_color,
        #                 width=5, )
        #     ))

        # # 折れ線グラフ：月間収入
        # if x_list_income and y_list_income:
        #     fig.add_trace(go.Scatter(
        #         x=x_list_income,
        #         y=y_list_income,
        #         mode='lines',
        #         name='income',
        #         opacity=0.5,
        #         line=dict(color=self.income_color,
        #                 width=5, )
        #     ))

        # 棒グラフ：月間支出
        if x_list_payment and y_list_payment:
            fig.add_trace(go.Bar(
                x=x_list_payment,
                y=y_list_payment,
                name='payment',
                marker_color=self.payment_color,
            ))

        # 棒グラフ：月間収入
        if x_list_income and y_list_income:
            fig.add_trace(go.Bar(
                x=x_list_income,
                y=y_list_income,
                name='income',
                marker_color=self.income_color,
            ))

        # グラフの装飾
        fig.update_layout(
            paper_bgcolor=self.paper_bg_color,
            plot_bgcolor=self.plot_bg_color,
            font=dict(size=14, color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0, r=0, b=20, t=30,
            ),
            yaxis=dict(
                showgrid=False,
                linewidth=1,
                rangemode='tozero'
                ),
                height=400  # グラフの高さ調整
            )

        fig.update_yaxes(showticklabels=True)  # 目盛り表示
        fig.update_xaxes(tickangle=45)  # x軸のラベルを45度傾ける
        return fig.to_html(include_plotlyjs=False)