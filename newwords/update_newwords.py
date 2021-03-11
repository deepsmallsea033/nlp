# -*- coding: utf-8 -*-

import sys
import time
import datetime
import MySQLdb
#from neologism_synchronize import NewsProcess
from local_synchronize import NewsProcess

reload(sys)
sys.setdefaultencoding('utf8')


def fetch_from_cms_news(start_date, end_date):
    time_start = time.time()
    #conn_cms = MySQLdb.connect(host='10.31.144.174', 10.174.88.196 10.80.50.170
    conn_cms = MySQLdb.connect(host='10.80.50.170',
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
        time.ctime(), str(total), str(update_count), (time.time() - time_start) / 60.0)


def update_data(start, end):
    startdate = datetime.datetime.strptime(str(start) + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
    enddate = datetime.datetime.strptime(str(end) + ' 00:00:00', "%Y-%m-%d %H:%M:%S")
    while startdate < enddate:
        start_data = startdate.strftime("%Y-%m-%d %H:%M:%S")
        end_data = (startdate + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        
	time_start = time.time()
        print startdate
        fetch_from_cms_news(start_data, end_data)
        startdate += datetime.timedelta(days=1)



if __name__ == '__main__':
    print '*' * 40
    time_start = time.time()
    _start = sys.argv[1]
    _end = sys.argv[2]

    # print _start
    # print _end
    # _start = '2017-09-09'   # sys.argv[1]
    # _end = '2017-09-10'   # sys.argv[2]
    updata_tag = "tags"
    update_data(_start, _end)
    print 'main: date: %s spend time: %s min' % (_end, (time.time() - time_start) / 60.0)


