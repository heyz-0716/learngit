
import  data
import IOfile
import pandas as pd
IO_class = IOfile.IO()
data_path = 'G:\\Pythonproject\\data-processing\\learngit-master'
excel_name_list,txt_name_list,output_name_list = IO_class.Get_filename(data_path)
len_files = len(excel_name_list)

output_DataFrame = pd.DataFrame()
for i in range(len(excel_name_list)):
    file_name_excel = excel_name_list[i]
    file_name_txt = txt_name_list[i]
    output_name = output_name_list[i]

    fp_excel,fp_txt,fp_location =IO_class.Read_file(file_name_excel,file_name_txt)
    class_A = data.A()
    Tf_data_Series = class_A.Tf_data(fp_txt)
    a = fp_excel[0].dropna(how='any')
    output_Series = [a.iloc[0, 0], Tf_data_Series.loc['入口P'], Tf_data_Series.loc['质量流率kg/m2.s'],
                     Tf_data_Series.loc['内壁面热流密度kW/m2'], \
                     Tf_data_Series.loc['进口含汽率']]
    output_Series = pd.Series(output_Series)
    output_DataFrame = pd.concat([output_DataFrame,output_Series],axis=1,ignore_index=True)
output_DataFrame = output_DataFrame.sort_values(by=0,axis=1)
output_DataFrame.T.to_excel('Time_Series.xlsx')