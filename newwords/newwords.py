#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from collections import defaultdict  # defaultdict是经过封装的dict，它能够让我们设定默认值
from math import log
import re

dict = {}
#for line in open('/data/anaconda2/lib/python2.7/site-packages/jieba/dict.txt' ,'r'):
for line in open('/usr/lib/python2.7/site-packages/jieba/dict.txt' ,'r'):
    line = line.strip().split(' ')
    if len(line) == 2:
        dict[line[0].decode('utf-8')] = ''

stop_word = [u'的', u'是', u'和', u'丨', u'在']

def texts(db):
    for a in db:
        yield a


class Find_Words:

    def __init__(self, min_count=1, min_pmi=0.0):
        self.min_count = min_count
        self.min_pmi = min_pmi
        self.chars, self.pairs = defaultdict(int), defaultdict(int)
        self.total = 0.

    # 预切断句子，以免得到太多无意义（不是中文、英文、数字）的字符串
    def text_filter(self, texts):
	line_arr = []
	w = u'#'

	for line in texts:
	    for word in stop_word:
		line = line.replace(word, w)
	    line_arr.append(line)

	for a in line_arr:
            # 这个正则表达式匹配的是任意非中文、非英文、非数字，因此它的意思就是用任意非中文、非英文、非数字的字符断开句子
            for t in re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', a):
                if t:
                    yield t

    # 计数函数，计算单字出现频数、相邻两字出现的频数
    def count(self, texts):
        for text in self.text_filter(texts):
            self.chars[text[0]] += 1
            for i in range(len(text)-1):
                self.chars[text[i+1]] += 1
                self.pairs[text[i:i+2]] += 1
                self.total += 1
        self.pairs_score={}
        #最少频数过滤
        self.chars = {i: j for i, j in self.chars.items() if j >= self.min_count}
        self.pairs = {i: j for i, j in self.pairs.items() if j >= self.min_count}
        
        self.strong_segments = set()

        # 根据互信息找出比较“密切”的邻字
        for i, j in self.pairs.items():
            _ = log(self.total*j/(self.chars[i[0]]*self.chars[i[1]]))
            self.pairs_score[i]=_
            if _ >= self.min_pmi:
                self.strong_segments.add(i)

    # 根据前述结果来找词语
    def find_words(self, texts):
        self.words = defaultdict(int)
        # 左邻字、右邻字
        self.words_left = defaultdict(int)
        self.words_right = defaultdict(int)

        for text in self.text_filter(texts):
            s = text[0]
            for i in range(len(text)-1):
                # 如果比较“密切”则不断开
                if text[i:i+2] in self.strong_segments:
                    s += text[i+1]
		    if i+1 == len(text)-1:
			self.words[s] += 1
                        if len(s) > 1 and i+1-len(s) > 0:
                            self.words_left[text[i+1-len(s)], s] += 1

                # 否则断开，前述片段作为一个词来统计
                else:
                    self.words[s] += 1

                    if len(s) > 1 and i+1-len(s) > 0:
                        self.words_left[text[i - len(s)], s] += 1

                    if len(s) > 1 and i+1-len(s) >= 0:
                        self.words_right[s, text[i+1]] += 1

                    s = text[i+1]
		    if i+1 == len(text)-1:
			self.words[s] += 1

    # 计算左右信息熵
    def new_words(self):
        self.result = defaultdict(int)

        for words in self.words.items():
            if len(words[0]) > 1:

                l_value = 0.0
                for wl in self.words_left.items():
                    if words[0] == wl[0][1]:
                        pwl = wl[1] / float(words[1])
                        l_value -= pwl * log(pwl)

                r_value = 0.0
                for wr in self.words_left.items():
                    if words[0] == wr[0][1]:
                        pwr = wr[1] / float(words[1])
                        r_value -= pwr * log(pwr)

                # 左右信息熵取较小值
                w_value = min(l_value, r_value)
                if w_value > 0:
                    self.result[words[0]] = words[1]


def get_new_words(title, content):
    data = []
    try:
        title = title.lower()
        content = content.lower()
    except:
        print("lower error")
    if title or content:
	data.append(title)
	data.append(content)
    fw = Find_Words(3, 1.0)
    fw.count(texts(data))
    fw.find_words(texts(data))
    fw.new_words()
    # 添加书名号中的词作为候选新词
    rex_words = re.findall(u"(?<=《).*?(?=》)", title)
    if len(rex_words) > 0:
        for rex_w in rex_words:
            if len(rex_w) < 10:
                rex_ = re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', rex_w)[0]
                if rex_ in fw.result:
                    fw.result[rex_] += 3
                else:
                    fw.result[rex_] = 4
            
    new_words = []
    #words = sorted(fw.words.items(), key=lambda v: v[1], reverse=True)
    words = sorted(fw.result.items(), key=lambda v: v[1], reverse=True)
    for keys in words:
        if len(keys[0]) > 1 and keys[1] > 3:
            if not dict.has_key(keys[0]):
		if keys[0] in title:
                    new_words.append(keys[0] + ':' + str(keys[1]))
    
    return ','.join(new_words)
