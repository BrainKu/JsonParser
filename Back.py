__author__ = 'gzs3049'


def loads(s):
    scanonce(s)

    def scanonce(self, s):
        if not s.startswith("{"):
            raise SyntaxError("")
        length = len(s)
        leftcount = 0
        leftsquare = 0
        for i in range(1, length):
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
                elif i + 1 != length and s[i + 1] != "{":
                    raise SyntaxError()
                else:
                    continue
            elif s[i] == "]":
                if leftsquare == 0:
                    raise SyntaxError()
                else:
                    continue

        if leftsquare != 0 or leftsquare != 0:
            raise SyntaxError()