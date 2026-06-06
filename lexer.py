import re 
from config import *

class Lexer:
    token_types: dict

    def __init__(self):
        self.token_types = {
            STRING: r'"[^"]*"',
            NUMBER: r'-?(0|[1-9]\d*)(\.\d+)?',
            LBRACE: r"\{",
            RBRACE: r"\}",
            LBRACKET: r"\[",
            RBRACKET: r"\]",
            COLON: r":",
            COMMA: r",",
            TRUE: r"true",
            FALSE: r"false",
            NULL: r"null",
            SKIP: r"\s+"
        }

    def tokenize(self, text: str) -> list:
        if type(text) != str:
            raise TypeError("text must be string")
        
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
                    tokens.append((token_type, token_value, text_index))

                text_index += len(token_value)
                matched = True
                break
            if not matched:
                if text[text_index] == '"':
                    raise JsonParseError(
                        build_error_message(
                            text,
                            text_index,
                            expected='closing quote: "',
                            unexpected=text[text_index],
                            hint="Unterminated string literal"
                        )
                    )

                raise JsonParseError(
                    build_error_message(
                        text,
                        text_index,
                        unexpected=text[text_index],
                        hint="Remove this character or replace it with a valid JSON token"
                    )
                )
        tokens.append((EOF, EOF, len(text)))
        return tokens
