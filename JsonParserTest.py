# coding=utf-8
__author__ = '郑鑫伟'

from JsonParser import JsonParser
import json
import unittest
import copy

# from http://json.org/JSON_checker/test/pass1.json and add chinese symbol
JSON = r'''
{"key":[
    "JSON Test Pattern pass1",
    {"object with 1 member":["array with 1 element"]},
    {},
    [],
    -42,
    true,
    false,
    null,
    {
        "integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E6,
        "中文":"字符串",
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "controls": "\b\f\n\r\t",
        "slash": "/ & \/",
        "alpha": "abcdefghijklmnopqrstuvwyz",
        "ALPHA": "ABCDEFGHIJKLMNOPQRSTUVWYZ",
        "digit": "0123456789",
        "special": "`1~!@#$%^&*()_+-={':[,]}|;.</>?",
        "hex": "\u0123\u4567\u89AB\uCDEF\uabcd\uef4A",
        "true": true,
        "false": false,
        "null": null,
        "array":[  ],
        "object":{  },
        "address": "50 St. James Street",
        "url": "http://www.JSON.org/",
        "comment": "// /* <!-- --",
        "# -- --> */": " ",
        " s p a c e d " :[1,2 , 3

,

4 , 5        ,          6           ,7        ],
        "compact": [1,2,3,4,5,6,7],
        "jsontext": "{\"object with 1 member\":[\"array with 1 element\"]}",
        "quotes": "&#34; \u0022 %22 0x22 034 &#x22;",
        "\/\\\"\uCAFE\uBABE\uAB98\uFCDE\ubcda\uef4A\b\f\n\r\t`1~!@#$%^&*()_+-=[]{}|;:',./<>?"
: "A key can be any string"
    },
    0.5 ,98.6
,
99.44
,

1066


,"rosebud"]
}
'''


