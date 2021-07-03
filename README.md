# mongotosql

## Automated Testing
Run the following command `pytest tests.py` (over the main folder)

## Manual Testing
Run the following command `python main.py` (over the main folder) and then the user will be asked to enter a 
mongodb query that wants to be translated. After entering it, the resulting SQL query would
be shown on the console. If any error occurs, due to some bad syntax or an unsupported mongodb
operation being entered, an error would be shown on the console.

## Design
Most of the implementation is base on a based class that is inherited by several classes. This inheritance provide with
one or more generic methods that have to be overwritten on each child class with its specific behaviour.
The idea behind of this design is to provide a basic common structure and flexibility to add new child classes in the
future.

There are two main files:
- `string_parser.py`
- `mongo_parser.py`

### String Parser
This file contains a class that is in charge of doing the string parsing and also one Parser class per
each one of the possible structured contained within the string to parse (Dict, List and Values which represents
strings and integers). Those parsers inherit from a common class which provides them with a method to identify if
a given string belongs to the data structure that the Parser represents.

### MongoDB Parser
This file contains a class that is in charge of doing the parsing to a sql syntax and one Parser class per
each one of the supported mongo operators (lt, lte, and, or, etc). Those parsers inherit form a common class and have a
method that will return the corresponding sql syntax given some information.
To know which OperationParser there is dictionary that matches the mongodb operator which its respective parser.