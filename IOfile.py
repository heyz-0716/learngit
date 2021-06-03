
import  os
import re
import pandas as pd

#获取数据文件夹底下的excel表格名以及txt文件名，并形成读入文件名列表和输出文件名列表
class IO(object):

    def Get_filename(self):
        path = 'D:\\pythonProject-pandastry\\'
        files_name = os.listdir(path)
        excel_name_list = list(filter(lambda x: re.match('.*\.xls', x) != None, files_name))
        txt_name_list=[]
        output_name_list =[]
        for i in excel_name_list:
            txt_name = i.split('.')[0] + '.txt'
            txt_name_list.append(txt_name)
            output_name = i.split('.')[0] + '-data.xlsx'
            output_name_list.append(output_name)
        return excel_name_list,txt_name_list,output_name_list

    def Read_file(self,file_name_excel,file_name_txt):
        fp_location = pd.read_table('location.txt', sep='\s+')
        fp_excel = pd.read_excel(file_name_excel, sheet_name=[0, 1, 2, 3, 4, 5, 6, 7], header=None)
        fp_txt = pd.read_table(file_name_txt, sep='\t', encoding='gbk')
        return fp_excel,fp_txt,fp_location

    def Output_file(self,output_name,data1,data2,data3):
        dir_name = './data-processing'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        file_path = dir_name+'/' + output_name
        data1.to_excel(file_path,sheet_name='流体数据')
        data2.to_excel(file_path,sheet_name='传热特性')
        data3.to_excel(file_path,sheet_name='流动阻力特性')



