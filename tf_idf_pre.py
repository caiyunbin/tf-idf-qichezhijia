# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 14:45:13 2019

这个文件是把excel表格中的词语转变成以月为单位的文档合集

@author: Administrator
"""

from datetime import datetime
import pandas as pd


def slice_data(yuefen):
    #读取了数据将列名进行了修改
    data= pd.read_csv('C:/Users/Administrator/Desktop/文件集合/qichedata1.csv',encoding='GB18030',names=['汽车代号','ID','日期','帖子类型','内容'])
    #去除数据的重复行
    data = data.drop_duplicates()
    data['日期'] = pd.to_datetime(data['日期'])
    #一年中的八个月份
    if yuefen == 'January':
        January = data[(data["日期"]>= datetime(2019,1,1)) & (data["日期"]<= datetime(2019,1,31))]
        return January
    elif yuefen == 'February':
        February = data[(data["日期"]>= datetime(2019,2,1)) & (data["日期"]<= datetime(2019,2,28))]
        return February
    elif yuefen == 'March':
        March = data[(data["日期"]>= datetime(2019,3,1)) & (data["日期"]<= datetime(2019,3,31))]
        return March
    elif yuefen == 'April':
        April  = data[(data["日期"]>= datetime(2019,4,1)) & (data["日期"]<= datetime(2019,4,30))]
        return April
    elif yuefen == 'May':
        May = data[(data["日期"]>= datetime(2019,5,1)) & (data["日期"]<= datetime(2019,5,31))]
        return May
    elif yuefen == 'June':
        June = data[(data["日期"]>= datetime(2019,6,1)) & (data["日期"]<= datetime(2019,6,30))]
        return June
    elif yuefen == 'July':
        July  = data[(data["日期"]>= datetime(2019,7,1)) & (data["日期"]<= datetime(2019,7,31))]
        return July
    else:
        August = data[(data["日期"]>= datetime(2019,8,1)) & (data["日期"]<= datetime(2019,8,31))]
    return August 
    

def get_variable_name(x)->str:
    for k,v in locals().items():
        if v is x:
            return k

  
def month_apply(month_dat,v_name):
    month_dat['内容'] = month_dat['内容'].astype(str)
    month_dat = month_dat['内容'].sum()
    path = 'C:/Users/Administrator/Desktop/month_data/'+ v_name +'.txt'
    with open(path, "w", encoding='utf-8') as f:
        f.write(month_dat)


    
    
def main():
    for v_name in ['January','February','March','April','May','June','July','August']:
        yuefen = slice_data(v_name)               
        month_apply(yuefen,v_name)
        
if __name__ == '__main__':
    main()






