#!/usr/bin/env python
#encoding: utf-8
from .settings import MEDIA_ROOT
import base64
import time
import datetime
from django.utils import timezone

def mk_md5(s):
    import hashlib
    salt = "HlameHastar"
    obj = hashlib.md5(salt.encode('utf-8'))
    obj.update(s.encode('utf-8'))
    return obj.hexdigest()


def now():
    return time.strftime('%Y-%m-%d %X', time.localtime() )

def str2datetime(str,delay=0):
    '''字符串转datetime，delay为延迟时间，单位秒'''
    return datetime.datetime.strptime(str, "%Y-%m-%d %X") + datetime.timedelta(seconds=delay)

def timeTrans(during):
    import datetime
    now = datetime.datetime.now()
    if during == "day":
        res = now - datetime.timedelta(1)
    if during == "week":
        res = now - datetime.timedelta(7)
    if during == "month":
        res = now - datetime.timedelta(30)
    if during == "year":
        res = now - datetime.timedelta(365)
    if during == "all":
        res = now - datetime.timedelta(9999)
    return res

def save_image(filename,base64_data):
    """将base64数据转换为图片并写入上传路径,增加时间戳防止文件覆盖"""
    filename += "_" + str(time.time())
    with open(MEDIA_ROOT / filename, "wb") as f:
        byte_data = base64.b64decode(base64_data.split("data:image/jpeg;base64,")[1])
        f.write(byte_data)
    return filename
