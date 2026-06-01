import pprint 
from parser import Parser
import json

pp = pprint.PrettyPrinter(indent=4)

parser = Parser()

tests = [
    """
{}
""",

    """
[]
""",

    """
{
  "a": {
    "b": {
      "c": {
        "d": {
          "e": [1]
        }
      }
    }
  }
}
""",

    """
{
    
    
    "a"    :     1,
    
    "b" : [ 1 , 2 , 3 ]
    
}
""",

    """
[[], [[]], [[[]]]]
""",

    """
{
  "a": "",
  "b": ["", "", ""]
}
""",

    """
{
  "a": -1,
  "b": -12.34,
  "c": 0.001,
  "d": 999999999
}
""",

    """
[
  {"a": 1},
  {"b": 2},
  {"c": 3}
]
""",

    """
[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
""",

    """
{
  "a": [1, 2, {"x": 3}],
  "b": {
    "c": [4, {"d": 5}]
  }
}
""",

    # INVALID TESTS

    """
{
  "a": 1,
}
""",

    """
[1,2,3,]
""",

    """
{
  "a": 1
  "b": 2
}
""",

    """
{
  "a" 1
}
""",

    """
{
  "a": 1
""",

    """
[1,2,3
""",

    """
{
  "a": "test
}
""",

    """
[1,,2]
""",

    """
,
""",

    """
{
  "a": 01
}
""",

    """
{
  "a": -
}
""",

    """
{
  "a": 1.
}
""",

    """
{
  "a": .5
}
""",

    """
{
  test
}
""",

    """
{} {}
"""
]

for i, test in enumerate(tests):
    try:
        print(f"\n####### TEST {i}: ######\n")
        print(json.dumps(parser.parse_json(test), sort_keys=True, indent=4))
    except ValueError as e:
        print(e)
    except SyntaxError as e:
        print(e)