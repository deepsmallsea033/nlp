# -*- coding: utf-8 -*-

import sys
import collections
import jieba
from getAreadic import AreaDic

reload(sys)
sys.setdefaultencoding('utf8')
AD = AreaDic()


def extract_locations(text):
    """
    Extract the locations in the input text. Return a list with definite type.
    :param text: string
    :return: [[province, city, district]]
    """
    if len(text) < 1:
        return []

    loc_list = []
    words = list(jieba.cut(text, cut_all=False))
    print ' '.join([str(c) for c in words])

    for word in words:
        if word not in AD.official_name_map:
            # 检查并去掉地名后缀
            find = False
            for p in AD.postfix_list:
                if p in word:
                    print '###', word,
                    word_new = word[:word.find(p)]
                    print word_new
                    if word_new in AD.official_name_map and len(word_new) > 0:
                        word = word_new
                        find = True
                        break
            if not find:
                continue

        # 获取官方地名。最多循环5次，防止词典错误时，不能取到官方地名
        for i in range(5):
            word = AD.official_name_map[word]
            if word == AD.official_name_map[word]:
                break
        # 省级
        if word in AD.first_level_list:
            for province in AD.loc_map[word]:
                location = [province, '', '']
                loc_list.append(location)
        # 地市级
        if word in AD.second_level_list:
            for province in AD.loc_map[word]:
                location = [province, word, '']
                loc_list.append(location)
        # 区县级
        if word in AD.third_level_list:
            for city in AD.loc_map[word]:
                for province in AD.loc_map[city]:
                    location = [province, city, word]
                    loc_list.append(location)

    # 合并去重
    loc_dict = collections.OrderedDict()
    for loc in loc_list:
        dic1 = {loc[1]: loc[2]}
        if loc[0] in loc_dict:
            dic2 = loc_dict[loc[0]]
            # 同一个市级单位下，只保留一个县级单位
            if loc[1] in dic2 and len(dic2[loc[1]]) == 0:
                dic2[loc[1]] = loc[2]
            dic1.update(dic2)

        for city in dic1.keys():
            if city == '' and len(dic1) > 1:
                dic1.pop(city)
        loc_dict[loc[0]] = dic1

    loc_list2 = []
    for k in loc_dict:
        for k_ in loc_dict[k]:
            loc_list2.append([k, k_, loc_dict[k][k_]])
    return loc_list2


def extract_locations_str(text):
    """
    Return a string with definite type.
    :param text:
    :return: str: province0#city0#district0;##;##
    """
    locations_list = extract_locations(text)
    loc_str = ''
    count = 0
    for loc in locations_list:
        count += 1
        if count > 1:
            loc_str += ';'
        loc_str += '#'.join(loc)

    return loc_str


def filter_news_by_location(text):
    """
    Filter the news that come from small town.
    :param text:
    :return:
    """
    f1 = [u'我县', u'我们县', u'县委县政府', u'县委', u'县政府', u'县城', u'自治县', u'一个县', u'县级市', u'名县']
    is_filter = False

    locations_str = extract_locations_str(text)

    # 包含小地名就过滤掉
    for f in f1:
        if f in text:
            is_filter = True
            return locations_str, is_filter

    locations_list = locations_str.strip().split(';')
    for loc in locations_list:
        term_ = loc.strip().split('#')
        if len(term_) == 3:   # 包含县级地址
            if len(term_[2]) > 0 and term_[2] not in imp_district_list:
                is_filter = True
                break

    return locations_str, is_filter


def extract_locations_service(title):
    return_data = {
                "rspcode": 1000,
                "msg": "OK",
                "results": extract_locations_str(title)
            }
    return return_data


if __name__ == '__main__':
    print '*'*40
    # text = u'北京市西城区召开A级景区暑期旅游秩序整治工作座谈会'
    text = u'快讯：2017年济宁市食品安全宣传周活动在嘉祥县启动'
    # text = u'8日娱乐热点：香港女星唐宁宣布离婚，“金童玉女”难逃“七年之痒”'
    # loc_str, is_filter = filter_news_by_location(text)
    loc_str = extract_locations_str(text)
    print loc_str
    # for word in third_level_list:
    #     print word
    print '*'*40
