import math

import  data
import IOfile
IO_class = IOfile.IO()
data_path = 'G:\\Pythonproject\\data-processing\\learngit-master'
excel_name_list,txt_name_list,output_name_list = IO_class.Get_filename(data_path)
len_files = len(excel_name_list)
columns_name = ['位置mm','压力MPa','热导率W/(m.K)','热力含汽率','流体温度℃', \
                '流体焓值j/kg','热流密度kW/m2', \
                '上侧外壁面温度','上侧内壁面温度','上侧换热系数W/(m2.℃)', \
                '外侧外壁温温度','外侧内壁面温度','外侧换热系数W/(m2.℃)', \
                '下侧外壁面温度','下侧内壁面温度','下侧换热系数W/(m2.℃)', \
                '内侧外壁面温度','内侧内壁面温度','内侧换热系数W/(m2.℃)', \
                '平均外壁面温度','平均内壁面温度','平均换热系数W/(m2.℃)']

for i in range(len_files):
    file_name_excel = excel_name_list[i]
    file_name_txt = txt_name_list[i]
    output_name = output_name_list[i]

    fp_excel,fp_txt,fp_location =IO_class.Read_file(file_name_excel,file_name_txt)
    data_analyst = data.analyst_data(fp_excel,fp_txt,fp_location)
    del data_analyst[0]
    data_analyst.columns = columns_name
    IO_class.Output_file(output_name,data_analyst)
