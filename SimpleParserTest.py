# coding=utf-8
__author__ = 'gzs3049'

import unittest
from SimpleParser import SimpleParser
import json


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.sp = SimpleParser()

    def test_load(self):
        objs = ['{"k":"v","k1":{"k1":{"k1":"v"}}, "k1":{"k1":{"k1":[123,123,false,true,null]}}}',
                '{"key":[123,123,null,false,true,"string",{"key":[123,null,false,true,"string",[false,true,null]]}]}']
        for obj in objs:
            self.sp.load(obj)
            # print self.sp.pDict
            self.assertIsNotNone(self.sp.pDict, "Load Failed!")
        global JSON
        self.sp.load(JSON)
        print self.sp.pDict

    def test_dump(self):
        objs = ['{"k1":{"k1":{"k1":"v"}}}',
                '{"k1":{"k1":{"k1":[123,123,false,true,null]}}}',
                '{"key":[123,123,null,false,true,"string",{"key":[123,null,false,true,"string",[false,true,null]]}]}']
        for obj in objs:
            self.sp.load(obj)
            self.sp.load(self.sp.dump())
            print self.sp.pDict

    def test_loadDict(self):
        d0 = {"k": "v", "k1": {"k1": {"k1": "v"}}}
        d1 = {"k": "v", 123: "value", None: "value", True: "value"}
        d2 = {(1, 2, 3): "value"}
        self.sp.loadDict(d0)
        self.assertEqual(2, len(self.sp.pDict))
        self.sp.loadDict(d1)
        self.assertEqual(1, len(self.sp.pDict))
        self.sp.loadDict(d2)
        self.assertEqual(0, len(self.sp.pDict))

    def test_dumpDict(self):
        c0 = {"k": "v", "k1": {"k1": {"k1": "v"}}}
        c1 = {"k": "v"}
        c2 = {}
        d0 = {"k": "v", "k1": {"k1": {"k1": "v"}}}
        d1 = {"k": "v", 123: "value", None: "value", True: "value"}
        d2 = {(1, 2, 3): "value"}
        self.sp.loadDict(d0)
        self.assertEqual(0, cmp(c0, self.sp.dumpDict()))
        print self.sp.dumpDict()
        self.sp.loadDict(d1)
        self.assertEqual(0, cmp(c1, self.sp.dumpDict()))
        self.sp.loadDict(d2)
        self.assertEqual(0, cmp(c2, self.sp.dumpDict()))

    def test_list(self):
        objlist = ['["abc","cde","efg",null,true,false]',
                   '["abc",["efg"]]',
                   '["abc",["abc",null,[false,  null, true]]]',
                   '[123,null,false,true,"string",{"key":[123,123,null,false,true,"string",[false,true,null]]}]']
        for obj in objlist:
            olist, index = self.sp.getlist(1, obj)
            self.assertIsNotNone(olist)
            print olist

        invalidlist = ['[,,,', '[abcdf']
        for obj in invalidlist:
            self.assertRaises(SyntaxError, self.sp.getlist, 1, obj)

    def test_object(self):
        objlist = ['{}',
                   '{"k":"v"}',
                   '{"k":"v","k1":"v"}',
                   '{"k":"v","k1":{"k1":{"k1":"v"}}}',
                   '{"k":[true, false, null]}',
                   '{"k":     null   }',
                   '{"k":1234, "kv":234}']
        for obj in objlist:
            robj, idx = self.sp.getobject(1, obj)
            self.assertIsNotNone(robj)
            print robj

    def test_number(self):
        numbers = ['12345', '-12345', '-123e10', '-123E10', '-123E-10', '10.1', '10.1e20]']
        for number in numbers:
            num, idx = self.sp.getnumber(0, number)
            print "Pair: {} : {}".format(number, num)
            self.assertIsNotNone(num)

        invalidnumbers = ['+', '-', '-1.1.1', '++033', '+333+', '0.e', 'e']
        for number in invalidnumbers:
            print number
            self.assertRaises(ValueError, self.sp.getnumber, 0, number)

    def test_string(self):
        # string = '["abcdefg", "abcd\n", "ab123"]'
        # invalidstr = ['"', '\"', "\\"]
        alist = r'["quote", "\"", "backslash", "\\"]'
        print "alist", alist
        print self.sp.getlist(1, alist)
        print "json", json.loads(alist)
        # print self.sp.getstring(1, r'"\bd"')

    def test_dump_dict(self):
        odictlist = [{"key": {"key2": True}},
                     {"k1": {"k1": {"k1": "v"}}},
                     {"key": [123, 123, 123, 123, None, False, True, "string", [False, True, None]]}]
        for odict in odictlist:
            rstring = ""
            print self.sp.dumpdict(odict, rstring)
            self.sp.load(rstring)

    def test_dump_list(self):
        objlist = [[], [123, 123, 123, 123, None, False, True, "string", [False, True, None]]]
        for olist in objlist:
            rstring = ""
            result = self.sp.dumplist(olist, rstring)
            print result
            self.sp.load(rstring)
            self.assertEqual(self.sp.dump(), rstring)

    def test_load_file(self):
        fstring = ""
        try:
            filename = "test_gbk.txt"
            with open(filename) as f:
                fstring = f.read()
        except IOError:
            print "Cannot found file ", filename
        self.sp.load(fstring)
        print self.sp.dump()

    def test_dump_file(self):
        filepath = "dump.txt"
        content = '{"key":[123,123,null,false,true,"string",{"key":[12312323,null,false,true,"string",[false,true,null]]}]}'
        self.sp.load(content)
        self.sp.dumpJson(filepath)

    def test_translate(self):
        global JSON
        print json.loads(JSON)


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
        "":  23456789012E666,
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
if __name__ == '__main__':
    unittest.main()
