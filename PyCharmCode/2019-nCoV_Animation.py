import pandas as pd
from datetime import datetime,timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import pyecharts
import pyecharts.options as opts
from pyecharts.charts import Map

#挑选出疫情最为严重的10个国家，并筛选出这些国家的历史疫情数据
historytime_data = pd.read_csv('./historytime_world_2021_04_02.csv')
#美国 巴西 印度 法国 俄罗斯 英国 意大利 土耳其 西班牙 德国
country_list = ['美国', '巴西', '印度', '法国', '俄罗斯', '英国', '意大利', '土耳其', '西班牙','德国']
need_data = historytime_data[historytime_data['name'].isin(country_list)]
time_list = [(datetime(2021, 1, 1) + timedelta(i)).strftime('%Y-%m-%d') for i in range(90)]
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['figure.dpi'] = 100
color_list = ['blue','brown','peru','orange','green','red','yellow','teal','pink','orchid']
country_color = pd.DataFrame()
country_color['country'] = country_list
country_color['color'] = color_list

#绘制动态条形图
def barh_draw(day):
    # 提取每一天的数据
    draw_data = need_data[need_data['date'] == day][['name', 'total_confirm']].sort_values(by='total_confirm',
                                                                                           ascending=True)
    ax.clear()
    ax.barh(draw_data['name'], draw_data['total_confirm'],
             color=[country_color[country_color['country'] == i]['color'].values[0] for i in draw_data['name']])

    dx = draw_data['total_confirm'].max() / 2
    for j, (name, value) in enumerate(zip(draw_data['name'], draw_data['total_confirm'])):
         ax.text(value + dx, j, f'{value:,.0f}', size=10, ha='left', va='center')
    ax.text(dead_data['total_dead'].max() * 0.75, 0.4, day, color='#777777', size=40, ha='left')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=15)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.text(0, 11, '世界各国家累计确诊动态条形图', size=20, ha='left')
    plt.box(False)
    plt.close()

fig, ax = plt.subplots(figsize=(12, 8))
animator = animation.FuncAnimation(fig, barh_draw, frames=time_list, interval=200)
with open('./世界各国家累计确诊动态条形图.html','w') as f:
    f.write(animator.to_jshtml())

