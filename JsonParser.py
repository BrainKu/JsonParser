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
        isfirstzero = False
        isfirstminus = False
        hasdot = False
        haspower = False
        length = len(string)
        idx = index
        # 先检查是否含有前导0和负号
        if string[idx] == '0':
            isfirstzero = True
            idx += 1
        elif string[idx] == '-':
            isfirstminus = True
            idx += 1
        else:
            pass
        while 1:
            if idx == length or string[idx] == ']' or string[idx] == '}' or string[idx] == ',':
                if hasdot or haspower:
                    return float(string[index:idx]), idx
                else:
                    return long(string[index:idx]), idx
            elif string[idx] == '.':
                if hasdot:
                    raise ValueError("Invalid number with double dot")
                elif isfirstzero:
                    string[idx-1]!='0'
                    hasdot = True
                    idx += 1
                    continue
            elif string[idx] == 'E' or string[idx] == 'e':
                pass
            elif string[idx] == '+' or string[idx] == '-':
                if string[idx - 1] != 'E' or string[idx - 1] != 'e':
                    raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))
                else:
                    idx += 1
                    continue
            elif '0' <= string[idx] <= '9':

                pass
            else:
                raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))

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