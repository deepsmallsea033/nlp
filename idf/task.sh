#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms -e "SELECT title, contenttext  from cms_news_detail WHERE datavalid = 1 and newsid > 200000 limit 10"  > /data/wangliqi/idf/test.txt

#mysql -h10.80.50.170 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms --default-character-set=utf8 -e "SELECT title, content from cms_news_detail WHERE datavalid = 1 and newsid >= 138000000 and newsid < 140433627"  > /data/wangliqi/idf/text_138000000_140433627.txt

mysql -h10.16.5.1 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms --default-character-set=utf8 -e "SELECT title, content from cms_news_detail WHERE datavalid = 1 and newsid >= 160125439 and newsid < 161664374"  > /data/wangliqi/idf/text_160125439_161664374.txt


#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms -e "SELECT title, contenttext  from cms_news_detail WHERE datavalid = 1 and newsid >= 10000000 and newsid < 19769516"  > /data/wangliqi/idf/text_10000000_19769516.txt &


#mysql -h10.31.144.174 -uniuerhot_sf_r -pdonewsRsfQWERYhaSED -P3306 -Ddevdonewscms -e "SELECT title, contenttext  from cms_news_detail WHERE datavalid = 1 and newsid >= 19769516 and newsid < 28218795"  > /data/wangliqi/idf/text_19769516_28218795.txt &