class JsonParserTest(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()
        self.maxDiff = None

    def test_main(self):
        file_path = "output1.json"
        a1 = JsonParser()
        a2 = JsonParser()
        a3 = JsonParser()

        # test_json_str、test_dict
        a1.load(JSON)
        d1 = a1.dumpDict()
        # 粗糙比较test_dict和d1

        a2.loadDict(d1)
        a2.dumpJson(file_path)
        a3.loadJson(file_path)
        d3 = a3.dumpDict()
        # 比较d1和d3是否完全一样
        self.assertEqual(d1, d3)

    def test_load(self):
        slist = [r'''{}''',
                 r'''{"abc":123}''',
                 r'''{"abc":{"abc":{"abc":123}}}''',
                 r'''{"abc":{"abc":{"abc":[123,234,567,null,false,true,[]]}}}''']
        for s in slist:
            self.jp.load(s)
            self.assertEqual(self.jp.dictcontent, json.loads(s))

    def test_dump(self):
        slist = [r'''{}''',
                 r'''{"abc":123}''',
                 r'''{"abc":{"abc":{"abc":123}}}''',
                 r'''{"abc":{"abc":{"abc":[123,234,567,null,false,true,[]]}}}''']
        for s in slist:
            self.jp.load(s)
            self.assertEqual(self.jp.dump(), s)

    def test_loadJson(self):
        self.jp.loadJson("JSON.txt")
        with open("JSON.txt") as f:
            content = f.read()
        self.assertEqual(self.jp.dictcontent, json.loads(content))  # 比较使用标准库和JsonParser加载相同字符串结果是否相同

    def test_dumpJson(self):
        output = "output2.json"
        self.jp.load(JSON)
        self.jp.dumpJson(output)
        first = copy.deepcopy(self.jp.dictcontent)  # 创建一个原字典的拷贝
        with open(output) as f:
            content = f.read()
        self.jp.load(content)
        self.assertEqual(first, self.jp.dictcontent)

    def test_loadDict(self):
        d1 = {"abc": 123, 123: "abc", False: "test", None: 123}
        e1 = {"abc": 123}
        self.jp.loadDict(d1)
        self.assertEqual(e1, self.jp.dictcontent)

    def test_dumpDict(self):
        d1 = r'''{"abc": 123, "bcd": false, "cde": null}'''
        self.jp.load(d1)
        # dumpDict返回的字典跟原字典具有相同的键值，但是不是同一个对象
        self.assertEqual(self.jp.dictcontent, self.jp.dumpDict())
        self.assertFalse(self.jp.dictcontent is self.jp.dumpDict())

    def test_getitem(self):
        d = {"abc": "cde", "cde": "abc"}
        self.jp.loadDict(d)
        key = "abc"
        value = "cde"
        self.assertEqual(value, self.jp[key])

    def test_setitem(self):
        d = {"abc": "cde", "cde": "abc"}
        self.jp.loadDict(d)
        key = "abc"
        expected = "abcdefg"
        self.jp[key] = expected
        self.assertEqual(expected, self.jp[key])

    def test_update(self):
        d = {"abc": "cde", "cde": "abc"}
        d1 = {"abc": "abc", "cde": "cde"}
        self.jp.loadDict(d)
        self.jp.update(d1)
        self.assertEqual("abc", self.jp["abc"])
        self.assertEqual("cde", self.jp["cde"])

    def test_deepdump(self):
        d0 = {"a": 123}
        d1 = {"b": d0}
        d2 = {"c": [d1]}
        d3 = self.jp.deepdump(d2)  # 深拷贝对象
        d3['c'][0]['b']['a'] = 234  # 修改拷贝后嵌套对象中的值
        self.assertEqual(d2['c'][0]['b']['a'], 123)  # 断言原本对象的值未改变

    def test_getnumber(self):
        s1 = r'-0.123'
        e1 = -0.123
        s2 = r'0.123456789E1'
        e2 = 1.23456789
        s3 = r'1231235234234234'
        e3 = 1231235234234234L
        s4 = r'-0'
        e4 = 0
        s5 = r'-0.0e+1'
        e5 = -0.0
        self.assertEqual(self.jp.getnumber(s1)[0], e1)
        self.assertEqual(self.jp.getnumber(s2)[0], e2)
        self.assertEqual(self.jp.getnumber(s3)[0], e3)
        self.assertEqual(self.jp.getnumber(s4)[0], e4)
        self.assertEqual(self.jp.getnumber(s5)[0], e5)

    def test_getchar(self):
        c = r'\ude1c'
        expected = unichr(int('de1c', 16))
        result, index = self.jp.getchar(c, 2)
        self.assertEqual(expected, result)

    def test_getstring(self):
        s0 = '"very simple"'
        e0 = 'very simple'
        s1 = r'''"`1~!@#$%^&*()_+-={':[,]}|;.</>?"'''
        e1 = r'''`1~!@#$%^&*()_+-={':[,]}|;.</>?'''
        self.assertEqual(e0, self.jp.getstring(s0[1:])[0])
        self.assertEqual(e1, self.jp.getstring(s1[1:])[0])

    def test_getarray(self):
        liststr = r'''{"key":[{"integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E6,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "unicode":"\uedda",
        "controls": "\b\f\n\r\t"}]}'''
        self.jp.load(liststr)
        expected = json.loads(liststr)
        self.assertEqual(0, cmp(expected, self.jp.dictcontent))

    def test_getobject(self):
        self.jp.load(JSON)
        expected = json.loads(JSON)
        self.assertEqual(0, cmp(expected, self.jp.dictcontent))

    def test_final(self):
        for tub in finaljson:
            self.jp.load(tub[0])
            assert self.jp.dictcontent[tub[1]] == tub[2]
            print tub[1], tub[2]


if __name__ == '__main__':
    unittest.main()

finaljson = [
    ('{"a":123}', "a", 123),  # 数字
    ('{"a":"hello"}', "a", "hello"),  # 字符串
    ('{"a":"\\t\\t\\n"}', "a", "\t\t\n"),  # tab和换行
    ('{"a": 1e1}', "a", 10),  # 数字
    ('{"a": "\\u6709\\u611f\\u800c\\u53d1\\u3002\\u3002"}', "a", u"\u6709\u611f\u800c\u53d1\u3002\u3002"),  # unicode
    ('{"a  ": 123}', "a  ", 123),  # 空格和tab
    ('{ "a" : 123    	}', "a", 123),  # 空格和tab
    ('{"a":[1,2,3]}', "a", [1, 2, 3]),  # 数组
    ('{"a":[1,2,"aaa"]}', "a", [1, 2, "aaa"]),  # 数组
    ('{"a": "a\\\\"}', "a", "a\\"),  # 反斜杠
    ('{"d{": "}dd"}', "d{", "}dd"),  # {}
    ('{"d,": ",dd", "a": [1,2,3]}', "d,", ",dd"),  # ,
    ('{"d\\\"": "\\\"dd", "a": [1,2,3]}', "d\"", "\"dd"),  # "
    ('{"a": {"a": {"a": 123}}}', "a", {"a": {"a": 123}}),  # 嵌套
    ('{"a": {"a": {"a": 123, "b": [1,2,3]}}}', "a", {"a": {"a": 123, "b": [1, 2, 3]}}),  # 嵌套
    ("""
{ "ab{" : "}123", "\\\\a[": "]\\\\", "cc": 123 }
""", "cc", 123),  # 复杂类型
]

