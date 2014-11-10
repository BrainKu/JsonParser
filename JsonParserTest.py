# coding=utf-8
__author__ = '郑鑫伟'

from JsonParser import JsonParser
import unittest
import json

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
        file_path = "output.txt"
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
            self.assertEqual(0, cmp(self.jp.dictcontent, json.loads(s)))

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
        self.assertEqual(0, cmp(self.jp.dictcontent, json.loads(content)))

    def test_dumpJson(self):
        with open("Test1.json", "w") as outputfile:
            json.dump(json.loads(JSON), outputfile)
        self.jp.dumpJson("test.txt")

    def test_loadDict(self):
        d1 = {"abc": 123, 123: "abc", False: "test", None: 123}
        e1 = {"abc": 123}
        self.jp.loadDict(d1)
        self.assertEqual(0, cmp(e1, self.jp.dictcontent))

    def test_dumpDict(self):
        pass

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

    # def test_control(self):
    # global JSON
    # self.jp.load(JSON)
    # self.jp.dumpJson("test_json.txt")
    # self.jp.loadJson("test_json.txt")
    # print self.jp.dictcontent

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


if __name__ == '__main__':
    unittest.main()

