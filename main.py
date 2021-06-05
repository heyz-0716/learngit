import math

import  data
import IOfile
IO_class = IOfile.IO()
excel_name_list,txt_name_list,output_name_list = IO_class.Get_filename()
len_files = len(excel_name_list)

for i in range(len_files):
    file_name_excel = excel_name_list[i]
    file_name_txt = txt_name_list[i]
    output_name = output_name_list[i]

    fp_excel,fp_txt,fp_location =IO_class.Read_file(file_name_excel,file_name_txt)
    data_analyst = data.analyst_data(fp_excel,fp_txt,fp_location)
    IO_class.Output_file(output_name,data_analyst)

# fp_excel = pd.read_excel(flie_name_excel, sheet_name=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
# fp_txt = pd.read_table(file_name_txt,sep='\t',encoding='gbk')
# fp_location = pd.read_table('location.txt',sep='\s+')
#
# data_analyst = data.analyst_data(fp_excel,fp_txt,fp_location)
# print(data_analyst)
