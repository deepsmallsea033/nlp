#!/user/bin/env python 
# _*_coding:utf-8 _*_
import time
import math

#定义贝叶斯类
class NaiveBayseian:
    def __init__(self,ratio=0.00001):

	#计算时遇到没有在训练样本中出现的词，给一个极小值
	self.ratio=math.log(ratio)

    def train(self,train_file_path):
	#读取训练数据，训练数据按照lables,tags格式统一
	#两个字典用与存储各个类别个数及每个类别中每个词出现的次数
	self.dict_type={}
	self.dict_type_tag={}
	line_num=0
	self.num=lin_num
	f_train=open(train_file_path,'r')
	for lines in f_train:
	    self.num+=1
	    line=lines.strip().split('\t')
	    type=line[0]
	    tags=line[1]
	    if self.dict_type.has_key(type):
		dict_type[type]+=1
	    else:
		dict_type[type]=1 #记录每个类别的数据个数
		dict_type_tag[type]={} #预存每个大类
	    
	    tags=tags.split(',')
	    for tag in tags:
	        if dict_type_tag[type].has_key(tag):
		    dict_type_tag[type][tag]+=1
		else:
		    dict_type_tag[type][tag]=1

	#统计完各个类的个数，以及在各个类下每个词出现的计数，开始计算概率
	self.dict_probibly_type={} #每个类占所有类的比例
	self.dict_probibly_type_tag={} #每个词在各个类中占的比例
	for type in self.dict_type:
	    self.dict_probibly_type[type]=math.log(float(self.dict_type[type])/self.num)
	    self.dict_probibly_type_tag[type]={}
	    for tag in dict_type_tag[type]:
		self.dict_probibly_type_tag[type][tag]=math.log(float(self.dict_type_tag[type][tag])/dict_type[type])

    def save(self,model_file_path):
	f_model=open(model_file_path,'w')
	for type in self.dict_probibly_type:
	    f_model.write(type+'\t'+str(dict_probibly_type[type])+'\n')
	    for tag in self.dict_probibly_type_tag[type]:
	        f_model.write(type+'\t'+tag+'\t'+str(self.dict_probibly_type_tag[type][tag])+'\n')
	f_model.close()

    def load(self,model_path):
        self.dict_type={}
	self.dict_type_tag={}
	f_model=open(model_file_path,'r')
	for lines in f_model:
	    line=lines.strip().split('\t')
	    if len(line)==2:
		self.dict_type[line[0]]=float(line[1])
		self.dict_type_tag[line[0]]={}
	    if len(line)==3:
		self.dict_type_tag[line[0]][line[1]]=float(line[2])
	f_model.close()
	return  self.dict_type,self.dict_type_tag

    def predict(self,tags=''):
	max_value=None
	result=''

	for type in self.dict_type:
	    type_value=dict_type[type]
	    
	    for tag in tags:
		if self.dict_type_tag[type].has_key[tag]:
		    type_value+=self.dict_type_tag[type][tag]
		else:
		    type_value+=self.ratio

	    if max_value==None or max_value<type_value:
		max_value=type_value
		result=type

	return result	
