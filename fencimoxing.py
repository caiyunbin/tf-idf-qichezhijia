# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:38:27 2019

@author: Administrator
"""

import jieba
import glob
import random

'''
sent  = '中文分词是文本处理不可或缺的一步'
seg_list = jieba.cut(sent,cut_all = False)

seg_list1 = jieba.cut_for_search(sent)

print('全模式:',','.join(seg_list))

print('搜索引擎模式:',','.join(seg_list1))
'''

def get_content(path):
    with open(path,'r',encoding='GB18030',errors='ignore') as f:
        content = ''
        for line in f:
            line = line.strip()
            content += line
        return content
            

def get_TF(words,topk=10):
    tf_dic = {}
    for word in words:
        tf_dic[word] = tf_dic.get(word,0) + 1
    return sorted(tf_dic.items(),key = lambda x:x[1],reverse = True)[:topk]


def main():
    files = glob.glob('C:/Users/Administrator/Desktop/month_data/*.txt')
    corpus = [get_content(x) for x in files]
    sample_inx = random.randint(0,len(corpus))
    split_words = list(jieba.cut(corpus[sample_inx]))
    print('样本之一:'+corpus[sample_inx])
    print('样本分词效果:'+'/'.join(split_words))
    print('样本topk(10)词:'+str(get_TF(split_words)))



if __name__ == "__main__":
    main()





