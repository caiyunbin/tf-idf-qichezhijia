# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 10:33:24 2019

@author: Administrator
"""

from wordcloud import WordCloud
import cv2
import jieba
 

with open('C:/Users/Administrator/Desktop/tf-idf documents/tmp.txt','r',encoding = 'utf8') as f:
    text = f.read()
 
cut_text =" ".join(jieba.cut(text))
 
color_mask = cv2.imread('C:/Users/Administrator/Desktop/tf-idf documents/qiya.jpg')
 
cloud = WordCloud(
       #设置字体，不指定就会出现乱码
       font_path="C:/Users/Administrator/Desktop/tf-idf documents/STXINGKA.TTF",
       #font_path=path.join(d,'simsun.ttc'),
       #设置背景色
       background_color='white',
       #词云形状
       mask=color_mask,
       #允许最大词汇
       max_words=2000,
       #最大号字体
       max_font_size=40
   )
 
wCloud = cloud.generate(cut_text)
wCloud.to_file('C:/Users/Administrator/Desktop/tf-idf documents/car.jpg')
 
import matplotlib.pyplot as plt
plt.imshow(wCloud, interpolation='bilinear')
plt.axis('off')
plt.show()









