import pandas as pd
import  numpy as np
import re
import math
import matplotlib.pyplot as plt
from CoolProp.CoolProp import PropsSI
from scipy.interpolate import interp1d


flie_name_excel = '1-oh-3.xls'
file_name_txt ='1-oh-3.txt'
fp_excel = pd.read_excel(flie_name_excel, sheet_name=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
fp_txt = pd.read_table(file_name_txt,sep='\t',encoding='gbk')
fp_location = pd.read_table('location.txt',sep='\s+')

print(len(fp_excel))
class A():
    def match_P(self,fp_txt):
        a=fp_txt.mean()
        a = a.dropna(how='any')
        P = []
        P.append(a.loc['入口P']-a.loc['DP1-2']/1000)  #入口压力指的是加热起始点处的压力，此处压力并没有直接测量，先用估算值
        for i in range(9,20):
            P.append(P[i-9]-a.iloc[i]/1000)
        location_P = list(range(230,6000,520))
        data_P =[]
        data_P.append(location_P)
        data_P.append(P)
        x ,y = data_P[0], data_P[1]
        f = interp1d(x, y, kind='linear')
        return  f , data_P

    #处理一个子excel表格里的数据，即处理的是一个工作表的内容
    def match_location(self,fp_excel,fp_txt,fp_location):
        f, data_P = self.match_P(fp_txt)
        data = []
        location_numpy = fp_location.to_numpy()
        middle=[]
        local_localtion =[]
        a=fp_excel
        b=a.dropna(how='any')

        list_num = a.iloc[0][1]
        list_num = str(list_num)
        # time_seq = b.iloc[:,0].tolist
        mean_temp_out = b.mean()
        mean_temp_out = mean_temp_out.to_numpy().tolist()

        for i in a.iloc[1]:
            i = str(i)
            i=re.findall(r"\d+",i)
            i=list_num + '-' + ''.join(i)
            location = np.where(location_numpy == i)
            row_index = location[0]
            columns_index = location[1]
            if len(row_index) !=0:
                row_index = int(row_index)
                columns_index = int(columns_index)
                middle.append(fp_location.loc[row_index]['L'])
                local_localtion.append(fp_location.columns[columns_index])
        data.append(local_localtion)
        data.append(middle)
        data.append(mean_temp_out)
        return data

class_a =A()
# data = class_a.match_location(fp_excel[0],fp_txt,fp_location)
# data2 = class_a.match_location(fp_excel[6],fp_txt,fp_location)
# e = pd.DataFrame(data=data,index=['标号','位置','外壁面温度'])
# e2 = pd.DataFrame(data=data2,index=['标号','位置','外壁面温度'])
# e3 =e.append(e2,ignore_index=True)
# print(e3)
new_data = pd.DataFrame()
for i in range(len(fp_excel)):
    f,data_P =class_a.match_P(fp_txt)
    data = class_a.match_location(fp_excel[i],fp_txt,fp_location)
    DataFrame_data = pd.DataFrame(data=data,index=['标号','位置','外壁面温度'])
    new_data = pd.concat([new_data,DataFrame_data],axis=1,ignore_index=True)
print(new_data)


