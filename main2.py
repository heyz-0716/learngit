import IOfile
import pandas as pd

test_data = pd.DataFrame(list(range(10)))
a=IOfile.IO()
a.Output_file()
excel_name_list,txt_name_list,output_name_list = a.Get_filename()
len_excelfile = len(excel_name_list)
print(len_excelfile)
for i in range(len_excelfile):
    fp_excel,fp_txt,fp_location = a.Read_file(excel_name_list[i],txt_name_list[i])
    a.Output_file(output_name_list[i],test_data,test_data,test_data)