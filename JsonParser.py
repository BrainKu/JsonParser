# coding=utf-8
__author__ = '郑鑫伟'


class JsonParser():
    def __init__(self):
        self.dictcontent = dict()

    def load(self, s):
        """读取json格式数据，输入s为一个json字符串，无返回值"""
        if not isinstance(s, unicode):
            s = s.decode('utf8')
        s = s.strip()
        if s and s[0] == '{':
            self.dictcontent, string = self.getobject(s[1:])
        else:
            raise ValueError("Invalid json string start without object")
        if len(string) != 0:
            raise ValueError("Json string can only have one object")

    def dump(self):
        """根据类中数据返回json字符串"""
        string = self.dumpobject(self.dictcontent)
        string = string.replace('\\x08', '\\b').replace('\\x0c', '\\f')
        return string

    def dumpobject(self, obj):
        """将dict的内容转换为json字符串后返回"""
        objstr = ''
        isfirst = True
        for key, value in obj.iteritems():
            if isfirst:
                isfirst = False
            else:
                objstr += ','
            objstr += self.dumpvalue(key) + ':'
            objstr += self.dumpvalue(value)
        return '{' + objstr + '}'

    def dumplist(self, alist):
        """将list的内容转换为json字符串后返回"""
        liststr = ''
        isfirst = True
        for value in alist:
            if isfirst:
                isfirst = False
            else:
                liststr += ','
            liststr += self.dumpvalue(value)
        return '[' + liststr + ']'

    def dumpvalue(self, value):
        """将value转换为json字符串后返回"""
        valuestr = ''
        if isinstance(value, dict):
            valuestr = self.dumpobject(value)
        elif isinstance(value, list):
            valuestr = self.dumplist(value)
        elif isinstance(value, bool):
            if value:
                valuestr = 'true'
            else:
                valuestr = 'false'
        elif value is None:
            valuestr = 'null'
        elif isinstance(value, unicode) or isinstance(value, str):
            valuestr = u''
            value = value.encode('unicode_escape')
            for char in value:
                if char == '\\':
                    valuestr += '\\'
                elif char == '\"':
                    valuestr += '\\\"'
                elif char == '\b':
                    valuestr += r'\b'
                elif char == '\f':
                    valuestr += 'f'
                elif char == '\n':
                    valuestr += 'n'
                elif char == '\r':
                    valuestr += r'\r'
                elif char == '\t':
                    valuestr += r'\t'
                else:
                    valuestr += char
            valuestr = '"' + valuestr + '"'
        else:
            valuestr = value

        return unicode(valuestr)

    def dumpDict(self):
        """返回一个字典，包含类中数据。所有字符均为unicode"""
        result = dict()
        for key, value in self.dictcontent.iteritems():
            result[key] = self.deepdump(value)
        return result

    def deepdump(self, value):
        """深拷贝对象"""
        if isinstance(value, list):
            l = list()
            for v in value:
                l.append(self.deepdump(v))
            return l
        elif isinstance(value, dict):
            for k, v in value.iteritems():
                d = dict()
                d[k] = self.deepdump(v)
                return d
        else:
            return value

    def loadDict(self, d):
        """读取dict中的数据，存入类中，若遇到不是字符串的key则忽略"""
        self.dictcontent = self.loaddictwithstr(d)

    def loaddictwithstr(self, d):
        """读取字典中的数据，返回一个当前字典的拷贝，若遇到不是字符串的key则忽略"""
        result = dict()
        for key, value in d.iteritems():
            if isinstance(key, str) or isinstance(key, unicode):
                if isinstance(value, dict):
                    value = self.loaddictwithstr(value)
                result[key] = value
        return result

    def loadJson(self, f):
        """从文件中读入json格式数据，f为文件路径，遇到文件读写失败则输出错误提示"""
        try:
            with open(f) as openfile:
                content = openfile.read()
            self.load(content)
        except EOFError:
            print "file {} input failed.".format(f)
        except IOError:
            print "file {} no exist.".format(f)

    def dumpJson(self, f):
        """将类中的内容以json格式存入文件，文件若存在则覆盖，文件操作失败抛出异常"""
        try:
            with open(f, 'w') as outputfile:
                outputfile.write(self.dump().encode(encoding='utf8'))
        except EOFError:
            print "file {} input failed.".format(f)
        except IOError:
            print "file {} no exist.".format(f)

    def getobject(self, string):
        """从已去除了{开头的字符串中获取dict并返回"""
        string = string.lstrip()
        objdict = dict()
        haskey = False
        hascolon = False
        hasvalue = False
        key = None
        while len(string) != 0:
            nextchar = string[0]
            if not haskey and not hascolon:  # 如果没有值和冒号，则先试着获取一个字符串作为key或返回一个空字典
                if nextchar == '}':
                    if len(objdict) == 0:
                        return objdict, string[1:]
                    else:
                        raise ValueError("Invalid object with empty value")
                elif nextchar == '"':
                    key, string = self.getstring(string[1:])
                    string = string.lstrip()
                    haskey = True
                else:
                    raise ValueError("Invalid object with no string key {}".format(string))
            elif haskey and not hascolon:
                if string[0] != ':':
                    raise ValueError("Invalid object without colon {}".format(string[:]))
                else:
                    string = string[1:].lstrip()
                    hascolon = True
            else:
                if nextchar == '}':
                    if haskey and hasvalue:
                        return objdict, string[1:]
                    else:
                        raise ValueError("Invalid object without key or value")
                elif nextchar == ',':
                    if not (hasvalue and haskey):
                        raise ValueError("Object elememnt should contain key and value")
                    haskey = False
                    hasvalue = False
                    hascolon = False
                    string = string[1:].lstrip()
                else:
                    if hasvalue:
                        raise ValueError("Object cannot have two value with one key {}".format(string))
                    value, string = self.getvalue(string[0:])
                    string = string.lstrip()
                    hasvalue = True
                    objdict[key] = value

        raise ValueError("String {}".format(string))

    def getarray(self, string):
        """从已去除了[开头的字符串中获取list"""
        string = string.lstrip()
        objlist = list()
        hasvalue = False  # 记录逗号前是否有值
        while len(string) != 0:
            nextchar = string[0]
            if nextchar == ']':
                if hasvalue or len(objlist) == 0:  # 如果右括号前有value或数组为空则返回
                    return objlist, string[1:]
                else:
                    raise ValueError("Invalid list with empty value")
            elif nextchar == ',':
                if hasvalue:
                    hasvalue = False
                    string = string[1:].lstrip()
                else:
                    raise ValueError("Invalid comma in list")
            else:
                value, string = self.getvalue(string)
                hasvalue = True
                objlist.append(value)
                string = string.lstrip()

        raise ValueError("Invalid list with no close symbol")

    def getvalue(self, string):
        """获取json标准中对应的value"""
        string = string.lstrip()
        if len(string) == 0:
            raise ValueError("Invalid value with empty content")
        if string[0] == '[':
            return self.getarray(string[1:])
        elif string[0] == '{':
            return self.getobject(string[1:])
        elif string[0] == '"':
            return self.getstring(string[1:])
        elif "0" <= string[0] <= "9" or string[0] == '-':
            return self.getnumber(string[0:])
        elif string[0] == 't':
            if len(string) >= 4 and string[:4] == 'true':
                return True, string[4:]
            else:
                raise ValueError("Invalid string start with t")
        elif string[0] == 'f':
            if len(string) >= 5 and string[:5] == 'false':
                return False, string[5:]
            else:
                raise ValueError("Invalid string start with f")
        elif string[0] == 'n':
            if len(string) >= 4 and string[:4] == 'null':
                return None, string[4:]
            else:
                raise ValueError("Invalid string start with n")
        else:
            raise ValueError("Invalid Symbol:{}".format(string[0]))

    def getnumber(self, string):
        """
        获取字符串中的数字，返回截取了数字之后的内容
        先判断是否含有前导0，如果含有前导0则特殊处理，处理之后再按照正常的逻辑进行判断
        """
        iszerofirst = False
        hasdot = False
        haspower = False
        length = len(string)
        idx = 0
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
                return 0, string[idx:]
            elif string[idx] != '.' and string[idx] != 'e' and string[idx] != 'E':  # 前导0后面跟的如果不是.，E，e中的其中一个则不合法
                raise ValueError("Invalid number with leading zero")
            else:
                pass
        while 1:
            if idx == length or string[idx] == ']' or string[idx] == '}' or string[idx] == ',':
                if hasdot or haspower:
                    return float(string[:idx]), string[idx:]
                else:
                    return int(string[:idx]), string[idx:]
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
                    if idx == length or string[idx] == '}' \
                            or string[idx] == ']' or string[idx] == ',':
                        raise ValueError("Invalid number with symbol {} in index {}".format(string[idx - 1], idx))
                    else:
                        continue
            elif string[idx] == '+' or string[idx] == '-':
                if string[idx - 1] != 'E' and string[idx - 1] != 'e':
                    raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))
                else:
                    idx += 1
                    if idx == length or string[idx] == '}' or string[idx] == ']' \
                            or string[idx] == ',':  # 单独的E-或者E+也是不合法的
                        raise ValueError("Invalid number with symbol {} in index {}".format(string[idx - 1], idx))
                    continue
            elif '0' <= string[idx] <= '9':
                idx += 1
                continue
            elif string[idx] == '\n' or string[idx] == ' ' or string[idx] == '\t':  # 忽略空格和换行符号
                idx += 1
                continue
            else:
                raise ValueError("Number has invalid symbol {} in index {}".format(string[idx], idx))

    def getstring(self, string):
        """获取string，返回截取了string剩下的内容"""
        idx = 0
        nstring = ""
        length = len(string)
        while idx < length:
            if string[idx] == '\\':
                idx += 1
                if idx == length:
                    break
                elif string[idx] == 'u':  # Get unicode char
                    curchar, idx = self.getchar(string, idx + 1)
                    nstring += curchar
                elif string[idx] == '"':
                    nstring += '\"'
                    idx += 1
                elif string[idx] == '\\':
                    nstring += '\\'
                    idx += 1
                elif string[idx] == '/':
                    nstring += '/'
                    idx += 1
                elif string[idx] == 'b':
                    nstring += '\b'
                    idx += 1
                elif string[idx] == 'f':
                    nstring += '\f'
                    idx += 1
                elif string[idx] == 'n':
                    nstring += '\n'
                    idx += 1
                elif string[idx] == 'r':
                    nstring += '\r'
                    idx += 1
                elif string[idx] == 't':
                    nstring += '\t'
                    idx += 1
                else:
                    raise ValueError("Invalid escapse: {}".format(string[idx]))
            elif string[idx] == '"':
                return unicode(nstring), string[idx + 1:]
            else:
                nstring += string[idx]
                idx += 1
        raise ValueError("Invalid string with no close \"")

    def getchar(self, string, index):
        """获取unicode字符"""
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
        return unichr(int(string[index:index + 4], 16)), index + 4

    def __getitem__(self, item):
        return self.dictcontent[item]

    def __setitem__(self, key, value):
        self.dictcontent[key] = value

    def update(self, d):
        """用字典d更新类中的数据"""
        d = self.loaddictwithstr(d)
        for key, value in d.iteritems():
            self.dictcontent[key] = value