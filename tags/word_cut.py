#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import jieba
import os
import re
word_map = {}

filedir = '/data/nlp/keywordsService/words_map/'
filelist = os.listdir(filedir)
for i in range(0, len(filelist)):
    path = os.path.join(filedir, filelist[i])
    file_ = open(path, 'r')
    for line in file_:
        _word = line.strip().split('\t')
        if len(_word) == 2:
            word_map[_word[0].decode('utf-8')] = _word[1].decode('utf-8')

name_dict = {}
for name in open('/data/nlp/keywordsService/words_call/dict_call.txt', 'r'):
    name = name.strip()
    if len(name) > 0:
        name_dict[name.decode('utf-8')] = ''

surname_dict = {}
for surname in open('/data/nlp/keywordsService/words_call/dict_surname.txt', 'r'):
    surname = surname.strip()
    if len(surname) > 0:
        surname_dict[surname.decode('utf-8')] = ''

def sent_cut(input_list):
    words = []
    seg_list = input_list
    if len(seg_list) > 0:
        i = 0
        while i < len(seg_list):
            if i+1 == len(seg_list):
                words.append(seg_list[i])
                break
            if surname_dict.has_key(seg_list[i]) and name_dict.has_key(seg_list[i+1]):
                words.append(seg_list[i] + seg_list[i+1])
                i += 2
            else:
                words.append(seg_list[i])
                i += 1
    return words

def cut_splicing_number(input_list):
    words = input_list
    value = re.compile(ur'^[一二三四五六七八九零十百千万亿]+$|^[-+]?[a-z]?[0-9]+[\.|%]?[0-9]?[a-z]?$')
    value_cn = re.compile(ur'^[一二三四五六七八九零十百千万亿]+$')
    out = ''
    result_list = []
    dict_tag = {'.': 1, '-': 1, '/': 1}
    CN_title = False
    for w_index,w in enumerate(words):
        result = value.match(w)
        if result:
            result_CN = value_cn.match(w)
            if result_CN:
                out += w
                CN_title =True
            elif not result_CN and CN_title:
                if len(out)>0:
                    result_list.append(out)
                    out = ''
                    out+=w
                CN_title = False
            else :
                out += w
                CN_title = False
        else:
            CN_title = False
            if len(out) > 0:
                if dict_tag.has_key(w):
                    out += w
                else:
                    result_list.append(out)
                    out = ''
                    result_list.append(w)
            else:
                result_list.append(w)

        if w_index == len(words)-1 and len(out) > 0:
            result_list.append(out)
            out = ''
    return result_list

def cut(content):
    word_list = []
    seg_list = list(jieba.cut(content))
    seg_list=cut_splicing_number(seg_list)
    seg_list = sent_cut(seg_list)
    for seg in seg_list:
        if word_map.has_key(seg):
            seg = word_map[seg]
        word_list.append(seg)

    return word_list

if __name__ == '__main__':
    list=cut('今天星期几？！各位，咱下了班儿、放了学撒丫子就奔工体！晚上见！@G_life北京')
    for w in list:
        print w

