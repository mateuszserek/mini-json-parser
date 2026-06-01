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
            SKIP: r"\s+"
        }

    def get_error_in_text(self, text, position, context_lines=2):
        lines = text.splitlines()
        line_number = text[:position].count("\n")
        column = position - (text.rfind("\n", 0, position) + 1)
        start = max(0, line_number - context_lines)
        end = min(len(lines), line_number + context_lines + 1)

        result = []

        for i in range(start, end):
            prefix = ">" if i == line_number else " "

            result.append(
                f"{prefix} {i+1:3} | {lines[i]}"
            )

            if i == line_number:
                result.append(
                    f"        {' ' * column}^"
                )

        return "\n".join(result)

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
                    tokens.append((token_type, token_value, text_index))

                text_index += len(token_value)
                matched = True
                break
            if not matched:
                if text[text_index] == '"':
                    raise SyntaxError(
                        "\n".join([
                            JSON_SYNTAX_ERROR,
                            "",
                            self.get_error_in_text(text, text_index),
                            "Unterminated string literal",
                            "",
                            'Expected closing quote: "'
                        ])
                    )

                raise SyntaxError(
                    "\n".join([
                        JSON_SYNTAX_ERROR,
                        "",
                        self.get_error_in_text(text, text_index),
                        "",
                        f"Unexpected character: '{text[text_index]}'"
                    ])
                )
        return tokens