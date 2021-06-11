# # from CoolProp.CoolProp import PropsSI
# # pressure = 101325
# # temperature = 373.15
# # fld = ['acetone.fld']
# # H = PropsSI('H','P',pressure,'T',temperature,'water')
# # print(H)
# import  Tf
# file_name_txt ='1-oh-3.txt'
# data_Series = Tf.Tf_data(file_name_txt)
# print(data_Series)
import os
import re
# set_list = [
#     ({'a':1},{'a':2}),
#     ({'a':3},{'a':4})
# ]
# path = 'G:\\Pythonproject\\data-processing\\learngit-master'
# files_name = os.listdir(path)
# excel_name_list = list(filter(lambda x: re.match('.*\.xls', x) != None, files_name))
# txt_name = list(map(lambda item: item.split('.')[0]+ '.txt',excel_name_list))
# print(txt_name)

import  data
import IOfile
IO_class = IOfile.IO()
data_path = 'G:\\Pythonproject\\data-processing\\learngit-master'
excel_name_list,txt_name_list,output_name_list = IO_class.Get_filename(data_path)
len_files = len(excel_name_list)
class_A =data.A()
for i in range(1):
    file_name_excel = excel_name_list[i]
    file_name_txt = txt_name_list[i]
    output_name = output_name_list[i]

    fp_excel,fp_txt,fp_location =IO_class.Read_file(file_name_excel,file_name_txt)
    data_analyst = data.analyst_data(fp_excel,fp_txt,fp_location)
middle_data = class_A.match_location(fp_excel[0],fp_location)
a=fp_excel[0]
list_num = a.iloc[0][1]  # 定位，指的是第i个数据板卡
list_num = str(list_num)
index_tab = map(lambda item: list_num + '-' + re.findall(r'\d+', item)[0], a.iloc[1].dropna(how='any'))

f ,data_P = class_A.match_P(fp_txt)


print(data_analyst)

# location_x_equal_0 = []
# if steam_quality[0]<0:
#     detla_enthalpy = hf[0] - Inlet_H
#     length_x_equal_0 = detla_enthalpy/Tf_data_Series.loc['单位长度焓差j/kg.mm']
#     location_x_equal_0.append(length_x_equal_0)
# else:
#     location_x_equal_0.append(data_P[0][0])
#
# location_x_equal_1 = []
# Outlet_steam_quality = steam_quality[-1]
# if Outlet_steam_quality >1:
#     detla_enthalpy = hfg[-1]+hf[-1] - Inlet_H
#     length_x_equal_1 = detla_enthalpy/Tf_data_Series.loc['单位长度焓差j/kg.mm']
#     location_x_equal_1.append(length_x_equal_1)
# else:
#     location_x_equal_1.append([0])
#
# relative_liquid_height = []
# for (i,j) in zip(steam_quality,data_P[0]):
#     if steam_quality[0]<0:
#         if i <0:
#             middle_height = j-data_P[0][0]
#         elif i>0:
#             middle_height = location_x_equal_0 - data_P[0][0]
#     else:
#         middle_height =0
#     relative_liquid_height.append(middle_height)
#
# relative_twophase_height = []
# for (i,j) in zip(steam_quality,data_P[0]):
#     if i >0 and i <1:
#         middle_height = j - location_x_equal_0[0]
#     elif i>1:
#         middle_height = location_x_equal_1[0] - location_x_equal_0[0]
#     elif i<0:
#         middle_height = 0
#     relative_twophase_height.append(middle_height)
#
# relative_vapor_height = []
# for (i,j) in zip(steam_quality,data_P[0]):
#     if i>1:
#         middle_height = j-location_x_equal_1[0]
#     else:
#         middle_height = 0
#     relative_vapor_height.append(middle_height)
#
# relative_liquid_height = relative_liquid_height / heat_length * vertical_height / 1000
# relative_twophase_height = relative_twophase_height / heat_length *vertical_height/1000
# relative_vapor_height = relative_vapor_height/heat_length*vertical_height/1000
# DPG_liquid =