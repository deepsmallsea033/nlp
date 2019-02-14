#!/user/bin/env python
# _*_coding:utf-8 _*_
import numpy as np
import cv2
import os
import tensorflow as tf
import random
#定义一个类用来规范化数据
class DataSet(object):

    def __init__(self):
        index=0
	images_list=[]
	labels_list=[]
    	for root,dirs,files in os.walk('./data/t1'):
            for f in files:
                img = cv2.resize(cv2.imread(os.path.join(root, f)), (80,60))
                index+=1
                images_list.append(img)
                labels_list.append([1,0])
        for root,dirs,files in os.walk('./data/t0'):
            for f in files:
                img = cv2.resize(cv2.imread(os.path.join(root, f)), (80,60))
                index+=1
                images_list.append(img)
                labels_list.append([0,1])


    	length=len(images_list)
    	cc=list(zip(images_list,labels_list))
    	random.shuffle(cc)
    	images_list[:],labels_list[:]=zip(*cc)
    	num=int(length*0.8)
    	train_data=images_list[:num]
    	train_label=labels_list[:num]
    	test_data=images_list[num:]
    	test_label=labels_list[num:]
    	x_train=np.array(train_data)
    	x_test=np.array(test_data)
    	y_train=np.array(train_label)
    	x_train = x_train.reshape(x_train.shape[0], 60, 80, 3).astype('float32')
    	x_test = x_test.reshape(x_test.shape[0], 60, 80, 3).astype('float32')
    	x_train /= 255
	x_test /= 255

	self.test_data=x_test
        self.test_label=test_label
        self._images=x_train
	self._labels=y_train
	self._epochs_completed=0 #完成遍历数
	self._index_in_epochs=0 #调用next_batch()函数后记住上一次位置
	self._num_examples=num #训练样本数

    def next_batch(self,batch_size,fake_data=False,shuffle=True):
	start=self._index_in_epochs #记录当前位置

	if self._epochs_completed == 0 and start == 0 and shuffle:
	    index0=np.arange(self._num_examples)
	    np.random.shuffle(index0) #随机打乱序列
	    self._images=np.array(self._images)[index0] #取指定序列的部分输入数据
	    self._labels=np.array(self._labels)[index0] #取到部分输入数据对于的标签

	if start + batch_size > self._num_examples:
	    self._epochs_completed +=1
	    rest_num_examples=self._num_examples - start
	    images_rest_part=self._images[start:self._num_examples]
	    labels_rest_part=self._labels[start:self._num_examples]
	    
	    #打乱顺序
	    if shuffle:
		index=np.arange(self._num_examples)
		np.random.shuffle(index)
		self._images=self._images[index]
		self._labels=self._labels[index]
	    start =0
	    self._index_in_epochs=batch_size - rest_num_examples
	    end=self._index_in_epochs
	    images_new_part=self._images[start:end]
	    labels_new_part=self._labels[start:end]
	    return np.concatenate((images_rest_part,images_new_part),axis=0),np.concatenate((labels_rest_part,labels_new_part),axis=0)
	else:
	    self._index_in_epochs+=batch_size
	    end=self._index_in_epochs
	    return self._images[start:end],self._labels[start:end]


#****************彞~D建cnn缾Q纾\****************#
#孾Z举I位·积佇½录°
'''
conv2d佇½录°住~B录°﻾Z
input:位·积轾S佅¥潚~D佛¾佃~O
filter:位·积庠¸
strides:位·积彗¶作¨佛¾佃~O殾O䷾@维潚~D步轕¿,strides[0],strides[3]表示位·积庠¸移佊¨
­¥轕¿佒~L作¨佛¾佃~O轀~Z轁~S䷾J移佊¨步轕¿﻾Lstrides[1],strides[2]佈~F佈«表示水平溾QQ
佊¨佒~L佞~B潛´溾Q佊¨步轕¿⽀~B
padding:SAME,VALID位·积彖¹廾O﻾L位·积计签W达G秾K中same彖¹廾O彘¯补0﻾Lvalid彘¯罈~M弼
~C
use_cudnn_on_gpu:彘¯佐¦使潔¨gpu佊| 轀~_﻾L麾X认true
'''
def conv2d(x,W):
    return tf.nn.conv2d(x,W,strides=[1,1,1,1],padding='SAME')

#孾Z举I氼 佌~V佇½录°
'''
max_pool佇½录°住~B录°﻾Z
value:轜~@襾A氼 佌~V潚~D轾S佅¥
ksize:氼 佌~V栾F大対O
strides:穾W住£移佊¨潚~D步轕¿
padding:SAME,VALID位·积彖¹廾O﻾L位·积计签W达G秾K中same彖¹廾O彘¯补0﻾Lvalid彘¯罈~M弼
~C
'''
def max_pool(x):
    return tf.nn.max_pool(x,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

#佈~]妾K佌~V彝~C轇~M
def weight_variable(shape):
    initial=tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(initial)
def bias_variable(shape):
    initial=tf.constant(0.1,shape=shape)
    return tf.Variable(initial)


if __name__ == '__main__':
    
    x = tf.placeholder("float", shape=[None,60,80,3])
    y_ = tf.placeholder("float", shape=[None,2])
    sess = tf.InteractiveSession()

    #从新调整输入图像格式
    x_image=tf.reshape(x,[-1,60,80,3])

    #第一层卷积
    W_conv1=weight_variable([5,5,3,32])
    b_conv1=bias_variable([32])

    h_conv1=tf.nn.relu(conv2d(x_image,W_conv1) + b_conv1)
    h_pool1=max_pool(h_conv1)

    #第二层卷积
    W_conv2=weight_variable([5,5,32,64])
    b_conv2=bias_variable([64])

    h_conv2=tf.nn.relu(conv2d(h_pool1,W_conv2)+b_conv2)
    h_pool2=max_pool(h_conv2)

    #密集连接层连接全连接层
    W_fc1=weight_variable([15*20*64,1500])
    b_fc1=bias_variable([1500])

    h_pool2_flat=tf.reshape(h_pool2,[-1,15*20*64])
    h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat,W_fc1) + b_fc1)

    #防止过拟合引入dropout
    keep_prob = tf.placeholder("float")
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    #输出层
    W_fc2 = weight_variable([1500, 2])
    b_fc2 = bias_variable([2])

    y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    #定义交叉熵损失函数
    cross_entropy=-tf.reduce_sum(y_*tf.log(y_conv+1e-10))
    #print 'predict:%f' %y_conv
    #优化策略求取迭代步长
    train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    #accuracy
    correct_prediction=tf.equal(tf.argmax(y_conv,1),tf.argmax(y_,1)) 
    accuracy=tf.reduce_mean(tf.cast(correct_prediction,"float"))
   
    sess.run(tf.initialize_all_variables())
    
    ds = DataSet()
    for i in range(1500):
        image_batch, label_batch = ds.next_batch(50)
	#print 'value', label_batch.argmax(axis=1)
  	if i%100 == 0:
    	    train_accuracy = accuracy.eval(feed_dict={
        x:image_batch, y_: label_batch, keep_prob: 1.0})
    	    print "step %d, training accuracy %g"%(i, train_accuracy)
	train_step.run(feed_dict={x:image_batch, y_:label_batch, keep_prob: 0.5})
        output=sess.run(y_conv,feed_dict={x:image_batch, y_:label_batch, keep_prob: 1.0})
        #print 'predict',output.argmax(axis=1)
        #print '*********************************************'
    print "test accuracy %g"%accuracy.eval(feed_dict={
    x: ds.test_data, y_: ds.test_label, keep_prob: 1.0})

