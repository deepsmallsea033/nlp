# _*_ coding:utf-8 _*_

import word_cut
import math

idf_set = set()
idf_dict = {}
word_map = {u'县', u'乡', u'镇'}

for idf_line in open('/data/nlp/keywordsService/idf.txt','r'):
    idf_word=idf_line.strip().split('\t')
    idf_dict[idf_word[0].decode('utf-8')] = float(idf_word[1])
    

def get_keywords(title, article, k):
    keywords_tfidflist=calculate_tfidf(title, article)
    sorted_tfidf = sorted(keywords_tfidflist.items(),key=lambda v: v[1],reverse=True)   
    k = min(len(sorted_tfidf), k)
    return sorted_tfidf[0:k]


def calculate_tfidf(title, content = ''):
    words_frq = {}
    tmp_list = {}
    get_wordtmp(title, content, tmp_list)
    get_tffrq(title, 3, words_frq, tmp_list)
    get_tffrq(content,1 , words_frq, tmp_list)

    tfidf = {}

    sum = 0
    for word in words_frq:
        sum += words_frq[word]
    square = 0.0
    for word in words_frq:        
        tfidf[word] = idf_dict[word] * float(words_frq[word]) / sum
        square += tfidf[word] * tfidf[word]
    for word in tfidf:
        tfidf[word] = round(tfidf[word] / math.sqrt(square),4)

    return tfidf


def get_tffrq(content = '', weight = 1, frq = {}, tmp_list = {}):
    seg_list = word_cut.cut(content.lower())
    for seg in seg_list:
        if idf_dict.has_key(seg):
            if tmp_list.has_key(seg):
                seg = tmp_list[seg]
            if frq.has_key(seg):
                frq[seg] += weight
            else:
                frq[seg] = weight


def get_wordtmp(title = '', content = '', tmp_list = {}):
    seg_list = word_cut.cut((title + '\t' + content).lower())
    for seg in seg_list:
        if idf_dict.has_key(seg):
            for key in word_map:
                if seg.endswith(key):
                    w = seg[:seg.find(key)]
                    if len(w) > 1:
                        tmp_list[w] = seg


def get_keywords_service(title,article,k):	
    return_data = {
                "rspcode": 1000,
                "msg":"OK",
                "results": get_keywords(title,article,k)
            }
    return return_data				

