import pandas as pd
import  numpy as np
import re
from scipy.interpolate import interp1d
import  math
from  CoolProp.CoolProp import PropsSI

class A():
    def match_P(self,fp_txt):
        a=fp_txt.mean()
        a = a.dropna(how='any')
        P = []
        vertival_height = 456
        dp_between_impulse = PropsSI('D','T',30+273.15,'P',a.loc['入口P']*1e6,'water')*9.8*vertival_height/12/1000/1000   #单位 kPa
        P.append(a.loc['入口P']-a.loc['DP1-2']/1000)  #入口压力指的是加热起始点处的压力，此处压力并没有直接测量，先用估算值
        for i in a.loc['DP1-2':'DP11-12']:
            P.append(P[-1]-i/1000-dp_between_impulse/1000)
        location_P = list(range(230,6000,520))       #引压管位置，最好也有配置文件进行配置，后续可改进
        data_P = [location_P] + [P]
        x ,y = data_P[0], data_P[1]
        f = interp1d(x, y, kind='linear')
        return  f , data_P , vertival_height

    #处理一个子excel表格里的数据，即处理的是一个工作表的内容,即形参 fp_excel 是一个dataframe，要注意
    def match_location(self,fp_excel,fp_location):
        location_numpy = fp_location.to_numpy()
        middle=[]
        local_localtion =[]
        a=fp_excel
        b=a.dropna(how='any')
        del b[0]                            #删除Time_series，因为时间序列无法算平均值
        list_num = a.iloc[0][1]             #定位，指的是第i个数据板卡
        list_num = str(list_num)
        mean_temp_out = b.mean()
        mean_temp_out = mean_temp_out.to_numpy().tolist()
        index_tab = map(lambda item: list_num + '-' + re.findall(r'\d+', item)[0], a.iloc[1].dropna(how='any'))
        for i in index_tab:
            # i = str(i)
            # i=re.findall(r"\d+",i)
            # i=list_num + '-' + ''.join(i)
            location = np.where(location_numpy == i)
            row_index = location[0]
            columns_index = location[1]
            if len(row_index) !=0:
                row_index = int(row_index)
                columns_index = int(columns_index)
                middle.append(fp_location.loc[row_index]['L'])
                local_localtion.append(fp_location.columns[columns_index])
        data = [local_localtion] + [middle] + [mean_temp_out]
        return data

    def Tf_data(self,fp_txt):
        heat_length = 6500  # 试验件的加热段长度。单位mm

        mean_data = fp_txt.mean()
        Inlet_P = mean_data.loc['入口P']
        Inlet_T = (mean_data.loc['入口T1'] + mean_data.loc['入口T2']) / 2
        Inlet_x = mean_data.loc['入口含汽率']
        Outlet_T = (mean_data.loc['出口T1'] + mean_data.loc['出口T2']) / 2
        Power = mean_data.loc['功率P']
        ther_eff = mean_data.loc['热效率']
        mass_flux = mean_data.loc['FV1'] / 60  # 单位 kg/s
        di = 0.011
        do = 0.016
        Area_cross = 1 / 4 * math.pi * pow(di, 2)
        mass_flowrate = mass_flux / Area_cross
        ther_Power = Power * ther_eff  # 加热功率 P_加热 = P *热效率 单位kW
        heat_flux = ther_Power / (math.pi * di*heat_length / 1000)  # 热流密度 单位kw/m2
        hfg = PropsSI('H', 'P', Inlet_P * 1e6, 'Q', 1, 'water') - PropsSI('H', 'P', Inlet_P * 1e6, 'Q', 0, 'water')
        hf = PropsSI('H', 'P', Inlet_P * 1e6, 'Q', 0, 'water')
        Inlet_H = Inlet_x * hfg + hf
        delt_H = ther_Power / mass_flux * 1000  # 单位 j/kg
        Outlet_H = Inlet_H + delt_H  # 单位 j/kg
        perunit_deltH = delt_H / heat_length  # 单位 j/kg.mm

        data_list = [heat_length, di, do, mass_flowrate, ther_Power, ther_eff, heat_flux, Inlet_T, Inlet_H, Outlet_T,
                     Outlet_H, delt_H, perunit_deltH, Inlet_x,Inlet_P]
        index = ['加热长度mm', '螺旋管内径mm', '螺旋管外径mm', '质量流率kg/m2.s', '加热功率kW', '热效率', '内壁面热流密度kW/m2', '进口温度℃', '进口焓值j/kg', \
                 '出口温度℃', '出口焓值j/kg', '进出口焓差j/kg', '单位长度焓差j/kg.mm','进口含汽率','入口P']
        data_series = pd.Series(data_list, index=index)
        return data_series

    def location_data_series(self,fp_excel,fp_txt,fp_location):
        class_a = A()
        #处理外壁温的所有数据，整理为一个表格
        new_data = pd.DataFrame()
        for i in range(len(fp_excel)):
            data = class_a.match_location(fp_excel[i],fp_location)
            DataFrame_data = pd.DataFrame(data=data,index=['标号','位置','外壁面温度'])
            new_data = pd.concat([new_data,DataFrame_data],axis=1,ignore_index=True)

        Tf_data_series = class_a.Tf_data(fp_txt)
        f,data_P , _ = class_a.match_P(fp_txt)
        location_ = new_data.loc['位置'].tolist()
        location_P = map(f,location_)
        location_P = pd.Series(location_P)
        new_data = new_data.append(location_P,ignore_index=True)
        new_data = new_data.sort_values(by=1,axis=1)
        columns_index = sorted(new_data.columns)
        new_data.columns =columns_index
        return new_data,Tf_data_series

