# Parser JSON

## Opis projektu

Projekt jest prostym parserem JSON napisanym w Pythonie. Program rozwiązuje problem analizy tekstowego wejścia w formacie JSON: najpierw dzieli tekst na tokeny przy pomocy leksera, a następnie parser rekurencyjnie sprawdza strukturę dokumentu i przekształca go na odpowiadające mu struktury Pythona.

Główne funkcjonalności parsera:

- rozpoznawanie obiektów JSON,
- rozpoznawanie tablic JSON,
- obsługa zagnieżdżonych obiektów i tablic,
- obsługa napisów oraz liczb całkowitych i zmiennoprzecinkowych,
- ignorowanie białych znaków,
- zgłaszanie błędów składniowych wraz z pozycją problemu w tekście.

Implementacja obsługuje podzbiór formatu JSON: obiekty, tablice, napisy i liczby. W aktualnej wersji nie zdefiniowano tokenów dla wartości `true`, `false`, `null` ani sekwencji escape w napisach.

## Formalna gramatyka i tokeny

### Tokeny leksykalne

Lekser rozpoznaje następujące tokeny:

| Token | Wyrażenie regularne | Znaczenie |
| --- | --- | --- |
| `STRING` | `"[^"]*"` | napis w cudzysłowie |
| `NUMBER` | `-?(0|[1-9]\d*)(\.\d+)?` | liczba całkowita lub zmiennoprzecinkowa |
| `LBRACE` | `\{` | nawias klamrowy otwierający `{` |
| `RBRACE` | `\}` | nawias klamrowy zamykający `}` |
| `LBRACKET` | `\[` | nawias kwadratowy otwierający `[` |
| `RBRACKET` | `\]` | nawias kwadratowy zamykający `]` |
| `COLON` | `:` | dwukropek |
| `COMMA` | `,` | przecinek |
| `SKIP` | `\s+` | białe znaki pomijane przez lekser |

### Gramatyka

Symbol startowy: `json`.

Nieterminale: `json`, `value`, `object`, `members`, `member`, `array`, `elements`.

Terminale: `STRING`, `NUMBER`, `{`, `}`, `[`, `]`, `:`, `,`.

Gramatyka w notacji EBNF:

```ebnf
json     ::= object | array

value    ::= STRING
           | NUMBER
           | object
           | array

object   ::= "{" "}"
           | "{" members "}"

members  ::= member
           | member "," members

member   ::= STRING ":" value

array    ::= "[" "]"
           | "[" elements "]"

elements ::= value
           | value "," elements
```

Zgodnie z hierarchią Chomsky'ego jest to gramatyka bezkontekstowa, czyli gramatyka typu 2. Każda produkcja ma po lewej stronie pojedynczy nieterminal, a struktury zagnieżdżone, takie jak obiekty i tablice, są opisywane rekurencyjnie.

## Instrukcja uruchomienia

1. Upewnij się, że masz zainstalowanego Pythona 3.

2. Przejdź do katalogu projektu:

```bash
cd /Users/mateuszserek/Desktop/json_parser
```

3. Uruchom zestaw przykładów i testów:

```bash
python3 tests.py
```

Projekt korzysta wyłącznie z bibliotek standardowych Pythona (`re`, `json`, `pprint`), dlatego nie wymaga instalowania zewnętrznych zależności przez `pip`.

Parser można też wykorzystać bezpośrednio w innym skrypcie:

```python
from parser import Parser

parser = Parser()
result = parser.parse_json('{"a": [1, 2, {"b": -3.5}]}')
print(result)
```

## Przykłady użycia

### Przykład 1: poprawny obiekt JSON

Wejście:

```json
{
  "a": 1,
  "b": [1, 2, 3]
}
```

Wynik interpretacji:

```python
{
    "a": 1,
    "b": [1, 2, 3]
}
```

Odpowiadająca struktura AST może być przedstawiona jako:

```text
object
├── member
│   ├── key: "a"
│   └── value: number(1)
└── member
    ├── key: "b"
    └── value: array
        ├── number(1)
        ├── number(2)
        └── number(3)
```

### Przykład 2: poprawne zagnieżdżenie obiektów i tablic

Wejście:

```json
{
  "a": [1, 2, {"x": 3}],
  "b": {
    "c": [4, {"d": 5}]
  }
}
```

Wynik interpretacji:

```python
{
    "a": [
        1,
        2,
        {
            "x": 3
        }
    ],
    "b": {
        "c": [
            4,
            {
                "d": 5
            }
        ]
    }
}
```

Odpowiadająca struktura AST może być przedstawiona jako:

```text
object
├── member
│   ├── key: "a"
│   └── value: array
│       ├── number(1)
│       ├── number(2)
│       └── object
│           └── member
│               ├── key: "x"
│               └── value: number(3)
└── member
    ├── key: "b"
    └── value: object
        └── member
            ├── key: "c"
            └── value: array
                ├── number(4)
                └── object
                    └── member
                        ├── key: "d"
                        └── value: number(5)
```

### Przykład 3: obsługa błędu składniowego

Wejście z błędem, czyli przecinkiem po ostatnim elemencie tablicy:

```json
[1,2,3,]
```

Wynik działania parsera:

```text
JSON syntax error

>   1 | [1,2,3,]
            ^
Unexpected token: ']'
Expected token: STRING, NUMBER, OBJECT or ARRAY
```

Parser wskazuje miejsce błędu znakiem `^`, pokazuje nieoczekiwany token oraz informuje, jakiego typu wartości oczekiwał w tym miejscu.
