# coding=utf-8
import json


class JsonParser():
    def __init__(self):
        self.d = dict()

    def load(self, s):
        pass

    def getobject(self, index, string):
        pass

    def trimspace(self):
        s = '  \n\tatc  \n\r\t'
        length = len(s)
        idx = 0
        ns = ''
        while 1:
            if idx == length:
                break
            elif s[idx] == '\n' or s[idx] == '\t' or s[idx] == ' ':
                idx += 1
            else:
                ns += s[idx]
                idx += 1
        print s.replace('\n', ' ').replace('\r', '')

    def getlist(self, index, string):
        pass

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
        """Get string"""
        idx = index
        nstring = ""
        length = len(string)
        hasdoublequote = False
        while 1:
            if idx == length:
                if hasdoublequote:
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
                if hasdoublequote:
                    return nstring, idx + 1
                else:
                    hasdoublequote = True
                    idx += 1
            else:
                if hasdoublequote:
                    nstring += string[idx]
                    idx += 1
                elif string[idx] == ' ':
                    idx += 1
                else:
                    raise ValueError("Invalid string not start with double quotes")
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