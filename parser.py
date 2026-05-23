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

    def get_error_in_text(self, position, context_lines=2):
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
                    f"      {' ' * column}^"
                )

        return "\n".join(result)

    def expect(self, expected_token):
        current_token = self.get_current_token()
        if current_token[0] != expected_token:
            raise ValueError(
                f"{JSON_SYNTAX_ERROR}\n\n"
                f"{self.get_error_in_text(current_token[2])}\n"
                f"{EXPECTED} {expected_token}\n"
                f"{UNEXPECTED_TOKEN}: '{current_token[1]}'"
            )
        self.current_position += 1
        return current_token[1]
    
    def convert_number(self, num: str):
        if "." in num:
            return float(num)
        return int(num)
    
    def parse_value(self):
        current_type, current_value, _ = self.get_current_token()

        if current_type == LBRACKET:
            return self.parse_array()
        
        if current_type == LBRACE:
            return self.parse_object()
        
        if current_type == STRING:
            self.current_position += 1
            return current_value
        
        if current_type == NUMBER:
            self.current_position += 1
            return self.convert_number(current_value)

    def get_current_token(self):
        return self.tokens[self.current_position]

    def parse_array(self):
        try:
            json_list = []
            self.expect(LBRACKET)
            if self.get_current_token()[0] == RBRACKET:
                return json_list
            
            while self.current_position < len(self.tokens):
                json_list.append(self.parse_value())
                if self.get_current_token()[0] == RBRACKET:
                    self.current_position += 1
                    return json_list
                else:
                    self.expect(COMMA)
                    current_token = self.get_current_token()
                    if current_token[0] == RBRACKET:
                        raise(ValueError(
                            f"{JSON_SYNTAX_ERROR}\n\n"
                            f"{self.get_error_in_text(current_token[2])}\n"
                            f"{EXPECTED}']'\n"
                            f"{UNEXPECTED_TOKEN}: '{current_token[1]}'"
                        ))
                
        except IndexError:
            raise(ValueError(END_OF_FILE_EXCEPTION))
        
    def parse_object(self):
        json_object = {}
        self.expect(LBRACE)
        if self.get_current_token()[0] == RBRACE:
            self.current_position += 1
            return json_object

        while self.current_position < len(self.tokens):
            print(self.current_position)
            token_type, key, _ = self.get_current_token()
            self.expect(STRING)
            self.expect(COLON)

            value = self.parse_value()
            json_object[key] = value 

            current_token, val, pos = self.get_current_token()
            if current_token == COMMA:
                self.current_position += 1
                continue

            if current_token == RBRACE:
                self.current_position += 1
                break 

            raise ValueError(
                f"{JSON_SYNTAX_ERROR}\n\n"
                f"{self.get_error_in_text(pos)}\n"
                f"{UNEXPECTED_TOKEN}: '{val}'"
            )
        
        return json_object


    def parse_json(self, text):
        self.tokens = self.lexer.tokenize(text)
        self.text = text
        print(self.tokens)

        if not self.tokens:
            raise ValueError(EMPTY_INPUT_EXCEPTION)

        first_token = self.tokens[0][0]

        if first_token == "LBRACE":
            result = self.parse_object()
            self.reset_parser()
            return result

        elif first_token == "LBRACKET":
            result = self.parse_array()
            self.reset_parser()
            return result

        else:
            self.reset_parser()
            raise ValueError(FIRST_TOKEN_EXCEPTION)
        
parser = Parser()
print(parser.parse_json("""
    {
        "name": "Jan",
        "age": 2,
        "address": {
            "city": "Szczecin",
            "street": "Mickiewicza",
            "number": 12
        },
        "array": [
            "key",
            123,"adc",
            {
                "value": 123     
            },    
            [1,2,3,4,5]        
        ],
                      "val": ["asc"],
    }
"""))


print(parser.parse_json(
    """
    {
        "key": "value"
    }
"""
))