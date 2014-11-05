# coding=utf-8
__author__ = 'gzs3049'
import json


# o2 = '{"key":"[value1, value2]","key2":"value3"}'
o2 = '{"key":true}'
ss = "abcdefg"
print ss[0:4] == "abcd"
s1 = json.loads(o2)
s2 = json.dumps(s1)
print s1
print s2