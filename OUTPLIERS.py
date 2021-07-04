import  pandas as pd
import  matplotlib.pyplot as plt
import scipy
import numpy as np
import pyod

# path = 'D:\\pythonProject-pandastry\\data-processing\\'
#
# file_name = path +'1-oh-2.xlsx'
# DATA_Frame = pd.read_excel(file_name,sheet_name='传热特性')
# print(DATA_Frame.head(5))
class OUTLIERS(object):

    def box_plot_outliers(self,s):
        q1,q3 = s.quantile(.25),s.quantile(.75)
        iqr = q3-q1
        low ,up = q1-1.5*iqr,q3+1.5*iqr
        outlier =s.mask((s <low)|(s>up) )
        return outlier

    def outliers(self,DATA_Frame):
        x = DATA_Frame.loc[:,'位置mm']
        y = DATA_Frame.loc[:,'平均换热系数W/(m2.℃)']
        gradient_y = np.gradient(y.values)
        gradient_y = pd.Series(gradient_y)
        outlier = self.box_plot_outliers(gradient_y)
        index = y[outlier.isna()].index
        outlier_index = []
        for i in range(len(index)-1):
            if index[i+1] -index[i] ==2:
                outlier_index.append(int((index[i+1]+index[i])/2))

        new_DATAFrame = DATA_Frame.drop(labels = outlier_index,axis=0)
        # x,y = x.drop(labels = outlier_index),y.drop(labels=outlier_index)
        # new_x = new_DATAFrame.loc[:,'位置mm']
        # new_y = new_DATAFrame.loc[:,'平均换热系数W/(m2.℃)']
        return new_DATAFrame

# print(y.drop(labels = outlier_index))
# for i in pd.isna(outlier):
#     print(i)
# print(pd.isna(outlier))
# plt.scatter(x,gradient_y)
# plt.scatter(new_x,new_y)
# plt.show()