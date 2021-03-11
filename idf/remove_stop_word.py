#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# idf文件过滤掉停用词
def remove_stop_word():
    idf_path = open('idf', 'r')
    new_path = open('idf.txt', 'w')
    stop_word = {}
    for line in open('stop_word.txt', 'r'):
        line = line.strip().split('\t')
        stop_word[line[1]] = ''
    index = 0
    for line_ in idf_path:
        line_ = line_.strip().split('\t')
        if stop_word.has_key(line_[0]):
            index += 1
            print line_[0]
        else:
            new_path.write(line_[0] + '\t' + line_[1] + '\n')
    print index
    idf_path.close()
    new_path.close()


if __name__ == '__main__':

    remove_stop_word()
