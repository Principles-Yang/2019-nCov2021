import requests
import pandas as pd
import time 
import json
pd.set_option('display.max_rows',None) #显示多少行
pd.set_option('display.max_columns', None)   #显示多少列

# 爬取
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'  
r = requests.get(url, headers=headers) 
print(r.status_code) 
data_json = json.loads(r.text)
data = data_json['data']

# 提取数据
def get_data(data, info_list):
    info = pd.DataFrame(data)[info_list] 
    today_data = pd.DataFrame([i['today'] for i in data])  
    today_data.columns = ['today_' + i for i in today_data.columns]  
    total_data = pd.DataFrame([i['total'] for i in data]) 
    total_data.columns = ['total_' + i for i in total_data.columns]  
    return pd.concat([info, total_data, today_data], axis=1)  

# 保存数据
def save_data(data,name):
    file_name = name+'_'+time.strftime('%Y_%m_%d',time.localtime(time.time()))+'.csv'
    data.to_csv(file_name,index=None,encoding='utf_8_sig')
    print(file_name+' 保存成功！')

areaTree = data["areaTree"]

# 功能：传递参数 保存全球当日疫情数据
today_world = get_data(areaTree,['id','lastUpdateTime','name'])
save_data(today_world,'today_world')


#各国历史数据爬取
today_world = get_data(areaTree,['id','lastUpdateTime','name'])
country_dict = {key:value for key,value in zip(today_world['id'], today_world['name'])}
start = time.time()
for country_id in country_dict:  # 遍历每个国家的编号
    try:
        url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-by-area-code?areaCode=' + country_id
        r = requests.get(url, headers=headers)
        json_data = json.loads(r.text)
        country_data = get_data(json_data['data']['list'], ['date'])
        country_data['name'] = country_dict[country_id]
        if country_id == '9577772':
            alltime_world = country_data
        else:
            alltime_world = pd.concat([alltime_world, country_data])
        print('-' * 20, country_dict[country_id], '成功', country_data.shape, alltime_world.shape,
              ',累计耗时:', round(time.time() - start), '-' * 20)
        time.sleep(20)
    except:
        print('-' * 20, country_dict[country_id], 'wrong', '-' * 20)
save_data(alltime_world,'historytime_world')