# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 16:03:52 2019

@author: Administrator
"""
import math
import jieba
import jieba.posseg as psg
import glob
import numpy as np
import functools

def get_stopword_list():
    stop_word_path = 'C:/Users/Administrator/Desktop/month_data/stop_words.txt'
    stop_word_list = [article.replace('\n','') for article in open(stop_word_path,encoding = 'utf8').readlines()]
    return stop_word_list


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
        if not flag.startswith('n' or 'a'):
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
            print(k + '/',end ='')
        print()


def tfidf_extract(word_list,pos=False,keyword_num=15):
    doc_list = load_doc(pos)
    idf_dic,default_idf =train_idf(doc_list)
    tfidf_model = TfIdf(idf_dic,default_idf,word_list,keyword_num)
    tfidf_model.get_tfidf()


if __name__ == '__main__':
    text = '继不久前两艘美国海军舰艇访问香港的请求被中国拒绝后，美国防务官员称，中国又拒绝了该国一艘驱逐舰访问青岛港的请求'
    pos = True
    seg_list = seg_to_list(text,pos)
    filter_list = word_filter(seg_list,pos)
    print('TF-IDF模型结果:')
    tfidf_extract(filter_list)












































