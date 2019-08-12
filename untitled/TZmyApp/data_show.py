from django.db import models
import json
from TZmyApp import models
import tushare as ts
def _out_log(request):
    contains = json.loads(_open_and_readfile(request))
    #username1 = request.POST.get("username", None)
    #password1 = request.POST.get("password", None)
    if contains:
        models.result.objects.create( open_num=contains['open'],
                             high_num=contains['high'], close_num=contains['close'], low_name=contains['low'],volume_num=contains['volume'])
        list1 = models.result.objects.all()
        return list1
    else:
        models.result.objects.create(open_num=contains['open'],
                                     high_num=contains['high'], close_num=contains['close'], low_name=contains['low'],
                                     volume_num=contains['volume'])

def _open_and_readfile(request):
    hs300 = ts.get_k_data('hs300', start='2013-01-01', end='2013-01-25')  # 训练集数据
    #hs300.set_index('date', inplace=True)
    open1 = hs300['open']
    high = hs300['high']
    close = hs300['close']
    low = hs300['low']
    volume = hs300['volume']
    _result_list = json.dumps({'open': open1, 'high': high, 'close': close,'low': low, 'volume': volume})
    print(_result_list)
    #_result_list = json.dumps({'anr': anr, 'crash': crash, 'exception': exception, 'is_finish': is_finish, 'total': total})
    return  _result_list



