from common import execute_logic
from constants import OPERANDS


class Sentence:
    def __init__(self, raw_content: str = "", content: list = [], symbols: dict = dict()):
        self.raw_content = raw_content
        self.content = content
        self.symbols = symbols

    # check if the model satisfies the sentence
    def check(self, model: list[tuple[str, bool]]) -> bool:
        stack = []
        for token, value in model:
            if token in self.symbols:
                self.symbols[token] = value
        symbols_clone = self.symbols.copy()
        for token in self.content:
            if token not in OPERANDS:
                stack.append(token)
            elif stack.__len__() >= 2 and token != "~":
                right = stack.pop()
                left = stack.pop()
                symbols_clone[f"({left} {token} {right})"] = execute_logic(
                    token, symbols_clone[left], symbols_clone[right]
                )
                stack.append(f"({left} {token} {right})")
            elif stack.__len__() >= 1 and token == "~":
                right = stack.pop()
                symbols_clone[f"~{right}"] = execute_logic(
                    token, symbols_clone[right], symbols_clone[right]
                )
                stack.append(f"~{right}")
        return symbols_clone[stack.pop()]

    def __str__(self) -> str:
        return f"content {str(self.content)}, symbols {str(self.symbols)}"
