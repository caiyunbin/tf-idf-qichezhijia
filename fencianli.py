# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 10:38:27 2019
这一个文档是关于如何使用jieba分词的问题,使用这一个文件是为了更好地理解jieba分词这一个库

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
def stop_words(path):
    with open(path,encoding='utf8') as f:
        return [line.strip() for line in f]
        

def get_content(path):
    with open(path,'r',encoding='utf8') as f:
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
    split_words = [x for x in jieba.cut(corpus[sample_inx]) if x not in stop_words('C:/Users/Administrator/Desktop/month_data/stop_words.txt')]
    print('样本之一:'+corpus[sample_inx])
    print('样本分词效果:'+'/'.join(split_words))
    print('样本topk(10)词:'+str(get_TF(split_words)))


if __name__ == '__main__':
    main()

    