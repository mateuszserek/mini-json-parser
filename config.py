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
    LBRACE: "'{'",
    RBRACE: "'}'",
    LBRACKET: "'['",
    RBRACKET: "']'",
    COLON: "':'",
    COMMA: "','",
    EOF: "end of file"
}

END_OF_FILE_EXCEPTION = "Unexpected end of file"
FIRST_TOKEN_EXCEPTION = "Expected '[' or '{' at the beginning of the file"
EMPTY_INPUT_EXCEPTION = "Empty File"
EXPECTED_JSON_VALUE = "Expected a JSON value"
JSON_VALUE = "STRING, NUMBER, OBJECT or ARRAY"
JSON_SYNTAX_ERROR = "JSON syntax error"
EXPECTED = "Expected token"
UNEXPECTED_TOKEN = "Unexpected token"
EXTRA_CONTENT_EXCEPTION = "Unexpected content after end of JSON document"


class JsonParseError(ValueError):
    pass


def get_line_and_column(text, position):
    line = text[:position].count("\n") + 1
    column = position - (text.rfind("\n", 0, position) + 1) + 1
    return line, column


def format_error_context(text, position, context_lines=2):
    lines = text.split("\n")
    if not lines:
        lines = [""]

    line_index = text[:position].count("\n")
    column = position - (text.rfind("\n", 0, position) + 1)

    start = max(0, line_index - context_lines)
    end = min(len(lines), line_index + context_lines + 1)

    result = []

    for i in range(start, end):
        prefix = ">" if i == line_index else " "
        result.append(f"{prefix} {i + 1:3} | {lines[i]}")

        if i == line_index:
            result.append(f"        {' ' * column}^")

    return "\n".join(result)


def build_error_message(text, position, expected=None, unexpected=None, title=JSON_SYNTAX_ERROR, hint=None):
    line, column = get_line_and_column(text, position)
    lines = [
        f"{title} at line {line}, column {column}",
        "",
        format_error_context(text, position),
    ]

    if unexpected is not None:
        lines.append(f"{UNEXPECTED_TOKEN}: '{unexpected}'")

    if expected is not None:
        lines.append(f"{EXPECTED}: {expected}")

    if hint is not None:
        lines.append(f"Hint: {hint}")

    return "\n".join(lines)
