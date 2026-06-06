from parser import Parser
import json

parser = Parser()

valid_tests = [
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
          "e": [-1]
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

    """
{
  "active": true,
  "deleted": false,
  "metadata": null,
  "items": [true, false, null]
}
""",

    """
[true, false, null, {"nested": [null, true, false]}]
""",

    """
{
  "featureFlags": {
    "login": true,
    "payments": false,
    "legacyMode": null
  },
  "users": [
    {"name": "Ada", "active": true},
    {"name": "Bob", "active": false, "lastLogin": null}
  ]
}
""",

    """
{
  "emptyArray": [],
  "emptyObject": {},
  "mixed": [1, "text", true, false, null, {"ok": true}]
}
"""
]

invalid_tests = [
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
""",

    """
{
  "active": True
}
""",

    """
{
  "deleted": False
}
""",

    """
{
  "metadata": None
}
""",

    """
{
  "active": tru
}
""",

    """
{
  "values": [true false]
}
""",

    """
{
  "values": [null,]
}
""",

    """
{
  "flag": true,
  "missing": null
  "next": false
}
"""
]

print("\n================ VALID TESTS - SHOULD PASS ================\n")

for i, test in enumerate(valid_tests):
    try:
        print(f"\n####### VALID TEST {i}: ######\n")
        print(json.dumps(parser.parse_json(test), sort_keys=True, indent=4))
    except ValueError as e:
        print("UNEXPECTED ERROR:")
        print(e)

print("\n================ INVALID TESTS - SHOULD SHOW ERRORS ================\n")

for i, test in enumerate(invalid_tests):
    try:
        print(f"\n####### INVALID TEST {i}: ######\n")
        result = parser.parse_json(test)
        print("UNEXPECTED SUCCESS:")
        print(json.dumps(result, sort_keys=True, indent=4))
    except ValueError as e:
        print(e)
