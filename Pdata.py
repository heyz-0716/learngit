import math

import pandas as pd
import numpy as np
import data
import IOfile
from  CoolProp.CoolProp import PropsSI

IO_class = IOfile.IO()
data_path = 'D:\\pythonProject-pandastry'
excel_name_list,txt_name_list,output_name_list = IO_class.Get_filename(data_path)
file_name_txt = txt_name_list[0]
file_name_excel = excel_name_list[0]
fp_location = pd.read_table('location.txt', sep='\s+')
fp_excel = pd.read_excel(file_name_excel, sheet_name=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
fp_txt = pd.read_table(file_name_txt, sep='\t', encoding='gbk')
class_A = data.A()
# print(class_A.match_P(fp_txt)[0:2])
f,data_P , vertical_height = class_A.match_P(fp_txt)
Tf_data_Series = class_A.Tf_data(fp_txt)
index_tab = list(range(1,13))
# print(data_P)
relative_height = vertical_height/len(data_P[0])

enthalpy = list(map(lambda item:Tf_data_Series.loc['进口焓值j/kg'] + Tf_data_Series.loc['单位长度焓差j/kg.mm']*item,data_P[0]))
hf = list(map(lambda item : PropsSI('H','P',item*1e6,'Q',0,'water'),data_P[1]))
hfg = list(map(lambda item : PropsSI('H','P',item*1e6,'Q',1,'water')-PropsSI('H','P',item*1e6,'Q',0,'water'),data_P[1]))
steam_quality = list(map(lambda x,y,z: (x-y)/z,enthalpy,hf,hfg))
mass_flowrate = Tf_data_Series.loc['质量流率kg/m2.s']
Inlet_H = Tf_data_Series.loc['进口焓值j/kg']
Svolume_saratutedwater = list(map(lambda item: 1/PropsSI('D','P',item*1e6,'Q',0,'water'),data_P[1]))
Svolume_saratutedvapor = list(map(lambda item: 1/PropsSI('D','P',item*1e6,'Q',1,'water'),data_P[1]))
heat_length = Tf_data_Series.loc['加热长度mm']
relative_height = [0] + [vertical_height/len(data_P[0])]*11
# dp_between_impulse = list(map(lambda x,y:PropsSI('D','T',30+273.15,'P',x*1e6,'water')*y/1000*9.8/1000,data_P[1],relative_height))
DP = list(map(lambda  item :(data_P[1][0] - item)*1000,data_P[1]))
tem_Tf = list(map(lambda x,y: PropsSI('T','P',x*1e6,'H',y,'water')-273.15,data_P[1],enthalpy))
local_specificVolume = list(map(lambda x,y:1/PropsSI('D','P',x*1e6,'H',y,'water'),data_P[1],enthalpy))

for i in range(len(relative_height)):
    if i==0:
        relative_height[i] = 0
    else:
        relative_height[i] = relative_height[i-1]+relative_height[i]

data_frame = data_P + [enthalpy] + [steam_quality] + [Svolume_saratutedwater] +[Svolume_saratutedvapor] + [DP] +[local_specificVolume]+[relative_height]
index_label = ['位置mm','压力MPa','焓值j/kg','含汽率','饱和水比容','饱和蒸汽比容','压降kPa','当地比容','相对高度mm']
data_frame = pd.DataFrame(data_frame,index=index_label)

data_frame_liquid = data_frame.loc[:,data_frame.loc['含汽率']<0]
data_frame_twophase = data_frame.loc[:,data_frame.loc['含汽率'].between(0,1)]
data_frame_vapor = data_frame.loc[:,data_frame.loc['含汽率']>1]


def detl_P_cal(data_frame_in,mass_flowrate,status):
    initial_steam_quality = data_frame_in.loc['含汽率'][0]
    initial_height = data_frame_in.loc['相对高度mm'][0]
    intial_Specific_Volume = data_frame_in.loc['当地比容'][0]
    DPG = []
    DPA = []
    DPF = []
    for (i,j,m,n,o,p) in zip(data_frame_in.loc['相对高度mm'],data_frame_in.loc['当地比容'],data_frame_in.loc['饱和水比容'], \
                           data_frame_in.loc['饱和蒸汽比容'],data_frame_in.loc['压降kPa'],data_frame_in.loc['含汽率']):
        if status == 1: #两相区阻力计算
            middle_dpg = i/1000*9.8/(n-m)/p*math.log(1+(n-m)/m*p)/1000 - \
                         initial_height/1000*9.8/(n-m)/initial_steam_quality*math.log(1+(n-m)/m*initial_steam_quality)/1000
            middle_dpa = pow(mass_flowrate,2)*(n-m)*p/1000 - pow(mass_flowrate,2)*(n-m)*initial_steam_quality/1000
            middle_dpf = o - middle_dpg- middle_dpa
        elif status ==0: #单相液阻力计算
            middle_dpg = (i-initial_height)/1000*9.8*2/(j+intial_Specific_Volume)/1000
            middle_dpa = (j-intial_Specific_Volume)*pow(mass_flowrate,2)/1000
            middle_dpf = o - middle_dpg - middle_dpa
        elif status ==2:  #单相汽阻力计算
            middle_dpg = (i-initial_height)/1000*9.8*2/(intial_Specific_Volume+j)/1000
            middle_dpa = (j-intial_Specific_Volume)*pow(mass_flowrate,2)/1000
            middle_dpg = o - middle_dpg - middle_dpa
        DPG.append(middle_dpg)
        DPA.append(middle_dpa)
        DPF.append(middle_dpf)
    # DPG = pd.Series(DPG)
    # DPA = pd.Series(DPA)
    # DPF = pd.Series(DPF)
    DP_dataframe = pd.DataFrame([DPG,DPA,DPF],index=['DPG','DPA','DPF'])
    data_frame_in = pd.concat([data_frame_in,DP_dataframe],axis=0)
    return DPG,DPA,DPF,data_frame_in

DPG,DPA,DPF,new_data = detl_P_cal(data_frame_twophase,mass_flowrate,1)
print(new_data)
#单相液摩擦压降计算
