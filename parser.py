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
        return build_error_message(
            self.text,
            position,
            expected=expected_token,
            unexpected=unexpected_token,
            title=exception_type
        )

    def get_token_display_value(self, token_type, token_value):
        if token_type == EOF:
            return TOKEN_DICT[EOF]
        return token_value

    def expect(self, expected_token):
        current_token = self.get_current_token()
        if current_token[0] != expected_token:
            raise JsonParseError(
                self.prepare_exception_message(
                    current_token[2],
                    TOKEN_DICT[expected_token],
                    self.get_token_display_value(current_token[0], current_token[1]),
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

        if current_type == TRUE:
            self.current_position += 1
            return True

        if current_type == FALSE:
            self.current_position += 1
            return False

        if current_type == NULL:
            self.current_position += 1
            return None
        
        raise JsonParseError (
            self.prepare_exception_message(
                current_position,
                JSON_VALUE,
                self.get_token_display_value(current_type, current_value),
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
                    raise JsonParseError(
                        self.prepare_exception_message(
                            position,
                            "',' or ']'",
                            self.get_token_display_value(token_type, token_value)
                        )
                    )
                self.current_position += 1

                next_type, next_value, next_pos = self.get_current_token()

                if next_type == RBRACKET:
                    raise JsonParseError(
                        build_error_message(
                            self.text,
                            next_pos,
                            expected=JSON_VALUE,
                            unexpected=next_value,
                            hint="Trailing comma is not allowed in a JSON array"
                        )
                    )

        except IndexError:
            raise JsonParseError(
                build_error_message(
                    self.text,
                    len(self.text),
                    expected="']'",
                    unexpected=TOKEN_DICT[EOF],
                    title=END_OF_FILE_EXCEPTION
                )
            )
        
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
                    next_token, next_val, next_pos = self.get_current_token()
                    if next_token == RBRACE:
                        raise JsonParseError(
                            build_error_message(
                                self.text,
                                next_pos,
                                expected=STRING,
                                unexpected=next_val,
                                hint="Trailing comma is not allowed in a JSON object"
                            )
                        )
                    continue

                if current_token == RBRACE:
                    self.current_position += 1
                    break 

                raise JsonParseError(
                    self.prepare_exception_message(
                        pos,
                        "',' or '}'",
                        self.get_token_display_value(current_token, val),
                        EXPECTED_JSON_VALUE
                    )
                )
            
            return json_object
        except IndexError:
            raise JsonParseError(
                build_error_message(
                    self.text,
                    len(self.text),
                    expected="'}'",
                    unexpected=TOKEN_DICT[EOF],
                    title=END_OF_FILE_EXCEPTION
                )
            )

    def parse_json(self, text):
        try:
            self.text = text
            self.tokens = self.lexer.tokenize(text)
            result = {}

            if len(self.tokens) == 1 and self.tokens[0][0] == EOF:
                raise JsonParseError(
                    build_error_message(
                        self.text,
                        self.tokens[0][2],
                        expected="'{' or '['",
                        unexpected=TOKEN_DICT[EOF],
                        title=EMPTY_INPUT_EXCEPTION
                    )
                )

            first_token = self.tokens[0][0]
            
            if not first_token in [LBRACE, LBRACKET]:
                first_token_type, first_token_value, first_token_position = self.tokens[0]
                raise JsonParseError(
                    build_error_message(
                        self.text,
                        first_token_position,
                        expected="'{' or '['",
                        unexpected=self.get_token_display_value(first_token_type, first_token_value),
                        title=FIRST_TOKEN_EXCEPTION
                    )
                )

            if first_token == LBRACE:
                result = self.parse_object()
            elif first_token == LBRACKET:
                result = self.parse_array()

            current_token_type, current_token_value, current_token_position = self.get_current_token()
            if current_token_type != EOF:
                raise JsonParseError(
                    build_error_message(
                        self.text,
                        current_token_position,
                        expected=TOKEN_DICT[EOF],
                        unexpected=self.get_token_display_value(current_token_type, current_token_value),
                        title=EXTRA_CONTENT_EXCEPTION
                    )
                )

            return result
        
        finally:
            self.reset_parser()
