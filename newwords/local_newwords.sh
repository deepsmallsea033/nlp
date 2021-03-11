#mysql -hrm-2zehfe870qi138343.mysql.rds.aliyuncs.com -udm_user -pDonews1234 -P3306 -Dnlp --default-character-set=utf8 -e "SELECT newsid,covertitle from dm_news where cat1 = 5"  > /data/wangliqi/dict/data/entertainment_title.txt


#nohup /data/anaconda2/bin/python2.7 /data/wangliqi/newwords/local_fetch_periodicly.py >> /data/wangliqi/newwords/result/local_logs.txt &
nohup /usr/bin/python2.7 /data/wangliqi/newwords/local_fetch_periodicly.py >> /data/wangliqi/newwords/result/local_logs.txt &




