__author__ = 'gzs3049'
# coding=utf-8

import unittest
from JsonParser import JsonParser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()

    def test_getlist(self):
        liststr = r'''[{"integer": 1234567890,
        "real": -9876.543210,
        "e": 0.123456789e-12,
        "E": 1.234567890E+34,
        "":  23456789012E666,
        "zero": 0,
        "one": 1,
        "space": " ",
        "quote": "\"",
        "backslash": "\\",
        "unicode":"\uedda",
        "controls": "\b\f\n\r\t"}]'''

        s1 = r'''["space", " ","quote"]'''
        # print json.loads(liststr)
        print self.jp.getlist(s1[1:])
        # print self.jp.getlist(s1, 1)
        # print json.dumps(data)

    def test_getlist0(self):
        liststr = r'''[{
        "quote": "\"",
        "backslash": "\\",
        "unicode":"\uedda",
        "controls": "\b\f\n\r\t"}]'''
        l = r'''["abcd",123,null,false,true,{"abc":123},[123,56,99,10000, null,false   ]]'''
        # print self.jp.getlist(liststr[1:])
        self.jp.load(JSON)
        self.jp.load(self.jp.dump())
        self.jp.load(self.jp.dump())
        print self.jp.dictcontent

    def test_getobject(self):
        obj = r'''{"abc":123,"cde":{"abc":
                {"abc":false,"abd":""}}}'''
        objfile = r'''{"china":"\u7f51\n\u6613","array":[6,"wyl",true],"null":null}'''
        # print JSON[1:2]
        # print self.jp.getobject(JSON[2:])
        # print self.jp.load(objfile)
        self.jp.load(JSON)
        import json
        # print json.loads(objfile)
        # self.jp.load(objfile)
        print self.jp.d

    def test_loadjson(self):
        self.jp.loadJson("StudentInfo.json")
        print self.jp.dump()

    def test_getchar(self):
        c = r'\ude1c'
        expected = unichr(int('de1c', 16))
        result, index = self.jp.getchar(c, 2)
        print result
        self.assertEqual(expected, result)

    def test_getstring(self):
        s0 = '"very simple"'
        e0 = 'very simple'
        s1 = r'''"`1~!@#$%^&*()_+-={':[,]}|;.</>?"'''
        e1 = r'''`1~!@#$%^&*()_+-={':[,]}|;.</>?'''
        self.assertEqual(e0, self.jp.getstring(s0[1:])[0])
        self.assertEqual(e1, self.jp.getstring(s1[1:])[0])

    def test_getfile(self):
        content = ""
        with open("StudentInfo.json") as f:
            for line in f:
                content += line
        self.jp.load(content)
        print self.jp.dump()

    def test_dumpfile(self):
        self.jp.loadJson("JSON.txt")
        self.jp.dumpJson("test.txt")

    def test_dumpDict(self):
        self.jp.loadJson("JSON.txt")
        print self.jp.dumpDict()

    def test_getnumber(self):
        s1 = r'-0.123'
        e1 = -0.123
        s2 = r'0.123456789E1'
        e2 = 1.23456789
        s3 = r'1231235234234234'
        e3 = 1231235234234234L
        s4 = r'-0'
        e4 = 0
        self.assertEqual(self.jp.getnumber(s1)[0], e1)
        self.assertEqual(self.jp.getnumber(s2)[0], e2)
        self.assertEqual(self.jp.getnumber(s3)[0], e3)
        self.assertEqual(self.jp.getnumber(s4)[0], e4)


if __name__ == '__main__':
    unittest.main()

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