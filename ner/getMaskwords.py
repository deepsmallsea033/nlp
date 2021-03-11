import sys
import os
import cPickle
import codecs
import requests
sys.path.append("/data/nlp/keywordsService/")
import word_cut
reload(sys)
sys.setdefaultencoding('utf8')

def load_dict():
    f=open('/data/nlp//maskwordsService/dict.txt','r')
    dict_word={}
    for lines in f:
        line=lines.strip()
        word,tag=line.split('\t')
	if dict_word.has_key(word):
            continue
	else:
            dict_word[word]=tag

    f.close()
    return dict_word

dic_word= load_dict()#加载标注词典

def get_tags(title):
    try:
	tag_dict = {u'nr': 1, u'nz': 1, u'nt': 1, u'ns': 1}#实体词
        word_result=[]
	words = word_cut.cut(title.lower().decode('utf-8'))
	for word in set(words):
	    if dic_word.has_key(word.encode('utf-8')) and tag_dict.has_key(dic_word[word.encode('utf-8')].encode('utf-8')):
		word_result.append(word)
	return word_result
    except:
        print 'Error:get_tags', title
        return ''

def get_maskwords_service(title):	
    return_data = {
                "rspcode": 1000,
                "msg":"OK",
                "results": get_tags(title)
            }

    return return_data
if __name__ == '__main__':

    list_out=get_tags(u'张家口姚明和NBA百度燕山大学') 
    for w in list_out:
        print w 
