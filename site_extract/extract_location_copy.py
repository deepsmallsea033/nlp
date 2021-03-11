# -*- coding: utf-8 -*-

import sys
import codecs
import collections
import jieba

reload(sys)
sys.setdefaultencoding('utf8')


# 词频越高，后续jieba分词越容易分词：标准官方地名设置为高词频；其他设置为低词频。
WORD_FREQ_HIGH = 1
WORD_FREQ_LOW = 1

# 记录全国县以上的地名
loc_dic_fenci = collections.OrderedDict()
# 上级行政区划映射表
loc_map = collections.OrderedDict()
# 一级行政区：省、直辖市、自治区、特别行政区
first_level_list = list()
# 二级行政区：市、自治州
second_level_list = list()
# 三级行政区：区、县
third_level_list = list()
# 行政区官方名字映射表
official_name_map = collections.OrderedDict()
# 机构单位
postfix_list = []
# 区、县
imp_district_list = []


def get_locations_dic():
    file_cnlocations = codecs.open('D:/dic/work/code/diming/input/cn_locations_original.txt', 'a+', 'utf-8')
    fi1e_city = codecs.open('D:/dic/work/code/diming/input/city_byname.txt', 'a+', 'utf-8')
    file_postfix = codecs.open('D:/dic/work/code/diming/input/locations_postfix.txt', 'r+', 'utf-8')
    file_district = codecs.open('D:/dic/work/code/diming/input/imp_district_list.txt', 'r+', 'utf-8')

    province_level = [u'省', u'自治区', u'直辖市', u'特别行政区', u'市']
    city_level = [u'市', u'地区', u'朝鲜族自治州', u'土家族苗族自治州',
          u'藏族羌族自治州', u'藏族自治州', u'彝族自治州', u'布依族苗族自治州',
          u'苗族侗族自治州', u'哈尼族彝族自治州', u'壮族苗族自治州', u'傣族自治州',
          u'白族自治州', u'傈僳族自治州', u'回族自治州', u'蒙古族藏族自治州', u'蒙古自治州',
          u'柯尔克孜自治州', u'哈萨克自治州']
    distric_level = [u'区', u'县']

    # 列表中的词具有强烈的指代作用，不宜作为地名简称
    filter_list = [u'阿里', u'和平', u'北海']
    # top city的地名简称精确到区县
    top_city_list = [u'北京市', u'上海市', u'深圳市', u'杭州市', u'天津市', u'香港特别行政区', u'澳门特别行政区']

    is_new_provence = True
    k_pro = None
    count = 0

    for line in file_postfix.readlines():
        term = line.strip().split()
        postfix_list.append(term[0])

    for line in file_district.readlines():
        term = line.strip().split()
        if len(term) == 1 and len(term[0]) > 0:
            imp_district_list.append(term[0])

    for line in file_cnlocations.readlines():
        # print count, line
        count += 1

        term = line.strip().split()
        if len(term) == 0:
            is_new_provence = True
            continue

        if is_new_provence:
            # 初始化下一个省份的dic
            k_pro = term[0]
            is_new_provence = False

            if k_pro not in loc_dic_fenci:
                loc_dic_fenci[k_pro] = str(WORD_FREQ_HIGH)
                loc_map[k_pro] = [k_pro]
                first_level_list.append(k_pro)
            else:
                prev = loc_map[k_pro]
                prev.append(k_pro)
                loc_map[k_pro] = list(set(prev))

            official_name_map[k_pro] = k_pro
            # 创建关联的所有省级名称
            for p in province_level:
                if p in k_pro:
                    pro_new = k_pro[:k_pro.find(p)]
                    official_name_map[pro_new] = k_pro  # 记录官方名字
                    if pro_new not in loc_dic_fenci:
                        loc_dic_fenci[pro_new] = str(WORD_FREQ_HIGH)  # 记录行政单位级别
                        loc_map[pro_new] = [k_pro]
                        first_level_list.append(pro_new)
                    else:
                        prev = loc_map[pro_new]
                        prev.append(k_pro)
                        loc_map[pro_new] = list(set(prev))

        else:
            term2 = line.strip().split(':')
            city = term2[0]
            if len(term2) > 1:
                district = term2[1].strip().split(' ')
            else:
                district = []

            official_name_map[city] = city
            # 创建关联的所有市级单位名称;添加市级单位的上级地名
            if city not in loc_dic_fenci:
                loc_dic_fenci[city] = str(WORD_FREQ_HIGH)
                loc_map[city] = [k_pro]
                second_level_list.append(city)
            else:
                prev = loc_map[city]
                prev.append(k_pro)
                loc_map[city] = list(set(prev))

            for p in city_level:
                if p in city:
                    city_new = city[:city.find(p)]
                    if city_new in filter_list:  # 去掉过滤表中的地名简称
                        continue

                    official_name_map[city_new] = city
                    if city_new not in loc_dic_fenci:
                        loc_dic_fenci[city_new] = str(WORD_FREQ_HIGH)
                        loc_map[city_new] = [k_pro]
                        second_level_list.append(city_new)
                    else:
                        prev = loc_map[city_new]
                        prev.append(k_pro)
                        loc_map[city_new] = list(set(prev))

            # 添加区县级单位的上级地名
            for dis in district:
                if dis not in loc_dic_fenci:
                    loc_dic_fenci[dis] = str(WORD_FREQ_HIGH)
                    loc_map[dis] = [city]
                    third_level_list.append(dis)
                else:
                    prev = loc_map[dis]
                    prev.append(city)
                    loc_map[dis] = list(set(prev))

                official_name_map[dis] = dis
                # 对于重点城市，名称列表精确到区县
                if city in top_city_list:
                    for p in distric_level:
                        if p in dis and len(dis) > 2:
                            dis_new = dis[:dis.find(p)]
                            if dis_new in filter_list:  # 去掉过滤表中的地名简称
                                continue

                            official_name_map[dis_new] = dis
                            if dis_new not in loc_dic_fenci:
                                loc_dic_fenci[dis_new] = str(WORD_FREQ_LOW)
                                loc_map[dis_new] = [city]
                                third_level_list.append(dis_new)
                            else:
                                prev = loc_map[dis_new]
                                prev.append(city)
                                loc_map[dis_new] = list(set(prev))

    # 将城市别名加入列表中
    for line in fi1e_city.readlines():
        term = line.strip().split()
        if len(term) == 2:
            official_name_map[term[0]] = term[1]
            loc_dic_fenci[term[0]] = str(WORD_FREQ_LOW)

    # print len(loc_dic_fenci), len(loc_map)

    file_cnlocations.close()
    fi1e_city.close()
    file_district.close()
    file_postfix.close()


