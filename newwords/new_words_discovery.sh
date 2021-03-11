#!/bin/bash

#nohup /data/anaconda2/bin/python2.7 /data/wangliqi/newwords/fetch_periodicly.py >> /data/wangliqi/newwords/words_logs.txt &
nohup /usr/bin/python2.7 /data/wangliqi/newwords/fetch_periodicly.py >> /data/wangliqi/newwords/words_logs.txt &

#nohup /data/anaconda2/bin/python2.7 /data/wangliqi/fetch_news/fetch_periodicly_copy.py >> /data/wangliqi/fetch_news/_logs.txt &


#nohup /data/anaconda2/bin/python2.7 /data/wangliqi/fetch_news/fetch_periodicly_copy1.py >> /data/wangliqi/fetch_news/logs12.txt &


#nohup python -u /data/wangliqi/newwords/update_newwords.py 2018-05-21 2018-06-21 >> 2018_05_logs.txt &
