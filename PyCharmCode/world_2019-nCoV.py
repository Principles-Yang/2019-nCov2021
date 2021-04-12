import pandas as pd
import pyecharts
import pyecharts.options as opts
from pyecharts.charts import Map

world_data = pd.read_csv('./today_world_2021_04_02.csv')
#各国家的 累计确诊人数---累计治愈----累计死亡人数===现存确诊人数
world_data['today_storeConfirm'] = world_data['total_confirm'] - world_data['total_heal'] - world_data['total_dead']
contry_name = pd.read_csv('./county_china_english.csv', encoding='GB2312')
world_data['eg_name'] = world_data['name'].replace(contry_name['中文'].values ,contry_name['英文'].values)
heatmap_data = world_data[['eg_name','today_storeConfirm']].values.tolist()
#绘图
map_test = Map().add(series_name = "现存确诊人数",
                 data_pair = heatmap_data, 
                 maptype = "world",
                 is_map_symbol_show = False
                )
map_test.set_series_opts(label_opts=opts.LabelOpts(is_show=False))  
map_test.set_global_opts(title_opts = opts.TitleOpts(title="世界各国现有确诊人数地图 截止：2021.04.02"), 
                     is_piecewise = True)
map_test.render('map_world_test.html')

