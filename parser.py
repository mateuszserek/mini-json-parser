from lexer import Lexer
from config import *

class Parser:
    lexer: Lexer
    current_position: int
    tokens: list

    def __init__(self):
        self.lexer = Lexer()
        self.current_position = 0

    def expect(self, expected_token):
        current_token = self.get_current_token()
        if current_token[0] != expected_token:
            raise(ValueError(
                f"Oczekiwano {expected_token}, otrzymano {current_token} na pozycji {self.current_position}"
            ))
        self.current_position += 1
        return current_token[1]
    
    def convert_number(self, num: str):
        if "." in num:
            return float(num)
        return int(num)
    
    def parse_value(self):
        current_type, current_value = self.get_current_token()

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
                    if self.get_current_token()[0] == RBRACKET:
                        raise(ValueError(
                            f"Otrzymano nieoczekiwany ','  na pozycji {self.current_position}"
                        ))
                
        except IndexError:
            raise(ValueError(
                "Nieoczekiwany koniec tekstu"
            ))
        
    def parse_object(self):
        json_object = {}
        self.expect(LBRACE)
        if self.get_current_token()[0] == RBRACE:
            self.current_position += 1
            return json_object

        while self.current_position < len(self.tokens):
            print(self.current_position)
            token_type, key = self.get_current_token()
            self.expect(STRING)
            self.expect(COLON)

            value = self.parse_value()
            json_object[key] = value 

            current_token, val = self.get_current_token()
            if current_token == COMMA:
                self.current_position += 1
                continue

            if current_token == RBRACE:
                self.current_position += 1
                break 
            error_string = "Oczekiwano ',' lub '}' na pozycji " + f"{self.current_position}"
            raise(ValueError(
                error_string
            ))
        return json_object


    def parse_json(self, text):
        self.tokens = self.lexer.tokenize(text)
        print(self.tokens)

        if not self.tokens:
            raise ValueError("Pusty input")

        first_token = self.tokens[0][0]

        if first_token == "LBRACE":
            return self.parse_object()

        elif first_token == "LBRACKET":
            return self.parse_array()

        else:
            raise ValueError(
                "Oczekiwano '{' lub '[' na początku JSON"
            )
        
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
            123,
            {
                "value": 123     
            }            
        ]
    }
"""))