get_locations_dic()


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
        if word not in official_name_map:
            # 检查并去掉地名后缀
            find = False
            for p in postfix_list:
                if p in word:
                    print '###', word,
                    word_new = word[:word.find(p)]
                    print word_new
                    if word_new in official_name_map and len(word_new) > 0:
                        word = word_new
                        find = True
                        break
            if not find:
                continue

        # 获取官方地名。最多循环5次，防止词典错误时，不能取到官方地名
        for i in range(5):
            word = official_name_map[word]
            if word == official_name_map[word]:
                break
        # 省级
        if word in first_level_list:
            for province in loc_map[word]:
                location = [province, '', '']
                loc_list.append(location)
        # 地市级
        if word in second_level_list:
            for province in loc_map[word]:
                location = [province, word, '']
                loc_list.append(location)
        # 区县级
        if word in third_level_list:
            for city in loc_map[word]:
                for province in loc_map[city]:
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
    locations_str = ''
    count = 0
    for loc in locations_list:
        count += 1
        if count > 1:
            locations_str += ';'
        locations_str += '#'.join(loc)

    return locations_str


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


def test_getAreaname():
    fi = codecs.open('D:/dic/work/code/services/area.txt', 'r+', 'utf-8')
    fo = codecs.open('D:/dic/work/code/services/area_location.txt', 'w+', 'utf-8')

    for line_ in fi.readlines():
        term_ = line_.strip().split('\t')
        if len(term_) == 3:
            loc_str3 = extract_locations_str(term_[1])
            fo.write(term_[0] + '\t' + term_[1] + '\t' + loc_str3 + '\n')
    fi.close()
    fo.close()


if __name__ == '__main__':
    print '*'*40
    # # text = u'北京市西城区召开A级景区暑期旅游秩序整治工作座谈会'
    # text = u'8日娱乐热点：香港女星唐宁宣布离婚，“金童玉女”难逃“七年之痒”'
    text = u'快讯：2017年济宁市食品安全宣传周活动在嘉祥县启动'
    # loc_str, is_filter = filter_news_by_location(text)
    loc_str = extract_locations_str(text)
    print loc_str
    # test_getAreaname()
    print '*'*40
