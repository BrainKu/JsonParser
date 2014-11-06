# coding=utf-8
import json


class JsonParser():
    def __init__(self):
        self.d = dict()

    def load(self, s):
        s = s.strip()
        pass

    def getobject(self, string, index):
        objdict = dict()
        haskey = False
        key = ""
        idx = index + 1
        length = len(string)
        while 1:
            if idx == length:
                raise ValueError("Out of length")
            elif string[idx] == '"':
                if not haskey:
                    key, idx = self.getstring(string, idx)
                else:
                    value, idx = self.getstring(string, idx)
                    objdict[key] = value
            elif string[idx] == ',':
                idx += 1
                haskey = False
            elif string[idx] == '{':
                value, idx = self.getobject(string, idx)
                objdict[key] = value
            elif string[idx] == '[':
                value, idx = self.getlist(string, idx)
                objdict[key] = value
            elif "0" <= string[idx] <= "9" or string[idx] == '-':
                value, idx = self.getnumber(string, idx)
                objdict[key] = value
            elif string[idx] == '}':
                return objdict, idx + 1
            elif string[idx] == ':':
                haskey = True
                idx += 1
                continue
            else:
                obj, idx = self.getspecialvalue(string, idx)
                objdict[key] = obj
            print string[idx:idx + 20]
            raise ValueError("Invalid symbol {} in index {}".format(string[idx], idx))

    def getlist(self, string, index):
        string = string.strip()
        objlist = list()
        hasvalue = False  # 记录逗号分割符出现时是否已有值被载入
        onetime = True  # 左括号是否出现了一次
        idx = index + 1
        length = len(string)
        while 1:
            if idx == length:
                if onetime:
                    break
                else:
                    return objlist, idx
            elif string[idx] == ' ':
                idx += 1
                continue
            elif string[idx] == ',':
                if hasvalue:
                    idx += 1
                else:
                    raise ValueError("Invalid array with empty value before index {}".format(idx))
            elif string[idx] == '[':
                value, idx = self.getlist(string, idx + 1)
                objlist.append(value)
                hasvalue = True
            elif string[idx] == '{':
                value, idx = self.getobject(string, idx + 1)
                objlist.append(value)
                hasvalue = True
            elif string[idx] == '"':
                value, idx = self.getstring(string, idx + 1)
                objlist.append(value)
                hasvalue = True
            elif "0" <= string[idx] <= "9" or string[idx] == "-":
                value, idx = self.getnumber(string, idx)
                objlist.append(value)
                hasvalue = True
            elif string[idx] == ']':
                if onetime:
                    return objlist, idx + 1
                else:
                    raise ValueError("Invalid list end in index {}".format(idx))
            else:
                value, idx = self.getspecialvalue(string, idx)
                objlist.append(value)
                hasvalue = True
        raise ValueError("Invalid list with no close ]")

    def getspecialvalue(self, string, index):
        length = len(string)
        idx = index
        if string[idx] == 't':
            if idx + 4 < length and string[idx:idx + 4] == 'true':
                obj = True
                return obj, idx + 4
            else:
                raise ValueError("Invalid Symbol:{}".format(string[idx]))
        elif string[idx] == 'f':
            if idx + 5 < length and string[idx:idx + 5] == 'false':
                obj = False
                return obj, idx + 5
            else:
                raise ValueError("Invalid Symbol:{}".format(string[idx:idx + 5]))
        elif string[idx] == 'n':
            if idx + 4 < length and string[idx:idx + 4] == 'null':
                obj = None
                return obj, idx + 4
            else:
                raise ValueError("Invalid Symbol:{}".format(string[idx:idx + 4]))
        else:
            raise ValueError("Invalid Symbol:{}".format(string[idx]))


    def getnumber(self, string, index):
        iszerofirst = False
        hasdot = False
        haspower = False
        length = len(string)
        idx = index
        # 先检查是否含有前导0和负号
        if string[idx] == '0':
            iszerofirst = True
            idx += 1
        elif string[idx] == '-':
            if idx == length or string[idx] == ']' or string[idx] == '}' \
                    or string[idx] == ',' or string[idx] == ' ':
                raise ValueError("Invalid number with only -")
            else:
                idx += 1
            if string[idx] == '0':
                iszerofirst = True
                idx += 1
            elif '1' <= string[idx] <= '9':
                pass
            else:
                raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))
        else:
            pass
        if iszerofirst:
            if idx == length or string[idx] == ']' or string[idx] == '}' \
                    or string[idx] == ',' or string[idx] == ' ':
                return 0, idx
            elif string[idx] != '.' and string[idx] != 'e' and string[idx] != 'E':  # 前导0后面跟的如果不是.，E，e中的其中一个则不合法
                raise ValueError("Invalid number with leading zero {}".format(string[idx]))
            else:
                pass
        while 1:
            if idx == length or string[idx] == ']' or string[idx] == '}' or string[idx] == ',':
                if hasdot or haspower:
                    return float(string[index:idx]), idx
                else:
                    return int(string[index:idx]), idx
            elif string[idx] == '.':
                if hasdot:
                    raise ValueError("Invalid number with double dot")
                else:
                    hasdot = True
                    idx += 1
                    continue
            elif string[idx] == 'E' or string[idx] == 'e':  # 幂标志只能出现一次且不能出现在结尾
                if haspower:
                    raise ValueError("Invalid number with double power")
                else:
                    haspower = True
                    idx += 1
                    if self.__checkisend(string, idx):
                        raise ValueError("Invalid number with symbol {} in index {}".format(string[idx - 1], idx))
                    else:
                        continue
            elif string[idx] == '+' or string[idx] == '-':
                if string[idx - 1] != 'E' and string[idx - 1] != 'e':
                    raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))
                else:
                    idx += 1
                    if self.__checkisend(string, idx):  # 单独的E-或者E+也是不合法的
                        raise ValueError("Invalid number with symbol {} in index {}".format(string[idx - 1], idx))
                    continue
            elif '0' <= string[idx] <= '9':
                idx += 1
                continue
            else:
                raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))


    def __checkisend(self, string, idx):
        length = len(string)
        if idx == length or string[idx] == '}' or string[idx] == ']' or string[idx] == ',':
            return True
        else:
            return False


    def getstring(self, string, index):
        """Get string 传入时默认是以双引号开头的"""
        idx = index + 1
        nstring = ""
        length = len(string)
        hassinglequote = True
        while 1:
            if idx == length:
                if hassinglequote:
                    break
                else:
                    return nstring, idx + 1  # JSON允许空字符串
            elif string[idx] == '\\':
                idx += 1
                if idx == length:
                    break
                elif string[idx] == 'u':  # Get unicode char
                    curchar, idx = self.getchar(string, idx + 1)
                    nstring += '\\u' + curchar
                elif string[idx] == '"':
                    nstring += '\\\"'
                    idx += 1
                elif string[idx] == '\\':
                    nstring += '\\\\'
                    idx += 1
                elif string[idx] == '/' or string[idx] == 'b' \
                        or string[idx] == 'f' or string[idx] == 'n' \
                        or string[idx] == 'r' or string[idx] == 't':  # Get control symbol
                    nstring += '\\' + string[idx]
                    idx += 1
                else:
                    raise ValueError("Invalid escapse")  # Invalid escapse
            elif string[idx] == '"':
                if hassinglequote:  # 再遇到一个双引号则返回
                    return nstring, idx + 1  # 返回取出字符串之后的下标
                else:
                    hassinglequote = True
                    idx += 1
            else:
                if hassinglequote:  # 之前出现了一个引号则添加字符
                    nstring += string[idx]
                    idx += 1
                elif string[idx] == ' ':
                    idx += 1
                else:
                    raise ValueError("Invalid string does not start with double quotes")
        raise ValueError("Invalid string with no close \"")


    def getchar(self, string, index):
        """Get unicode char"""
        length = len(string)
        if index + 3 >= length:
            raise ValueError("Invalid unicode string {}".format(string[index:length]))
        idx = 0
        while idx < 4:
            curchar = string[index + idx]
            if "0" <= curchar <= "9" or "a" <= curchar <= "f" or "A" <= curchar <= "F":
                idx += 1
                continue
            else:
                raise ValueError("Invalid unicode char {}".format(curchar))
        return string[index:index + 4], index + 4