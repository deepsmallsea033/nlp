# -*- coding: utf-8 -*-

import sys
import codecs
import collections

reload(sys)
sys.setdefaultencoding('utf8')


class AreaDic(object):

    def __init__(self):
        # 词频越高，后续jieba分词越容易分词：标准官方地名设置为高词频；其他设置为低词频。
        self.WORD_FREQ_HIGH = 1
        self.WORD_FREQ_LOW = 1

        self.official_name_map = collections.OrderedDict()  # 记录官方名字对照表
        self.loc_map = collections.OrderedDict()    # 记录该地名的上一级地名
        self.loc_dic_fenci = collections.OrderedDict()  # 记录全国县以上的地名
        self.first_level_list = list()  # 一级行政单位
        self.second_level_list = list()  # 二级行政单位
        self.third_level_list = list()  # 三级行政单位
        self.postfix_list = []  # 机构单位
        self.imp_district_list = []  # 区、县
        self.get_cn_locations()
        self.get_postfix()
        self.get_imp_district()

    def get_cn_locations(self):
        file_cnlocations = codecs.open('/data/wangliqi/site_extract/input/cn_locations_original.txt', 'a+', 'utf-8')
        fi1e_city = codecs.open('/data/wangliqi/site_extract/input/city_byname.txt', 'a+', 'utf-8')

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

        for line in file_cnlocations.readlines():
            count += 1
            term = line.strip().split()
            if len(term) == 0:
                is_new_provence = True
                continue

            if is_new_provence:
                # 初始化下一个省份的dic
                k_pro = term[0]
                is_new_provence = False

                if k_pro not in self.loc_dic_fenci:
                    self.loc_dic_fenci[k_pro] = str(self.WORD_FREQ_HIGH)
                    self.loc_map[k_pro] = [k_pro]
                    self.first_level_list.append(k_pro)
                else:
                    prev = self.loc_map[k_pro]
                    prev.append(k_pro)
                    self.loc_map[k_pro] = list(set(prev))

                self.official_name_map[k_pro] = k_pro
                # 创建关联的所有省级名称
                for p in province_level:
                    if p in k_pro:
                        pro_new = k_pro[:k_pro.find(p)]
                        self.official_name_map[pro_new] = k_pro  # 记录官方名字
                        if pro_new not in self.loc_dic_fenci:
                            self.loc_dic_fenci[pro_new] = str(self.WORD_FREQ_HIGH)  # 记录行政单位级别
                            self.loc_map[pro_new] = [k_pro]
                            self.first_level_list.append(pro_new)
                        else:
                            prev = self.loc_map[pro_new]
                            prev.append(k_pro)
                            self.loc_map[pro_new] = list(set(prev))
            else:
                term2 = line.strip().split(':')
                city = term2[0]
                if len(term2) > 1:
                    district = term2[1].strip().split(' ')
                else:
                    district = []

                self.official_name_map[city] = city
                # 创建关联的所有市级单位名称;添加市级单位的上级地名
                if city not in self.loc_dic_fenci:
                    self.loc_dic_fenci[city] = str(self.WORD_FREQ_HIGH)
                    self.loc_map[city] = [k_pro]
                    self.second_level_list.append(city)
                else:
                    prev = self.loc_map[city]
                    prev.append(k_pro)
                    self.loc_map[city] = list(set(prev))

                for p in city_level:
                    if p in city:
                        city_new = city[:city.find(p)]
                        if city_new in filter_list:  # 去掉过滤表中的地名简称
                            continue

                        self.official_name_map[city_new] = city
                        if city_new not in self.loc_dic_fenci:
                            self.loc_dic_fenci[city_new] = str(self.WORD_FREQ_HIGH)
                            self.loc_map[city_new] = [k_pro]
                            self.second_level_list.append(city_new)
                        else:
                            prev = self.loc_map[city_new]
                            prev.append(k_pro)
                            self.loc_map[city_new] = list(set(prev))

                # 添加区县级单位的上级地名
                for dis in district:
                    if dis not in self.loc_dic_fenci:
                        self.loc_dic_fenci[dis] = str(self.WORD_FREQ_HIGH)
                        self.loc_map[dis] = [city]
                        self.third_level_list.append(dis)
                    else:
                        prev = self.loc_map[dis]
                        prev.append(city)
                        self.loc_map[dis] = list(set(prev))

                    self.official_name_map[dis] = dis
                    # 对于重点城市，名称列表精确到区县
                    if city in top_city_list:
                        for p in distric_level:
                            if p in dis and len(dis) > 2:
                                dis_new = dis[:dis.find(p)]
                                if dis_new in filter_list:  # 去掉过滤表中的地名简称
                                    continue

                                self.official_name_map[dis_new] = dis
                                if dis_new not in self.loc_dic_fenci:
                                    self.loc_dic_fenci[dis_new] = str(self.WORD_FREQ_LOW)
                                    self.loc_map[dis_new] = [city]
                                    self.third_level_list.append(dis_new)
                                else:
                                    prev = self.loc_map[dis_new]
                                    prev.append(city)
                                    self.loc_map[dis_new] = list(set(prev))

        # 将城市别名加入列表中
        for line in fi1e_city.readlines():
            term = line.strip().split()
            if len(term) == 2:
                self.official_name_map[term[0]] = term[1]
                self.loc_dic_fenci[term[0]] = str(self.WORD_FREQ_LOW)

        print len(self.loc_dic_fenci), len(self.loc_map)

        file_cnlocations.close()
        fi1e_city.close()

    def get_postfix(self):
        file_postfix = codecs.open('/data/wangliqi/site_extract/input/locations_postfix.txt', 'r+', 'utf-8')
        for line in file_postfix.readlines():
            term = line.strip().split()
            self.postfix_list.append(term[0])

    def get_imp_district(self):
        file_district = codecs.open('/data/wangliqi/site_extract/input/imp_district_list.txt', 'r+', 'utf-8')
        for line in file_district.readlines():
            term = line.strip().split()
            if len(term) == 1 and len(term[0]) > 0:
                self.imp_district_list.append(term[0])

    if __name__ == '__main__':
        print ''
