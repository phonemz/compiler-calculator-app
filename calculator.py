from sly import Lexer, Parser


class CalcLexer(Lexer):
    tokens = {NUMBER, PLUS, TIMES, LPAREN, RPAREN}
    ignore = " \t"

    NUMBER = r"\d+"
    PLUS = r"\+"
    TIMES = r"\*"
    LPAREN = r"\("
    RPAREN = r"\)"

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        self.index += 1


class CalcParser(Parser):
    tokens = CalcLexer.tokens

    precedence = (
        ("left", TIMES),
        ("left", PLUS),
    )

    def __init__(self):
        self.env = {}

    @_("expr PLUS expr")
    def expr(self, p):
        return ("+", p.expr0, p.expr1)

    @_("expr TIMES expr")
    def expr(self, p):
        return ("*", p.expr0, p.expr1)

    @_("LPAREN expr RPAREN")
    def expr(self, p):
        return p.expr

    @_("NUMBER")
    def expr(self, p):
        return int(p.NUMBER)

    def prefix(self, p):
        if isinstance(p, tuple):
            op, left, right = p
            return f"{op} {self.prefix(left)} {self.prefix(right)}"
        else:
            return str(p)

    def postfix(self, p):
        if isinstance(p, tuple):
            op, left, right = p
            return f"{self.postfix(left)} {self.postfix(right)} {op}"
        else:
            return str(p)

    def evaluate(self, p):
        if isinstance(p, tuple):
            op, left, right = p
            if op == "+":
                return self.evaluate(left) + self.evaluate(right)
            elif op == "*":
                return self.evaluate(left) * self.evaluate(right)
        else:
            return p

    def error(self, p):
        if p:
            print("Syntax error at token", p.type)
            self.index += 1
        else:
            print("Syntax error at EOF")
