# -*- coding: utf-8 -*-

import sys
import time
import datetime
import MySQLdb
from neologism_synchronize import NewsProcess

reload(sys)
sys.setdefaultencoding('utf8')


def fetch_from_cms_news(start_date, end_date):
    t1 = time.time()
    #conn_cms = MySQLdb.connect(host='10.31.144.174', 10.174.88.196 10.80.50.170
    #conn_cms = MySQLdb.connect(host='10.80.50.170',
    conn_cms = MySQLdb.connect(host='10.16.5.1',
                               user='niuerhot_sf_r',
                               passwd='donewsRsfQWERYhaSED',
                               db='devdonewscms',
                               charset='utf8')

    cur = conn_cms.cursor()
    sql = "select cms_news.newsid, covertitle, content \
           from cms_news, cms_news_detail \
           where cms_news.newsid = cms_news_detail.newsid \
           and utime > (SELECT UNIX_TIMESTAMP('%s')) and utime <= (SELECT UNIX_TIMESTAMP('%s')) \
           and (newsmode > 0) and online = 1;" % (start_date, end_date)
    #print sql
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    if conn_cms:
        conn_cms.close()

    total = len(data)
    update_count = 0

    # single process
    for line in data:
        NP = NewsProcess(line)
	update_count += NP.update_count
        
    print "%s | total: %s update: %s | spend time: %s min" % (
          time.ctime(), str(total), str(update_count), (time.time() - t1) / 60.0)


def periodicly_fetch():
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    curtime_p = datetime.datetime.strptime(cur_time, "%Y-%m-%d %H:%M:%S")
    start_time = (curtime_p + datetime.timedelta(minutes=-60)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = (curtime_p + datetime.timedelta(minutes=-30)).strftime("%Y-%m-%d %H:%M:%S")
    print end_time
    print start_time
    fetch_from_cms_news(start_time, end_time)


if __name__ == '__main__':
    print '*'*40
    #time1 = time.time()

    periodicly_fetch()
    print '*'*40

    #print 'main: %s spend time: %s min' % (time.ctime(), (time.time() - time1) / 60.0)

