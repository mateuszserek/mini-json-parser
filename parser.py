from lexer import Lexer
from config import *

class Parser:
    lexer: Lexer
    current_position: int
    tokens: list
    text: str

    def __init__(self):
        self.lexer = Lexer()
        self.current_position = 0
        self.text = ""

    def reset_parser(self):
        self.current_position = 0
        self.tokens = []
        self.text = ""

    def prepare_exception_message(self, position, expected_token, unexpected_token, exception_type = JSON_SYNTAX_ERROR):
        error_text = self.get_error_in_text(position)

        lines = [
            exception_type,
            "",
            error_text,
            f"{UNEXPECTED_TOKEN}: '{unexpected_token}'",
            f"{EXPECTED}: {expected_token}"
        ]

        return "\n".join(lines)

    def get_error_in_text(self, position, context_lines=4):
        lines = self.text.splitlines()

        line_number = self.text[:position].count("\n")
        column = position - (self.text.rfind("\n", 0, position) + 1)

        start = max(0, line_number - context_lines)
        end = min(len(lines), line_number + context_lines + 1)

        result = []

        for i in range(start, end):
            prefix = ">" if i == line_number else " "
            result.append(f"{prefix} {i+1:3} | {lines[i]}")

            if i == line_number:
                result.append(
                    f"        {' ' * column}^"
                )

        return "\n".join(result)

    def expect(self, expected_token):
        current_token = self.get_current_token()
        if current_token[0] != expected_token:
            raise ValueError(
                self.prepare_exception_message(
                    current_token[2],
                    TOKEN_DICT[expected_token],
                    current_token[1],
                    UNEXPECTED_TOKEN
                )
            )
        self.current_position += 1
        return current_token[1]
    
    def convert_number(self, num: str):
        if "." in num:
            return float(num)
        return int(num)
    
    def parse_value(self):
        current_type, current_value, current_position = self.get_current_token()

        if current_type == LBRACKET:
            return self.parse_array()
        
        if current_type == LBRACE:
            return self.parse_object()
        
        if current_type == STRING:
            self.current_position += 1
            return current_value[1:-1]
        
        if current_type == NUMBER:
            self.current_position += 1
            return self.convert_number(current_value)
        
        raise ValueError (
            self.prepare_exception_message(
                current_position,
                JSON_VALUE,
                current_value,
                EXPECTED_JSON_VALUE
            )
        )
    def get_current_token(self):
        return self.tokens[self.current_position]

    def parse_array(self):
        try:
            result = []
            self.expect(LBRACKET)

            if self.get_current_token()[0] == RBRACKET:
                self.current_position += 1
                return result

            while True:
                result.append(self.parse_value())

                token_type, token_value, position = self.get_current_token()

                if token_type == RBRACKET:
                    self.current_position += 1
                    return result

                if token_type != COMMA:
                    raise ValueError(
                        self.prepare_exception_message(
                            position,
                            "',' or ']'",
                            token_value
                        )
                    )
                self.current_position += 1

                if self.current_position >= len(self.tokens):
                    raise ValueError(END_OF_FILE_EXCEPTION)

                next_type, next_value, next_pos = self.get_current_token()

                if next_type == RBRACKET:
                    raise ValueError(
                        self.prepare_exception_message(
                            next_pos,
                            JSON_VALUE,
                            "]",
                            JSON_SYNTAX_ERROR
                        )
                    )

        except IndexError:
            raise ValueError(END_OF_FILE_EXCEPTION)
        
    def parse_object(self):
        try:
            json_object = {}
            self.expect(LBRACE)
            if self.get_current_token()[0] == RBRACE:
                self.current_position += 1
                return json_object

            while self.current_position < len(self.tokens):
                token_type, key, _ = self.get_current_token()
                self.expect(STRING)
                self.expect(COLON)

                value = self.parse_value()
                json_object[key[1:-1]] = value 

                current_token, val, pos = self.get_current_token()
                if current_token == COMMA:
                    self.current_position += 1
                    continue

                if current_token == RBRACE:
                    self.current_position += 1
                    break 

                raise ValueError(
                    self.prepare_exception_message(
                        pos, "',' or '}'", val, EXPECTED_JSON_VALUE
                    )
                )
            
            return json_object
        except IndexError:
            raise ValueError(END_OF_FILE_EXCEPTION)       

    def parse_json(self, text):
        try:
            self.tokens = self.lexer.tokenize(text)
            self.text = text
            result = {}
            first_token = self.tokens[0][0]

            if not self.tokens:
                raise ValueError(EMPTY_INPUT_EXCEPTION)
            
            if not first_token in [LBRACE, LBRACKET]:
                raise ValueError(FIRST_TOKEN_EXCEPTION)

            if first_token == "LBRACE":
                result = self.parse_object()
            elif first_token == "LBRACKET":
                result = self.parse_array()

            return result
        
        finally:
            self.reset_parser()
