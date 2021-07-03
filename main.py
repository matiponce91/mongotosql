from mongo_parser import MongoParser
from string_to_dict_parser import StringToDictParser
from re import match
from constants import FULL_QUERY_REGEX


def parse_mongodb_query_to_sql(query):
    try:
        if not query.startswith('db.'):
            print("Invalid clause initialization")
            return

        regex_match = match(FULL_QUERY_REGEX, query)

        if regex_match.group(2) != 'find':
            print('Invalid database method')
            return

        select_filter_dict = StringToDictParser.parse(regex_match.group(4))
        select_filter_sql_string = MongoParser.parse_select_clause(select_filter_dict)

        from_filter_sql_string = MongoParser.parse_from_clause(regex_match.group(1))

        where_filter_dict = StringToDictParser.parse(regex_match.group(3))
        where_filter_sql_string = MongoParser.parse_where_clause(where_filter_dict)

        return '{} {} {}'.format(select_filter_sql_string, from_filter_sql_string, where_filter_sql_string)
    except:
        print('There was a problem with the program')


if __name__ == '__main__':
    print('Enter the mongo query that you want to parse to sql: ')
    value = input()
    result = parse_mongodb_query_to_sql(value)
    print(result)
