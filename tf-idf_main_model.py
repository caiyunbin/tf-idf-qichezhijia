# -*- coding: utf-8 -*-

"""

Created on Wed Aug 28 16:03:52 2019

关键词算法的主程序

@author: Administrator



"""

import math
import jieba
import jieba.posseg as psg
import glob
import numpy as np
import functools
from tf_idf_pre import slice_data  


import sys
sys.path.append('C:/Users/Administrator/Desktop/tf-idf documents')


##这一段代码是获取停用词词表位置的函数，停用词词表最好是使用自己维护的那种
def get_stopword_list():
    stop_word_path = 'C:/Users/Administrator/Desktop/month_data/stop_words.txt'
    stop_word_list = [article.replace('\n','') for article in open(stop_word_path,encoding = 'utf8').readlines()]
    return stop_word_list


#这个是对分词方法进行定义，是否按照词性进行筛选
def seg_to_list(sentence,pos = False):
    if not pos:
        #不进行词性标注的分词方法
        seg_list = jieba.cut(sentence)
    else:
        seg_list =psg.cut(sentence)
    return seg_list


#去除干扰词
def word_filter(seg_list,pos = False):
    stopword_list = get_stopword_list()
    filter_list = []
    for seg in seg_list:
        if not pos:
            word = seg
            flag = 'n'
        else:
            word =seg.word
            flag =seg.flag
        if not flag.startswith('n'): #如果想要提取形容词和名词的话可以用这个代码if not (flag.startswith('n') or flag.startswith('n')):
            continue
        if not word in stopword_list and len(word)>1:
            filter_list.append(word)
            
    return filter_list


##这个函数目前在整个程序中是没有用的，写在这里是因为有一些场景需要一个文件，一个文件中包含了很多的行，每一行是一个文件
def load_data(pos = True,corpus_path='./corpus.txt'):
    doc_list = []
    for line in open(corpus_path,'r',encoding='utf8'):
        content = line.strip()
        seg_list = seg_to_list(content,pos)
        filter_list = word_filter(seg_list,pos)
        doc_list.append(filter_list)
    return doc_list


##这一次程序使用的是这一个方法，一个文件夹中有许多的子文件
def load_doc(pos=True):
    files = glob.glob('C:/Users/Administrator/Desktop/month_data/*.txt')
    doc_list =[]
    for doc in files:
        for line in open(doc,'r',encoding='utf8'):
            content = doc.strip()
            seg_list = seg_to_list(content,pos)
            filter_list = word_filter(seg_list,pos)
            doc_list.append(filter_list)
    return doc_list


##这个函数是模型的训练函数
def train_idf(doc_list):
    idf_dic = {}
    tt_count = len(doc_list)
    for doc in doc_list:
        for word in set(doc):
            idf_dic[word] = idf_dic.get(word,0.0) + 1.0
            
    for k,v in idf_dic.items():
        idf_dic[k] = math.log(tt_count/(1.0+v))
        
    default_idf = math.log(tt_count/(1.0))
    return idf_dic,default_idf


#这个函数是一个排序函数，主要是用来处理当两个词语得分情况一样该如何进行排序
def cmp(e1,e2):
    res = np.sign(e1[1] - e2[1])
    if res != 0:
        return res
    else:
        a = e1[0] + e2[0]
        b = e2[0] + e2[0]
        if a>b:
            return 1
        elif a==b:
            return 0
        else:
            return -1


##核心的tf-idf的这个类，是进行关键词查找的核心代码
class TfIdf(object):
    def __init__(self,idf_dic,default_idf,word_list,keyword_num):
        self.word_list = word_list
        self.idf_dic,self.default_idf = idf_dic,default_idf
        self.tf_dic = self.get_tf_dic()
        self.keyword_num = keyword_num
        
    def  get_tf_dic(self):
        tf_dic = {}
        for word in self.word_list:
            tf_dic[word] = tf_dic.get(word,0.0) + 1.0
            
        tt_count = len(self.word_list)
        for k,v in tf_dic.items():
            tf_dic[k] = float(v)/tt_count
            
        return tf_dic
    
    def get_tfidf(self):
        tfidf_dic = {}
        for word in self.word_list:
            idf = self.idf_dic.get(word,self.default_idf)
            tf = self.tf_dic.get(word,0)
            
            tfidf = tf*idf
            tfidf_dic[word] = tfidf
            
        for k,v in sorted(tfidf_dic.items(),key = functools.cmp_to_key(cmp),reverse = True)[:self.keyword_num]:
            print(k + str(round(v,2)) +'/' ,end ='')
            #print(k)
        return ' '.join(k)
        print()



##模型类的实例化，传入三个参数，其中第二个参数pos默认的是关闭，第三个参数表示取多少个关键词
def tfidf_extract(word_list,pos=False,keyword_num=50):
    doc_list = load_doc(pos)
    idf_dic,default_idf =train_idf(doc_list)
    tfidf_model = TfIdf(idf_dic,default_idf,word_list,keyword_num)
    tfidf_model.get_tfidf()


##对我们月份的数据进行处理，使得每一个月份的数据变成一个字符串
def month_process(mon_dat,vaname):
    mon_dat['内容'] = mon_dat['内容'].astype(str)
    mon_dat = mon_dat['内容'].sum()
    return mon_dat
    

##依次读取文件夹中每一个月份的数据
def main():
    for names in ['January','February','March','April','May','June','July','August']:
        mon_dat = slice_data(names)               
        text = month_process(mon_dat,names)
        pos = True
        seg_list = seg_to_list(text,pos)
        filter_list = word_filter(seg_list,pos)
        print(names+'的TF-IDF模型结果:')
        tfidf_extract(filter_list)


##运行主程序
if __name__ == '__main__':
   main()











































