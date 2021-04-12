from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
from pyecharts.faker import Faker
import pandas as pd
pd.set_option('display.max_rows',None) #显示多少行
pd.set_option('display.max_columns', None)   #显示多少列


# # #挑选出疫情最为严重的10个国家，并筛选出这些国家的历史疫情数据
# # historytime_data = pd.read_csv('./historytime_world_2021_04_02.csv')
# # #美国 巴西 印度 法国 俄罗斯 英国 意大利 土耳其 西班牙 德国
# # country_list = ['美国', '巴西', '印度', '法国', '俄罗斯', '英国', '意大利', '土耳其', '西班牙','德国']
# # need_data = historytime_data[historytime_data['name'].isin(country_list)]


# 读取数据
alltime_world = pd.read_csv("./historytime_world_finial.csv")

# 创建中文列名字典
name_dict = {'date':'日期','name':'名称','id':'编号','lastUpdateTime':'更新时间',
             'today_confirm':'当日新增确诊','today_suspect':'当日新增疑似',
             'today_heal':'当日新增治愈','today_dead':'当日新增死亡',
             'today_severe':'当日新增重症','today_storeConfirm':'当日现存确诊','today_input':'当日输入病例',
             'total_confirm':'累计确诊','total_suspect':'累计疑似',
             'total_heal':'累计治愈','total_dead':'累计死亡','total_severe':'累计重症','total_input':'累计输入病例'}

# 更改列名
alltime_world.rename(columns=name_dict,inplace=True)

# print(alltime_world.head())


# 将日期一列数据类型变为datetime
# alltime_world['日期'] = pd.to_datetime(alltime_world['日期'])

# 计算当日现存确诊
# alltime_world['当日现存确诊'] = alltime_world['累计确诊']-alltime_world['累计治愈']-alltime_world['累计死亡']
# print(alltime_world.info())  #查看数据信息、类型、缺失值
# print(len(alltime_world['名称'].unique()))   #统计唯一值 国家 的数量
# print(alltime_world.head())


# 数据预处理
# 设置日期索引
# alltime_world.set_index('日期',inplace=True)
# # groupby创建层次化索引
# data = alltime_world.groupby(['日期','名称']).mean()
# data.reset_index('名称',inplace=True)
# 提取部分数据
#美国 巴西 印度 法国 俄罗斯 英国 意大利 土耳其 西班牙 德国  loc(axis=0)按行挑选
# data_part = data.loc(axis=0)[:,['美国', '巴西', '印度', '法国', '俄罗斯', '英国', '意大利', '土耳其', '西班牙','德国']]
# 将层级索引还原
# data_part.reset_index('名称',inplace=True)
# print(data)
# 格式dataframe




# confirm = [(1,2,45,67),24,23,12,21,23,24,213,31]
# dead = [(2,56,73,78),23,23,34,21]
# confirm.append(data_part['2021-03':'2021-03-31'].groupby('名称')['累计确诊'])
# dead.append(data_part['2021-03':'2021-03-31'].groupby('名称')['累计死亡'])

tl = Timeline()
for i in range(1,32):

    country_list = ['德国','美国', '巴西', '土耳其', '法国','印度','英国',  '意大利', '俄罗斯',  '西班牙',]
    total_confirm_list = list(alltime_world['累计确诊'])
    total_dead_list = list(alltime_world['累计死亡'])
    # print(total_confirm_list)
    bar = (
        Bar()
        .add_xaxis(country_list)
        .add_yaxis("累计确诊", total_confirm_list, label_opts=opts.LabelOpts(position="right"))
        .add_yaxis("累计死亡", total_dead_list, label_opts=opts.LabelOpts(position="right"))
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts("Timeline-Bar-Reversal (时间: {} 日)".format(i))
        )
    )
    tl.add(bar, "{}日".format(i))
tl.render("timeline_bar_reversal2.html")