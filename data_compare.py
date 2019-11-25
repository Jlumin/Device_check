# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 15:18:42 2019

@author: Luming
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:03:12 2019

@author: Luming
"""
import PyQt5
import requests
import urllib.request
import re
import os 
import pandas as pd
from datetime import datetime
import numpy as np
import shutil
# =============================================================================
# print('相關站號及日期輸入請閱讀下載格式說明文件')


#id = input('輸入站號:')

def error_test(id,date):
#date = '20190903'
#pull the csv from database
# 
#for i in range(len(id)):

    url='http://ec2-54-175-179-28.compute-1.amazonaws.com/get_csv_xitou.php?device_id='+str(id)+'&year_month='+str(date)
# print(url)
# 
    r=requests.get(url)
# 
    csv_LINK_PATTERN = 'href="(.*)">Download'
    req = urllib.request.Request(url)
    html = urllib.request.urlopen(req)
    doc = html.read().decode('utf8')
#    print(doc)
    url_list = list(set(re.findall(csv_LINK_PATTERN, doc)))
# 
    string1 = "'>Download ID" + str(id) + str(date) +" Data</a><br>"
# 
    get_rul_patten = doc.strip(string1).strip("<a href='")
# 
# 
    file_name = get_rul_patten.strip('temp_file/').strip('.csv')
# 
    server_path="http://ec2-54-175-179-28.compute-1.amazonaws.com/"+ get_rul_patten
# 
# # =============================================================================
# # 創建資料夾及儲存檔案
# # =============================================================================
#如果是檔案則處理
    if not os.path.exists('./'+ file_name):
        os.makedirs('./'+ file_name)   # path 是”要建立的子目錄”
        urllib.request.urlretrieve(server_path,'./'+file_name+'/'+file_name+'.csv')
# 
# =============================================================================
#資料整理

    local_csv_pos = './'+file_name+'/'+file_name+'.csv'

    del_id = [0,2,4,6,8]
    csv_data = pd.read_csv(local_csv_pos,sep=", |,, | = |= ",header=None,index_col=False)
    csv_data.drop(del_id,axis=1, inplace=True)
#1.氣象資料(溫度、大氣壓力、濕度、風速、風向、雨量)
    wea = csv_data[3]
    compare= int(datetime.now().strftime("%Y%m%d%H%M")+"00")-int(wea[len(wea)-1])
    print("上次最後一筆時間為"+str(wea[len(wea)-1]))


#    data_test = wea['time'][0]-wea['time'][1]
    if int(str(compare)) > 20:
        print('機器故障，無傳輸訊號')
          
    else:
        print('正常')
date = datetime.now().strftime("%Y%m")

id = ["4001","4002","4003","4004","4005","4006","4007","4008","4009","4010","4011","4012"]
i=0
for i in range(len(id)):
    try:
        print(id[i]+"此站開始檢測")
        error_test(id[i],date)
        print(id[i]+"此站結束檢測")
    except:
        print(id[i]+"此站超過一個月停止傳輸")
        print(id[i]+"此站結束檢測")
# =============================================================================
    try:
       shutil.rmtree('./xitou_ID'+str(id[i])+'_TIME'+str(date))
    except:
       print("finish!!")
# =============================================================================












