# -*- coding: utf-8 -*-

import sys
import requests
import MySQLdb
from parsel import Selector
#from newwords import get_new_words
from new_words import get_new_words

reload(sys)
sys.setdefaultencoding('utf8')


class NewsProcess(object):
    """ synchronize the news from cms_news to dm_news
    input: line (newsid, title, content)
    :return:
    """
    def __init__(self, data):
        self.NUM = 3  # num of input params
        if len(data) != self.NUM:
            print 'Error: length of input data is wrong.'
            return

        self.newsid = data[0]
        self.title = data[1]
	if data[2] != None:
            self.content = self.remove_tag(data[2])
	else:
	    self.content = u''
	self.newwords = u''
	
        self.conn_dm = None
        self.connect_dm_news()

        self.update_count = 0

        self.synchronize_news_single()
        self.close_dm_news()

    def remove_tag(self, parsed_content):
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

    def synchronize_news_single(self):
        """ insert/update single news """
        exist, utime_old = self.is_news_exist_in_dm_news()
	if exist:
	    self.newwords = get_new_words(self.title, self.content)
	    if self.newwords != u'':
                self.update_count += 1
                self.update_to_dm_news()
            #else:
             #   print 'newwords is null: ', self.newsid, self.title, self.newwords

    def is_news_exist_in_dm_news(self):
        cur = self.conn_dm.cursor()
        sql = "SELECT utime FROM dm_news WHERE newsid='%s' limit 1;" % self.newsid
        try:
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            if len(data) > 0:
                return True, data[0][0]
            else:
                return False, None
        except:
            print "Error: ", sql
            cur.close()
            return False, None

    def update_to_dm_news(self):
        cur = self.conn_dm.cursor()
        sql = "UPDATE dm_news set newwords = '%s' WHERE newsid = '%s';" % (self.newwords, self.newsid)
	#print sql
        try:
            cur.execute(sql)
            self.conn_dm.commit()
        except:
            print "Error: ", sql
        cur.close()

    def connect_dm_news(self):
        #self.conn_dm = MySQLdb.connect(host='rm-2zehfe870qi138343.mysql.rds.aliyuncs.com',
        self.conn_dm = MySQLdb.connect(host='10.16.5.1',
                                  user='dm_user',
                                  passwd='Donews1234',
                                  db='nlp',
                                  charset='utf8')

    def close_dm_news(self):
        if self.conn_dm:
            self.conn_dm.close()
            self.conn_dm = None

