#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: r1ngs
# contact: r1ngs@outlook.com
# datetime: 2021/4/19/0019 18:12
# software: PyCharm

import urllib.parse, socket
def dns_resolver(url):
    parse = urllib.parse.urlparse(url)
    url_new = parse.netloc
    if url_new == '':
        raise Exception('URL Format Error!')
    url_new = url_new.split(':')[0]
    #print(url_new)
    result = socket.getaddrinfo(url_new, None)
    #print(result)
    IP = result[0][4][0]

    return IP

def formatFileSize(bytes, precision):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(bytes) < 1024.0:
            return '%s %s' % (format(bytes, '.%df' % precision), unit)
        bytes /= 1024.0
    return '%s %s' % (format(bytes, '.%df' % precision), 'Yi')


# 是否超过最大大小
def maxFileSize(filesize):
    num, type = filesize.split(' ')
    if type in ['GB', 'TB', 'PB', 'EB', 'ZB']:
        return True
    elif type == 'MB':
        if float(num) > 10:
            return True
        else:
            return False
    else:
        return False

if __name__ == '__main__':
    print(dns_resolver('http://127.0.0.1:8088/MyJavaWebProject_war_exploded/index.jsp'))
