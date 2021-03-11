#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms -e "SELECT title, contenttext  from cms_news_detail WHERE datavalid = 1 and newsid > 200000 limit 10"  > /data/wangliqi/idf/test.txt

#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms --default-character-set=utf8 -e "SELECT title, content from cms_news,cms_news_detail where cms_news.newsid = cms_news_detail.newsid and utime >1522166400 and newsmode = 1 and channelidnew = 9"  > /data/wangliqi/opsql/data/news_detail_2018328_2018428.txt &


#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms -e "SELECT title, contenttext  from cms_news_detail WHERE datavalid = 1 and newsid >= 10000000 and newsid < 19769516"  > /data/wangliqi/idf/text_10000000_19769516.txt &


#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms --default-character-set=utf8 -e "SELECT keywords from cms_news WHERE length(keywords) > 0"  > /data/wangliqi/opsql/data/keywords.txt &


#mysql -hrm-2zehfe870qi138343.mysql.rds.aliyuncs.com -udm_user -pDonews1234 -P3306 -Dnlp --default-character-set=utf8 -e "SELECT newsid,covertitle from dm_news where utime > 1534953600 and covertitle like '%妈妈%' limit 20000"  > /data/wangliqi/newwords/title_20000.txt &


mysql -h10.16.5.1 -udm_user -pDonews1234 -P3306 -Dnlp --default-character-set=utf8 -e "SELECT newsid,newwords,covertitle from dm_news where length(newwords) > 0 and utime >=1615219200  and utime < 1615305600"  > /data/wangliqi/newwords/online_result/newsid_title_newwords_2021-03-10.txt
