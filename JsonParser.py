# coding=utf-8
import json


class JsonParser():
    def __init__(self):
        self.dictcontent = dict()

    def load(self, s):
        self.scanonce(s)
        length = len(s)
        index = 1
        if s.startswith("{"):
            index, objdict = JsonParser.get_obj_dict(s, index)
            self.dictcontent["key"] = objdict
        elif s.startswith("["):
            index, objlist = self.get_obj_list(s, index)
            self.dictcontent["key"] = objlist
        elif s.startswith("\""):
            index, ss = JsonParser.get_string(s, index)


        # length = len(s)
        # if not JsonParser.check_is_object(s):
        # raise Exception("Invalid Object format")
        # s = s[1:-1]
        # values = s.split(",")
        # for value in values:
        # kv = value.split(":")
        # key = kv[0]
        # print key
        # if not JsonParser.check_is_string(key):
        # raise Exception("Invalid key")
        # key = key[1:-1]
        # value = kv[1][1:-1]
        #
        # self.dictcontent[key] = value
        self.dump()

    @classmethod
    def get_obj_dict(cls, originstr, index):
        objdict = dict()
        index += 5
        return index, objdict

    @classmethod
    def get_obj_list(cls, originstr, index):
        objlist = list()
        index += 5
        return index, objlist

    @classmethod
    def get_string(cls, originstr, index):
        index += 5
        return index, originstr

    def scanonce(self, s):
        if not s.startswith("{"):
            raise SyntaxError("")
        length = len(s)
        leftcount = 0
        leftsquare = 0
        for i in range(0, length):
            if s[i] == "t":
                if i + 3 >= length or s[i:i + 4] != "true":
                    raise SyntaxError()
            elif s[i] == "f":
                if i + 4 >= length or s[i:i + 5] != "false":
                    raise SyntaxError()
            elif s[i] == "n":
                if i + 3 >= length or s[i:i + 4] != "null":
                    raise SyntaxError()
            elif s[i] == "{":
                leftcount += 1
            elif s[i] == "[":
                leftsquare += 1
            elif s[i] == "}":
                if leftcount == 0:
                    raise SyntaxError()
                else:
                    leftcount -= 1
                    continue
            elif s[i] == "]":
                if leftsquare == 0:
                    raise SyntaxError()
                else:
                    leftsquare -= 1
                    continue

        if leftsquare != 0 or leftsquare != 0:
            raise SyntaxError()

    def dump(self):
        keys = self.dictcontent.keys()
        for key in keys:
            print "{\"",
            print key,
            print "\:"
            print "Key: {}, Value: {}".format(key, self.dictcontent[key])

    def loadJson(self, f):
        pass

    def dumpJson(self, f):
        pass

    def load_dict(self, di):
        pass

    def dump_dict(self):
        pass

    @classmethod
    def parse_value(cls, content):
        if content.startswith("\""):
            if not JsonParser.check_is_string(content):
                print "Invalid String"
            return content[1:-1]
        elif content.startswith("["):
            if not JsonParser.check_is_array(content):
                print "Invalid Array"
        elif content.startswith("{"):
            if not JsonParser.check_is_object(content):
                print "Invalid Object"

    @classmethod
    def check_is_string(cls, stringval):
        svalue = stringval.startswith("\"")
        evalue = stringval.endswith("\"")
        if not (svalue and evalue):
            return False
        return True

    @classmethod
    def check_is_number(cls, value):
        is_point_appear = False
        is_symbol_appear = False
        is_e_appear = False
        value = str(value)
        length = len(value)
        for i in range(0, length):
            if "0" <= value[i] <= "9":
                continue
            elif value[i] == "-":
                if i == 0:
                    continue
                elif i + 1 != length and value[i - 1] == "e" or value[i - 1] == "E":
                    continue
                else:
                    raise Exception("Invalid Symbol {} in wrong position".format(value[i]))
            elif value[i] == "+":
                if is_symbol_appear:
                    raise Exception("Invalid Symbol {}, {} appears twice".format(value[i]))
                elif i + 1 != length and value[i - 1] == "e" or value[i - 1] == "E":
                    continue
                else:
                    raise Exception("Invalid Symbol {} in wrong position".format(value[i]))
            elif value[i] == ".":
                if is_point_appear:
                    raise Exception("Invalid Symbol {}, {} appears twice".format(value[i]))
                elif i == 0 or i == length - 1:
                    raise Exception("Invalid Symbol {} in wrong position".format(value[i]))
                else:
                    is_point_appear = True
                    continue
            elif value[i] == "e" or value[i] == "E":
                if is_e_appear:
                    raise Exception("Invalid Symbol {}, {} appears twice".format(value[i]))
                else:
                    continue
            else:
                raise Exception("Invalid Symbol {} in position {}".format(value[i], i))
        return True

    @classmethod
    def check_value_isvalid(cls, value):
        pass

    @classmethod
    def check_is_array(cls, content):
        svalue = content.startswith("[")
        evalue = content.endswith("]")
        if not (svalue and evalue):
            return False
        else:
            return True

    @classmethod
    def check_is_object(cls, content):
        svalue = content.startswith("{")
        evalue = content.endswith("}")
        if not (svalue and evalue):
            return False
        else:
            return True

    @classmethod
    def get_string(cls, originstr):
        isfirstappear = True
        for achar in originstr:
            if achar is "/" and isfirstappear:
                pass


#
j = JsonParser()
s = '{"呵呵":"11","key2":[false, 333, 2222, {"key":"value"}]}'
# s3 = json.loads(s)
# s2 = json.dumps(s)
number = '{"number":1E10}'
print json.loads(number)
# print j.dump()
# li = list()
# li.append(2222)
# li.append("333")
# print s3
# print s3["key2"][2]
# print s2
# j.load(s)