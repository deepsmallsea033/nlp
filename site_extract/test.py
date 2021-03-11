# -*- coding: utf-8 -*-
import extract_location_service as els



if __name__ == '__main__':
    print '*'*40
    # text = u'北京市西城区召开A级景区暑期旅游秩序整治工作座谈会'
    text = u'快讯：2017年济宁市食品安全宣传周活动在嘉祥县启动'
    # text = u'8日娱乐热点：香港女星唐宁宣布离婚，“金童玉女”难逃“七年之痒”'
    # loc_str, is_filter = filter_news_by_location(text)
    loc_str = els.extract_locations_str(text)
    print loc_str
    # for word in third_level_list:
    #     print word
    print '*'*40
