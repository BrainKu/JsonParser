__author__ = 'gzs3049'
# coding=utf-8


class SimpleParser:
    def __init__(self):
        self.pDict = dict()

    def load(self, s):
        global objdict
        index = 0
        if s[index] == '{':
            objdict, index = self.getobject(index + 1, s)
            assert objdict is not None
            for key, value in objdict:
                self.pDict[key] = value
        # elif s[index] == '[':
        # objlist, index = self.getlist(index + 1, s)
        # elif s[index] == '"':
        # string, index = self.getstring(index + 1, s)
        elif s[index] == " ":
            index += 1
        elif index >= len(s):
            raise Exception("Out of Bound")

    def getobject(self, index, string):
        global haskey, idx, key, value
        objdict = dict()
        haskey = False
        key = ""
        value = ""
        idx = index
        length = len(string)
        while 1:
            if string[idx] == '"':
                if not haskey:
                    key, idx = self.getstring(idx + 1, string)
                else:
                    value, idx = SimpleParser.getstring(idx + 1, string)
                    objdict[key] = value
            elif string[idx] == '{':
                value, idx = self.getobject(idx + 1, string)
                objdict[key] = value
            elif string[idx] == '}':
                return objdict, idx + 1
            elif string[idx] == '[':
                value, idx = self.getlist(idx + 1, string)
                objdict[key] = value
            elif "1" < string[idx] < "9":
                value, idx = self.getnumber(self, idx, string)
                objdict[key] = value
            elif string[idx] == 't':
                if idx + 4 < length and string[idx:idx + 4] == 'true':
                    value = True
                    idx += 4
                    objdict[key] = value
                raise SyntaxError("Invalid Symbole {}".format(string[idx:idx + 4]))
            elif string[idx + 1] == 'f':
                if idx + 5 < length and string[idx:idx + 5] == 'false':
                    value = False
                    idx += 5
                    objdict[key] = value
                raise SyntaxError("Invalid Symbole {}".format(string[idx:idx + 4]))
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
            elif idx == length:
                raise SyntaxError("Out of length")
            else:
                raise Exception("Exception happen in symbol{} in index {}".format(string[idx], idx))

    def getlist(self, index, string):
        global idx, obj
        length = len(string)
        idx = index
        objlist = list()
        while 1:
            if idx == length:
                raise SyntaxError("Invalid String:{}".format(string))
            elif string[idx] == ' ':
                idx += 1
            elif string[idx] == ',':
                idx += 1
            elif string[idx] == '{':
                obj, idx = self.getobject(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == '[':
                obj, idx = self.getlist(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == '"':
                obj, idx = SimpleParser.getstring(idx + 1, string)
                objlist.append(obj)
            elif string[idx] == ']':
                return objlist, idx + 1
            elif "1" <= string[idx] <= "9":
                obj, idx = self.getnumber(self, idx, string)
                objlist.append(obj)
            elif string[idx] == 't':
                if idx + 4 < length and string[idx:idx + 4] == 'true':
                    obj = True
                    idx += 4
                    objlist.append(obj)
                else:
                    raise SyntaxError("Invalid Symbol:{}".format(string[idx:idx + 4]))
            elif string[idx] == 'f':
                if idx + 4 < length and string[idx:idx + 5] == 'false':
                    obj = False
                    idx += 5
                    objlist.append(obj)
                else:
                    raise SyntaxError("Invalid Symbol:{}".format(string[idx:idx + 5]))
            elif string[idx] == 'n':
                # print string[idx:idx + 5]
                if idx + 4 < length and string[idx:idx + 4] == 'null':
                    obj = None
                    idx += 4
                    objlist.append(obj)
                else:
                    raise SyntaxError("Invalid Symbol:{}".format(string[idx:idx + 4]))
            else:
                raise SyntaxError("Invalid Symbol {} in index {}".format(string[idx], idx))

    @classmethod
    def getnumber(cls, nindex, string):
        global idx
        idx = nindex
        number = 0
        return number, idx

    @classmethod
    def getstring(cls, sindex, string):
        """转义和utf未处理"""
        global nstring, idx
        nstring = ""
        idx = sindex
        while 1:
            if string[idx] == '\\':
                idx += 1
                if idx == len(string):
                    raise SyntaxError("Invalid String")
                nextchar = string[idx]
                if nextchar == '"' or nextchar == '\\' or nextchar == '/' or nextchar == "'":
                    nstring += nextchar
                else:
                    nstring += nextchar
            elif string[idx] == '"':
                return nstring, idx + 1
            else:
                nstring += string[idx]
                idx += 1



