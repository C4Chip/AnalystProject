from django.shortcuts import render
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline

import os

from datetime import datetime
from datetime import timedelta
from TZmyApp import models
#import datetime
import matplotlib.pyplot as plt
#%matplotlib inline
import pandas as pd
import numpy as np
import base64
from io import BytesIO
#list1 = {"date_num" : hs300['date'],open_num=hs300['open'],
#                             high_num=hs300['high'], close_num=hs300['close'], low_name=hs300['low'],volume_num=hs300['volume'],username=username,password=password}
# Create your views here.
def multiChart(data,symbol):
    plt.title(symbol)
    plt.plot(data)
    buffer = BytesIO()
    plt.savefig(buffer)
    plot_data = buffer.getvalue()
    return plot_data

# if request.method == 'POST':
#     # 获取用户通过post 提交过来的数据
#         user = request.POST.get('user',None)
#         pwd = request.POST.get('pwd',None)




# def filter(request):
#    if request.method == 'POST':
#        year_from=request.POST.get('year_from',None)
#        month_from = request.POST.get('month_from',None)
#        day_from = request.POST.get('day_from',None)
#        year_to = request.POST.get('year_to', None)
#        month_to = request.POST.get('month_to', None)
#        day_to = request.POST.get('day_to', None)


def LoadDataFrame(filename):
    df = pd.DataFrame()

    if os.path.isfile(filename):
        df = pd.read_csv(filepath_or_buffer=filename)
        df['<date>'] = df['<date>'].astype(str)

    return df


def LoadAllDataFrames(start, end):
    dfs = pd.DataFrame()

    dt_range = end - start

    for i in range(0, dt_range.days + 1):

        dt = start + timedelta(i)

        filename = "E:/H/citi/training/BackTesting/Back Testing/Test Data/FOREX_2011/FOREX_" + dt.strftime('%Y%m%d') + ".txt"

        df = LoadDataFrame(filename)

        if not df.empty:
            dfs = pd.concat([dfs, df])

    return dfs
# def getDate(request):
#     request1 = {}
#     if request.method == 'POST':
#         year_from = request.POST.get('year_from', None)
#         month_from = request.POST.get('month_from', None)
#         day_from = request.POST.get('day_from', None)
#         year_to = request.POST.get('year_to', None)
#         month_to = request.POST.get('month_to', None)
#         day_to = request.POST.get('day_to', None)
#         request1['year_from']=year_from
#         request1['month_from'] = month_from
#         request1['day_from'] = day_from
#         request1['year_to'] = year_to
#         request1['month_to'] = month_to
#         request1['day_to'] = day_to
#         return request1



def index(request):
    #mysql中读取数据
    #stock_list = models.StockInfo.objects.all()
    #stock_list_open = models.StockInfo.objects.get(id=1)
    #csv读取数据----------
    # df2 = pd.read_csv('E:/H/citi/training/BackTesting\Back Testing\Test Data\FOREX_2011/X.csv')
    # data = df2.values[:,:]
    # test_data = []
    # for line in data:
    #     ls=[]
    #     for j in line:
    #         ls.append(j)
    #     test_data.append(ls)
    # ar = np.array(test_data)
    #-----------------------
    year_from = request.POST.get('year_from', None)
    month_from = request.POST.get('month_from', None)
    day_from = request.POST.get('day_from', None)
    year_to = request.POST.get('year_to', None)
    month_to = request.POST.get('month_to', None)
    day_to = request.POST.get('day_to', None)
    start = datetime(year_from,month_from,day_from)
    end = datetime(year_to,month_to,day_to)
    symbol = "GBPUSD"
    df2 = LoadAllDataFrames( start, end)
    df2 = df2.set_index(['<ticker>'])
    df3 = df2.xs('GBPUSD')
    short = 10
    long = 60
    short_term = df3['<close>'].ewm(span=short).mean()
    long_term = df3['<close>'].ewm(span=long).mean()
    df_Res = pd.DataFrame()
    df_Res['short_term'] = np.round(short_term, 2)
    df_Res['long_term'] = np.round(long_term, 2)
    df_Res['Diff'] = df_Res['short_term'] - df_Res['long_term']
    df_Res['Regime'] = np.where(df_Res['Diff']/df_Res['long_term'] > 0.001, 1, 0)
    df_Res['Regime'] = np.where(df_Res['Diff'] / df_Res['long_term'] < -0.01, -1, df_Res['Regime'])
    df_Res['Market'] = np.log(df3['<close>'] / df3['<close>'].shift(1))
    df_Res['Strategy'] = df_Res['Regime'].shift(1) * df_Res['Market']
    for line in df_Res:
        ls=[]
        for j in line:
            ls.append(j)
        df_Res.append(ls)
    ar = np.array(df_Res)
    cols = ['Market', 'Strategy']
    datat = df_Res[cols].cumsum().apply(np.exp)
    plot_data1=multiChart(datat,symbol)
    imb1 = base64.b64encode(plot_data1)  # 对plot_data进行编码
    ims1 = imb1.decode()
    imd1 = "data:image/png;base64," + ims1
    return render(request, "index.html", {"img": imd1, "test_data": ar})

    # df = BackTest(symbol, start, end)
    # df = pd.read_csv('E:/H/SPX.csv',index_col = 'Date',parse_dates = True)
    # df['open'] = pd.to_numeric(df['open'].str.replace(',', ''))
    # df['high'] = pd.to_numeric(df['high'].str.replace(',', ''))
    # df['low'] = pd.to_numeric(df['low'].str.replace(',', ''))
    # df['close'] = pd.to_numeric(df['close'].str.replace(',', ''))
    # df['42d'] = df['close'].rolling(42).mean()
    # # 252days average 1 year
    # df['252d'] = df['close'].rolling(252).mean()
    # df['Diff'] = df['42d'] - df['252d']
    # thr = 0.03
    # df['Ragime'] = np.where(df['Diff'] / df['252d'] > thr, 1, 0)
    # df['Ragime'] = np.where(df['Diff'] / df['252d'] < -thr, -1, df['Ragime'])
    #
    # #df['volume'] = pd.to_numeric(df['volume'].str.replace(',', ''))
    #
    # df['Market'] = np.log(df['close'] / df['close'].shift(1))
    # df['Strategy'] = df['Ragime'].shift(1) * df['Market']
    # cols = ['Market', 'Strategy']
    # xx = df[cols].cumsum().apply(np.exp)
    #secondry_y = ['Diff']
    # plot_data1 =multiChart(xx)