def analyst_data(fp_excel,fp_txt,fp_location):
    class_a = A()
    location_data_series,Tf_data_series = class_a.location_data_series(fp_excel,fp_txt,fp_location)

    index_tab = location_data_series.iloc[0]
    location_ = location_data_series.iloc[1]
    temp_out = location_data_series.iloc[2]
    location_P = location_data_series.iloc[3]
    heat_flux = Tf_data_series['内壁面热流密度kW/m2']
    do = Tf_data_series.loc['螺旋管外径mm']
    di = Tf_data_series.loc['螺旋管内径mm']
    delt_enthalpy = Tf_data_series.loc['进出口焓差j/kg']
    perunit_deltH = Tf_data_series.loc['单位长度焓差j/kg.mm']
    Inlet_H = Tf_data_series.loc['进口焓值j/kg']

    thermal_conduc = []
    temp_in = []
    for i in temp_out:
        middle_tc = 22.69 + 0.023*i - 0.000025238*i**2      #计算热导率，后续可改进
        middle_tem = i - heat_flux*1000*di*pow(do,2)/(4*middle_tc*(pow(do,2)-pow(di,2)))*(2*math.log(do/di)+pow(di,2)/pow(do,2)-1)
        thermal_conduc.append(middle_tc)
        temp_in.append(middle_tem)
    temp_in = pd.Series(temp_in)
    thermal_conduc = pd.Series(thermal_conduc)
    location_data_series = location_data_series.append(thermal_conduc,ignore_index=True)
    location_data_series = location_data_series.append(temp_in,ignore_index=True)
    enthalpy = []
    steam_quality = []
    temp_Tf = []
    coeff_heat_transfer = []
    for i in range(len(location_)):
        middle_h = Inlet_H + perunit_deltH*location_[i]
        middle_P = location_P[i]*1e6      #单位 Pa
        hf = PropsSI('H','P',middle_P,'Q',0,'water')
        hfg = PropsSI('H','P',middle_P,'Q',1,'water') - PropsSI('H','P',middle_P,'Q',0,'water')
        middle_x = (middle_h - hf)/hfg
        middle_tf = PropsSI('T','P',middle_P,'H',middle_h,'water') - 273.15
        middle_htc = heat_flux/(temp_in[i]-middle_tf)*1000
        enthalpy.append(middle_h)
        steam_quality.append(middle_x)
        temp_Tf.append(middle_tf)
        coeff_heat_transfer.append(middle_htc)
    enthalpy = pd.Series(enthalpy)
    steam_quality = pd.Series(steam_quality)
    temp_Tf = pd.Series(temp_Tf)
    coeff_heat_transfer = pd.Series(coeff_heat_transfer)
    location_data_series = location_data_series.append(enthalpy,ignore_index=True)
    location_data_series = location_data_series.append(steam_quality,ignore_index=True)
    location_data_series = location_data_series.append(temp_Tf,ignore_index=True)
    location_data_series = location_data_series.append(coeff_heat_transfer,ignore_index=True)
    location_data_series = location_data_series.reindex([0,1,3,4,7,8,6,2,5,9])
    data_combine_A = location_data_series.loc[:,location_data_series.iloc[0] == 'A'].T
    data_combine_B = location_data_series.loc[:,location_data_series.iloc[0] == 'B'].T
    data_combine_C = location_data_series.loc[:,location_data_series.iloc[0] == 'C'].T
    data_combine_D = location_data_series.loc[:,location_data_series.iloc[0] == 'D'].T

    data_combine_A.index = list(range(len(data_combine_A.index)))
    data_combine_B.index = list(range(len(data_combine_B.index)))
    data_combine_C.index = list(range(len(data_combine_C.index)))
    data_combine_D.index = list(range(len(data_combine_D.index)))

    data_combine = pd.DataFrame()
    data_combine = pd.concat([data_combine,data_combine_A,data_combine_B.iloc[:,7:10],data_combine_C.iloc[:,7:10],data_combine_D.iloc[:,7:10]],axis=1,ignore_index=True)

    ave_temp_out = []
    ave_temp_in  = []
    ave_htc =[]
    index = data_combine.index
    for i in index:
        middle_ave_temp_out = (data_combine_A.iloc[i,7]+data_combine_B.iloc[i,7]+data_combine_C.iloc[i,7]+data_combine_D.iloc[i,7])/4
        middle_ave_temp_in  = (data_combine_A.iloc[i,8]+data_combine_B.iloc[i,8]+data_combine_C.iloc[i,8]+data_combine_D.iloc[i,8])/4
        middle_tf = data_combine_A.iloc[i,5]
        middle_ave_htc = heat_flux/(middle_ave_temp_in-middle_tf)*1000
        ave_temp_out.append(middle_ave_temp_out)
        ave_temp_in.append(middle_ave_temp_in)
        ave_htc.append(middle_ave_htc)
    ave_temp_out = pd.Series(ave_temp_out)
    ave_temp_in =pd.Series(ave_temp_in)
    ave_htc =pd.Series(ave_htc)
    data_combine = pd.concat([data_combine,ave_temp_out,ave_temp_in,ave_htc],axis=1,ignore_index=True)
    data_combine.insert(loc=7,column='热流密度kW/m2',value=heat_flux)
    return data_combine