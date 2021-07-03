OR = '$or'
AND = '$and'
LT = '$lt'
LTE = '$lte'
GT = '$gt'
GTE = '$gte'
NE = '$ne'
IN = '$in'

FULL_QUERY_REGEX = r'db\.(.+)\.(.+)\(({.+?})(?:\s?,\s?({.+}))?\)'
DICT_REGEX = r"([^{,]+?)\s?:\s?({.+?}|\[.+\]|[0-9]+|'.+')"