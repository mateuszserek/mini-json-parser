STRING = "STRING"
NUMBER = "NUMBER"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"
COLON = "COLON"
COMMA = "COMMA"
SKIP = "SKIP"
EOF = "EOF"

TOKEN_DICT = {
    STRING: STRING,
    NUMBER: NUMBER,
    LBRACE: "'['",
    RBRACE: "']'",
    LBRACKET: "'{'",
    RBRACKET: "'}'",
    COLON: "':'",
    COMMA: "','"
}

END_OF_FILE_EXCEPTION = "Unexpected end of file"
FIRST_TOKEN_EXCEPTION = "Expceted '[' or '{' at the beginning of the file"
EMPTY_INPUT_EXCEPTION = "Empty File"
EXPECTED_JSON_VALUE = "Expected a JSON value"
JSON_VALUE = "STRING, NUMBER, OBJECT or ARRAY"
JSON_SYNTAX_ERROR = "JSON syntax error"
EXPECTED = "Expected token"
UNEXPECTED_TOKEN = "Unexpected token"