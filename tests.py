import pprint 
from parser import Parser

pp = pprint.PrettyPrinter(indent=4)

parser = Parser()
json_dict = parser.parse_json("""
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
                "value": 123,
                "arr": []
            },    
            [1,2,3,4,5]        
        ],
                      "val": [1, 2, "avc"],
        "a": 123
        }
""")

pp.pprint(json_dict)