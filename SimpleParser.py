__author__ = 'gzs3049'
# coding=utf-8
# from copy import deepcopy


class SimpleParser:
    def __init__(self):
        self.pDict = dict()

    def load(self, s):
        """读取json格式数据，输入s为一个json字符串，无返回值"""
        index = 0
        s.strip()
        print s
        length = len(s)
        while 1:
            if index == length:
                break
            elif s[index] == " ":
                index += 1
            elif s[index] == "\n":
                index += 1
            elif s[index] == '{':
                objdict, index = self.getobject(index + 1, s)
                self.pDict = objdict
                if index == length:  # 由于假设最外层是object，读完一个object后如果还剩下字符（包含空字符）都将报错
                    break
                else:
                    raise SyntaxError("Invalid json string:{}".format(s))
            else:
                raise ValueError("Invalid string charcter {} in position {}".format(s[index], index))
                # raise SyntaxError("Invalid string {}".format(s))

    def dump(self):
        """根据类中数据返回json字符串"""
        rstring = ""
        objdict = self.pDict
        rstring = self.dumpdict(objdict, rstring)
        return rstring

    def loadJson(self, f):
        """从文件中读入json格式数据，f为文件路径"""
        pass

    def dumpJson(self, f):
        """将类中的内容以json格式存入文件，文件若存在则覆盖，文件操作失败抛出异常"""
        try:
            with open(f, 'w') as fs:
                fs.write(self.dump())
        except IOError:
            print "File not exists: {}".format(f)

    def loadDict(self, d):
        """读取dict中的数据，存入类中，若遇到不是字符串的key则忽略"""
        self.pDict.clear()
        for key in d:
            vtype = type(key)
            if vtype is str:
                self.pDict[key] = d[key]
            else:
                continue

    def dumpDict(self):
        """返回一个字典，包含类中数据。所有字符均为unicode"""
        return self.unidict(self.pDict)

    def unidict(self, d):
        ndict = dict()
        for key in d:
            value = d[key]
            vtype = type(value)
            if vtype is str:
                ndict[unicode(key)] = unicode(value)
            elif vtype is dict:
                ndict[unicode(key)] = self.unidict(value)
            elif vtype is list:
                ndict[unicode(key)] = self.unilist(value)
            else:
                ndict[unicode(key)] = value
        return ndict

    def unilist(self, l):
        nl = list()
        for value in l:
            vtype = type(value)
            if vtype == str:
                nl.append(unicode(value))
            elif vtype == dict:
                nl.append(self.unidict(value))
            elif vtype == list:
                nl.append(self.unilist(value))
            else:
                nl.append(value)
        return nl

    def dumpdict(self, odic, string):
        isfirstobj = True
        for key in odic:
            if isfirstobj:
                isfirstobj = False
            else:
                string += ','
            string += '{"' + key + '":'
            otype = type(odic[key])
            if otype == str:
                string += '"' + odic[key] + '"'
            elif otype == dict:
                string = self.dumpdict(odic[key], string)
            elif otype == list:
                string = self.dumplist(odic[key], string)
            elif otype == bool:
                if odic[key]:
                    string += 'true'
                else:
                    string += 'false'
            elif odic[key] is None:
                string += 'null'
            else:
                string += str(odic[key])
            string += '}'
        return string

    def dumplist(self, olist, string):
        isfirstobj = True
        string += '['
        for value in olist:
            if isfirstobj:
                isfirstobj = False
            else:
                string += ','
            otype = type(value)
            if otype == str:
                string += '"' + value + '"'
            elif otype == dict:
                string = self.dumpdict(value, string)
            elif otype == list:
                string = self.dumplist(value, string)
            elif value is None:
                string += 'null'
            elif otype == bool:
                if value:
                    string += 'true'
                else:
                    string += 'false'
            else:
                string += str(value)
        string += ']'
        return string

    def getobject(self, index, string):
        global haskey, idx
        objdict = dict()
        haskey = False
        key = ""
        value = ""
        idx = index
        string.strip()
        length = len(string)
        while 1:
            if string[idx] == '"':
                if not haskey:
                    key, idx = self.getstring(idx + 1, string)
                else:
                    value, idx = self.getstring(idx + 1, string)
                    objdict[key] = value
            elif string[idx] == '{':
                value, idx = self.getobject(idx + 1, string)
                objdict[key] = value
            elif string[idx] == '}':
                return objdict, idx + 1
            elif string[idx] == '[':
                value, idx = self.getlist(idx + 1, string)
                objdict[key] = value
            elif "0" <= string[idx] <= "9" or string[idx] == '-' or string[idx] == '+':
                value, idx = self.getnumber(idx, string)
                objdict[key] = value
            elif string[idx] == 't':
                if idx + 4 < length and string[idx:idx + 4] == 'true':
                    value = True
                    idx += 4
                    objdict[key] = value
                raise ValueError("Invalid Symbole {}".format(string[idx:idx + 4]))
            elif string[idx] == 'f':
                if idx + 5 < length and string[idx:idx + 5] == 'false':
                    value = False
                    idx += 5
                    objdict[key] = value
                raise ValueError("Invalid Symbole {}".format(string[idx:idx + 4]))
            elif string[idx] == 'n':
                if idx + 4 < length and string[idx:idx + 4] == 'null':
                    value = None
                    idx += 4
                    objdict[key] = value
            elif string[idx] == ':':
                haskey = True
                idx += 1
            elif string[idx] == ' ':
                idx += 1
            elif string[idx] == ',':
                idx += 1
                haskey = False
            elif string[idx] == '\n':
                idx += 1
            elif idx == length:
                raise ValueError("Out of length")
            else:
                print string[idx:idx + 20]
                raise ValueError("Invalid symbol {} in index {}".format(string[idx], idx))

    def getlist(self, index, string):
        global idx, obj
        length = len(string)
        idx = index
        isEmpty = True
        objlist = list()
        while 1:
            if idx == length:
                raise ValueError("Invalid String:{}".format(string))
            elif string[idx] == ' ':
                idx += 1
            elif string[idx] == ',':
                idx += 1
                if idx == length or string[idx] == ']':
                    raise ValueError("Invalid comma in index {}".format(idx - 1))
            elif string[idx] == '{':
                obj, idx = self.getobject(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == '[':
                obj, idx = self.getlist(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == '"':
                obj, idx = self.getstring(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == ']':
                return objlist, idx + 1
            elif "0" <= string[idx] <= "9" or string[idx] == '-' or string[idx] == '+':
                obj, idx = self.getnumber(idx, string)
                objlist.append(obj)
            elif string[idx] == 't':
                if idx + 4 < length and string[idx:idx + 4] == 'true':
                    obj = True
                    idx += 4
                    objlist.append(obj)
                else:
                    raise ValueError("Invalid Symbol:{}".format(string[idx]))
            elif string[idx] == 'f':
                if idx + 4 < length and string[idx:idx + 5] == 'false':
                    obj = False
                    idx += 5
                    objlist.append(obj)
                else:
                    raise ValueError("Invalid Symbol:{}".format(string[idx:idx + 5]))
            elif string[idx] == 'n':
                if idx + 4 < length and string[idx:idx + 4] == 'null':
                    obj = None
                    idx += 4
                    objlist.append(obj)
                else:
                    raise ValueError("Invalid Symbol:{}".format(string[idx:idx + 4]))
            elif string[idx] == '\n':
                idx += 1
            else:
                raise ValueError("Invalid Symbol {} in index {}".format(string[idx], idx))

    def getnumber(self, nindex, string):
        idx = nindex
        isfloat = False  # 是否是浮点数
        isint = True  # 是否是整数
        haspower = False  # 是否含有幂次
        length = len(string)
        while 1:
            if idx == length or string[idx] == '}' or string[idx] == ']' or string[idx] == ',':
                if isfloat or haspower:
                    return float(string[nindex:idx]), idx
                elif isint:
                    return int(string[nindex:idx]), idx
            elif string[idx] == '.':
                if isfloat:
                    raise ValueError("Invalid symbol: {} appear for twice".format(string[idx]))
                else:
                    isfloat = True
                    idx += 1
            elif string[idx] == 'e' or string[idx] == 'E':
                if haspower:
                    raise ValueError("Invalid symbol: {} appear for twice".format(string[idx]))
                else:
                    haspower = True
                    idx += 1
            elif string[idx] == '+' or string[idx] == '-':
                if idx == nindex or string[idx - 1] == 'e' or string[idx - 1] == 'E':
                    idx += 1
                    if idx == length:
                        raise ValueError("Invalid string {}".format(string[nindex:idx], idx))
                else:
                    raise ValueError("Invalid symbol:{}".format(string[idx - 1:idx + 1]))
            elif string[idx] == "0":
                if idx != nindex:
                    continue
                else:
                    idx += 1
                    if idx < length:
                        if string[idx] == ".":
                            continue
                        else:
                            raise ValueError("Number cannot have leading zeros")
                    else:
                        raise ValueError("Number cannot have leading zeros")
            elif "1" <= string[idx] <= "9":
                idx += 1
                continue
            else:
                raise ValueError("Invalid symbol: {}".format(string[idx]))

    def getstring(self, sindex, string):
        """转义和utf未处理"""
        global nstring, idx
        nstring = ""
        idx = sindex
        length = len(string)
        while 1:
            if string[idx] == '\\':
                print string[idx]
                idx += 1
                if idx == length:
                    raise ValueError("Invalid symbol {} in index {}".format('\\', idx - 1))
                nextchar = string[idx]
                if nextchar == '"' or nextchar == '\\' or nextchar == '/' or nextchar == 'b' \
                        or nextchar == 'f' or nextchar == 'n' or nextchar == 'r' or nextchar == 't':
                    nstring += '\\' + nextchar
                    idx += 1
                    print "nstring", nstring
                else:
                    nstring += nextchar
                    idx += 1
            elif string[idx] == '"':
                return nstring, idx + 1
            elif string[idx] == '\b' or string[idx] == '\f' \
                    or string[idx] == '\n' or string[idx] == '\r' or string[idx] == '\t':
                raise ValueError("Invalid symbol {} in index {}".format(string[idx], idx))
            else:
                nstring += string[idx]
                idx += 1