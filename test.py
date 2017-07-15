import re


INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
                type=self.type,
                value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None

        self.match = '[0-9]+'

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        ret = re.search(self.match, text[self.pos:])

        if ret is None:
            self.error()

        if ret.group(0).isdigit():
            token = Token(INTEGER, int(ret.group(0)))
            self.pos = ret.end()
            self.match = '\+'
            return token

        if ret.group(0) == '+':
            token = Token(PLUS, ret.group(0))
            self.pos = self.pos + ret.end()
            self.match = '[0-9]+'
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        self.eat(PLUS)

        right = self.current_token
        self.eat(INTEGER)

        print left, right
        result = left.value + right.value

        return result


def main():
    while True:
        text = raw_input('calc> ')
        inter = Interpreter(text)
        print inter.expr()


if __name__ == '__main__':
    main()
