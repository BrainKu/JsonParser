__author__ = 'gzs3049'
# coding=utf-8

from JsonParser import JsonParser
import unittest
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.jp = JsonParser()

    def test_getlist(self):
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
        obj = r'''{"abc":123,"cde":{"abc":
                {"abc":false,"abd":"","china":"\u7f51\n\u6613"}}}'''
        self.jp.load(obj)
        print self.jp.dump()
        expected = json.loads(obj)
        self.assertEqual(0, cmp(expected, self.jp.dictcontent))

    def test_loadjson(self):
        self.jp.loadJson("JSON.txt")
        with open("JSON.txt") as f:
            content = f.read()
        self.assertEqual(0, cmp(self.jp.dictcontent, json.loads(content)))
        self.jp.dumpJson("content.txt")
        with open("content.txt") as f:
            content = f.read()
        print content[580:600]
        self.jp.loadJson("content.txt")
        print self.jp.dictcontent
        print json.loads(content)

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
        with open("JSON.txt") as f:
            for line in f:
                content += line
        self.jp.load(content)
        print self.jp.dump()

    def test_dumpfile(self):
        # self.jp.loadJson("JSON.txt")
        self.jp.loadJson("Test.json")
        with open("Test1.json", "w") as outputfile:
            json.dump(json.loads(JSON), outputfile)
        self.jp.dumpJson("test.txt")

    def test_dumpDict(self):
        self.jp.loadJson("JSON.txt")
        print self.jp.dumpDict()

    def test_control(self):
        self.jp.load(JSON)
        self.jp.dumpJson("test_json.txt")
        self.jp.loadJson("test_json.txt")
        print self.jp.dictcontent

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