# -*- coding: utf-8 -*-
import sys
sys.path.append("/data/nlp/keywordsService/")


import word_cut
import jieba
import math
from parsel import Selector
import time

time_start = time.time()

dict_tag = {}

for line in open('/usr/lib/python2.7/site-packages/jieba/dict.txt','r'):
#for line in open('/data/wangliqi/idf/new_words.txt', 'r'):
    datas = line.strip().split(' ')
    dict_tag[datas[0].decode('utf-8')] = ''

print len(dict_tag)
word_freq = {}

def remove_tag(parsed_content):
    """Get body form html: param parsed_content: html: return: body """
    temp_lis = list()
    sel = Selector(text=parsed_content)
    ps = sel.xpath("//p")
    for p in ps:
	text = p.xpath("string(.)").extract_first()
	if not text.strip():
	    continue
	if not text.endswith((u'，', u'。', u'；', u'！', u',', u'.', u';', u'!')):
	    text = text
	temp_lis.append(text)
    return ''.join(temp_lis)


line_num = 0
for line in open('docs.txt','r'):
    line_num += 1
    if line_num % 10000 == 0:
	print line_num
    #print line.strip().lower()
    row = remove_tag(line.strip().lower().decode('utf-8'))
    seg_list = word_cut.cut(row)
    #seg_list = jieba.cut(row)
    tag_set = set(seg_list)

    for tag in tag_set:
        if dict_tag.has_key(tag):
            if word_freq.has_key(tag):
                word_freq[tag] += 1
            else:
                word_freq[tag] = 1

outfile = open('idf','w')
tag_idf = {}
for key in word_freq:
    tag_idf[key] = math.log(line_num /(word_freq[key])) 

sortedidf = sorted(tag_idf.items(), lambda x, y: cmp(x[1], y[1]))

for data in sortedidf:
    outfile.write(data[0].encode('utf-8') + '\t' + str(data[1]) + '\n')

outfile.close()
print (time.time() - time_start) / 60.0
