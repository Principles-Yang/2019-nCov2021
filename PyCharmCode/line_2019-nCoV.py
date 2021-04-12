import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib.ticker as ticker
import pandas as pd
import pyecharts
import pyecharts.options as opts
from pyecharts.charts import Map
import datetime
# 读取数据
alltime_world = pd.read_csv("./historytime_world_2021_04_02.csv",encoding='utf_8_sig')

# # 创建中文列名字典
# name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
#              'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
#              'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
#              'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊',
#              'total_confirm':'累计确诊','total_suspect':'累计疑似',
#              'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症'}

# 更改列名
# alltime_world.rename(columns=name_dict,inplace=True)

# 将日期一列数据类型变为datetime
alltime_world['date'] = pd.to_datetime(alltime_world['date'])

# 计算当日现存确诊
alltime_world['today_storeConfirm'] = alltime_world['total_confirm']-alltime_world['total_heal']-alltime_world['total_dead']

alltime_world.to_csv("historytime_world_after.csv",encoding='utf_8_sig')