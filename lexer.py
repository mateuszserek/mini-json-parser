import re 
from config import *

class Lexer:
    token_types: dict

    def __init__(self):
        self.token_types = {
            STRING: r'"[^"]*"',
            NUMBER: r"-?\d+",
            LBRACE: r"\{",
            RBRACE: r"\}",
            LBRACKET: r"\[",
            RBRACKET: r"\]",
            COLON: r":",
            COMMA: r",",
            SKIP: r"\s+"
        }

    def tokenize(self, text: str) -> list:
        if type(text) != str:
            raise("text must be string")
        
        tokens = []
        text_index = 0
        while text_index < len(text):
            matched = False
            for token_type, token_regex in self.token_types.items():
                found_token = re.match(token_regex, text[text_index:])
                if not found_token:
                    continue
                token_value = found_token.group()
                if token_type != SKIP:
                    tokens.append((token_type, token_value))

                text_index += len(token_value)
                matched = True
                break
            if not matched:
                raise(
                    SyntaxError(f"Nieoczekiwany token na pozycji {text_index}")
                )
        return tokens