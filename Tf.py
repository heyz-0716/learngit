import pandas as pd
from CoolProp.CoolProp import PropsSI
import math

def Tf_data(fp_txt):
    # fp_txt = pd.read_table(file_name_txt,sep='\t',encoding='gbk')
    heat_length = 6500      #试验件的加热段长度。单位mm

    mean_data = fp_txt.mean()
    Inlet_P = mean_data.loc['入口P']
    Inlet_T = (mean_data.loc['入口T1']+mean_data.loc['入口T2'])/2
    Inlet_x = mean_data.loc['入口含汽率']
    Outlet_T = (mean_data.loc['出口T1']+mean_data.loc['出口T2'])/2
    Power = mean_data.loc['功率P']
    ther_eff = mean_data.loc['热效率']
    mass_flux = mean_data.loc['FV1']/60   #单位 kg/s
    di = 0.011
    do = 0.016
    Area_cross = 1/4*math.pi *pow(di,2)
    mass_flowrate = mass_flux/Area_cross
    ther_Power = Power*ther_eff     #加热功率 P_加热 = P *热效率 单位kW
    heat_flux = ther_Power/(math.pi*heat_length/1000)   #热流密度 单位kw/m2
    hfg = PropsSI('H','P',Inlet_P*1e6,'Q',1,'water')-PropsSI('H','P',Inlet_P*1e6,'Q',0,'water')
    hf = PropsSI('H','P',Inlet_P*1e6,'Q',0,'water')
    Inlet_H = Inlet_x*hfg +hf
    delt_H = ther_Power/mass_flux*1000   #单位 j/kg
    Outlet_H = Inlet_H + delt_H          #单位 j/kg
    perunit_deltH = delt_H/heat_length   #单位 j/kg.mm

    data_list = [heat_length,di,do,mass_flowrate,ther_Power,ther_eff,heat_flux,Inlet_T,Inlet_H,Outlet_T,Outlet_H,delt_H,perunit_deltH]
    index = ['加热长度mm','螺旋管内径mm','螺旋管外径mm','质量流率kg/m2.s','加热功率kW','热效率','内壁面热流密度kW/m2','进口温度℃','进口焓值j/kg',\
             '出口温度℃','出口焓值j/kg','进出口焓差j/kg','单位长度焓差j/kg.mm']
    data_series = pd.Series(data_list,index=index)
    return data_series