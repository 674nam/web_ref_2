# # ビュークラス使用 money/urls.pyも変更する必要あり
# import calendar
# import datetime
# from django.shortcuts import render, redirect
# from django.utils import timezone
# from django.views import View

# import matplotlib.pyplot as plt # pip install必要
# import pytz # pip install必要

# from .models import Money
# from .forms import SpendingForm
# from .utils import index_utils # index_utils.pyに分けた関数

# plt.rcParams['font.family'] = 'MS Gothic' #日本語フォント表示

# today = str(timezone.now()).split('-')

# class MainView(View):
#     def get(self, request, year=today[0], month=today[1]):
#         year = int(year)
#         month = int(month)
#         money = Money.objects.filter(use_date__year=year,
#                 use_date__month=month).order_by('use_date')
#         total = index_utils.calc_month_pay(money)
#         index_utils.format_date(money)
#         form = SpendingForm()
#         next_year, next_month = index_utils.get_next(year, month)
#         prev_year, prev_month = index_utils.get_prev(year, month)
#         context = {'year' : year,
#                 'month' : month,
#                 'prev_year' : prev_year,
#                 'prev_month' : prev_month,
#                 'next_year' : next_year,
#                 'next_month' : next_month,
#                 'money' : money,
#                 'total' : total,
#                 'form' : form
#                 }

#         draw_graph(year, month)

#         return render(request, 'money/index.html', context)

#     def post(self, request, year=today[0], month=today[1]):
#         year = int(year)
#         month = int(month)
#         data = request.POST
#         use_date = data['use_date']
#         cost = data['cost']
#         detail = data['detail']
#         category = data['category']

#         use_date = timezone.datetime.strptime(use_date, "%Y/%m/%d")
#         tokyo_timezone = pytz.timezone('Asia/Tokyo')
#         use_date = tokyo_timezone.localize(use_date)
#         use_date += datetime.timedelta(hours=9)

#         Money.objects.create(
#                 use_date = use_date,
#                 detail = detail,
#                 cost = int(cost),
#                 category = category,
#                 )
#         return redirect(to='/money/{}/{}'.format(year, month))


# def draw_graph(year, month):
#     money = Money.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
#     last_day = calendar.monthrange(year, month)[1] + 1
#     day = list(range(1, last_day))
#     cost = [0] * len(day)
#     for m in money:
#         day_index = m.use_date.day - 1
#         cost[day_index] += m.cost

#     plt.figure()
#     plt.bar(day, cost, color='#00bfff', edgecolor='#0000ff')
#     plt.grid(True)
#     plt.xlim([0, last_day])
#     plt.xlabel('日付', fontsize=16)
#     plt.subplot().set_ylabel('支\n出\n額\n(円)', fontsize=16, labelpad=15, rotation=0, va='center')
#     # static/imagesフォルダに保存
#     plt.savefig('money/static/images/bar_{}_{}.svg'.format(year, month), transparent=True)


# ビュークラス不使用
import calendar
import datetime
from django.shortcuts import render, redirect
from django.utils import timezone

import matplotlib.pyplot as plt # コマンドpip install matplotlibでインストール
import pytz # コマンドpip install pytzでインストール

from .models import Money
from .forms import SpendingForm
from .utils import index_utils

plt.rcParams['font.family'] = 'MS Gothic'

today = str(timezone.now()).split('-')

def index(request, year=today[0], month=today[1]):
    year = int(year)
    month = int(month)
    money = Money.objects.filter(use_date__year=year,
                                use_date__month=month).order_by('use_date')
    total = index_utils.calc_month_pay(money)
    index_utils.format_date(money)
    form = SpendingForm()
    next_year, next_month = index_utils.get_next(year, month)
    prev_year, prev_month = index_utils.get_prev(year, month)
    context = {
        'year': year,
        'month': month,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'money': money,
        'total': total,
        'form': form
    }

    draw_graph(year, month)

    return render(request, 'money/index.html', context)


def post(request, year=today[0], month=today[1]):
    year = int(year)
    month = int(month)
    data = request.POST
    use_date = data['use_date']
    cost = data['cost']
    detail = data['detail']
    category = data['category']

    use_date = timezone.datetime.strptime(use_date, "%Y/%m/%d")
    tokyo_timezone = pytz.timezone('Asia/Tokyo')
    use_date = tokyo_timezone.localize(use_date)
    use_date += datetime.timedelta(hours=9)

    Money.objects.create(
        use_date=use_date,
        detail=detail,
        cost=int(cost),
        category=category,
    )
    return redirect(to='/money/{}/{}'.format(year, month))


def draw_graph(year, month):
    money = Money.objects.filter(use_date__year=year, use_date__month=month).order_by('use_date')
    last_day = calendar.monthrange(year, month)[1] + 1
    day = list(range(1, last_day))
    cost = [0] * len(day)
    for m in money:
        day_index = m.use_date.day - 1
        cost[day_index] += m.cost

    plt.figure()
    plt.bar(day, cost, color='#00bfff', edgecolor='#0000ff')
    plt.grid(True)
    plt.xlim([0, last_day])
    plt.xlabel('日付', fontsize=16)
    plt.subplot().set_ylabel('支\n出\n額\n(円)', fontsize=16, labelpad=15, rotation=0, va='center')
    plt.savefig('money/static/images/bar_{}_{}.svg'.format(year, month), transparent=True)
