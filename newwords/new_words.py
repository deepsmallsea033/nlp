#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import jieba
from parsel import Selector
import re

dict = {}

for line in open('/data/nlp/keywordsService/idf.txt', 'r'):
    line = line.strip().split('\t')
    if len(line) == 2:
        dict[line[0].decode('utf-8')] = ''


def segwords(content):
    wordslist = []
    seglist = jieba.cut(content.lower())
    for seg in seglist:
        if dict.has_key(seg):
            wordslist.append(seg)
    return wordslist


def extract_text(parsed_content):
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


def get_new_words(title, content):
    data = []
    words = []
    if title == None:
        return words 
    _title = extract_text(title.decode('utf-8'))
    _content = extract_text(content.decode('utf-8'))
    texts = _content + _title
    #stop_word = [u'的', u'是', u'和', u'丨']
    #w = u'#'
    #for word in stop_word:
    #	texts = texts.replace(word, w)
    for text in re.split(u'[^\u4e00-\u9fa50-9a-zA-Z]+', texts):
        data.append(text)

    newwords_map = {}
    for con in data:
        wordlist = segwords(con)
        if len(wordlist) > 0:
            #break
            newword = wordlist[0]
            for i in range(len(wordlist) - 1):
                newword += wordlist[i + 1]
                # print newword
		if not dict.has_key(newword):
                    if newwords_map.has_key(newword):
                        newwords_map[newword] += 1
                    else:
                        newwords_map[newword] = 1
                newword = wordlist[i + 1]
    newwords = sorted(newwords_map.items(), key=lambda v: v[1], reverse=True)

    #words = []
    for keys in newwords:
        if keys[0] in _title and keys[1] > 3:
            words.append(keys[0] + ':' + str(keys[1]))
    #print ','.join(words)
    return ','.join(words)


if __name__ == '__main__':
    title = u'毕竟看着这些胶原蛋白'
    content = u'含量爆表的青春美少女,暂且可以忘了自己已经是90后老阿姨的事'
    get_new_words(title, content)
    print 'Over'
