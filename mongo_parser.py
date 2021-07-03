from constants import (
    OR,
    AND,
    LT,
    LTE,
    GT,
    GTE,
    NE,
    IN,
)
from typing import Any


class MongoParser:

    @staticmethod
    def parse_select_clause(select_filters: dict) -> str:
        """
        From a list of filters returns them as one string that starts with `SELECT`. If the list of filters is empty,
        it means that not filters are applied and it is returned `SELECT *` as a result.
        Filter can have assigned 1 as value, which means that they have to be applied in the query, or any other number,
        which means that they are not applied to the query.
        
        :param select_filters: 
        :return: 
        """
        filters = [key for key, value in select_filters.items() if value == 1]
        if filters:
            select = 'SELECT ' + ', '.join(filters)
        else:
            select = 'SELECT *'
        return select

    @staticmethod
    def parse_from_clause(from_table: str) -> str:
        """
        Returns the query FROM clause
        :param from_table: 
        :return: 
        """
        return 'FROM {}'.format(from_table)

    @classmethod
    def parse_where_clause(cls, where_filters: dict) -> str:
        """
        From a list of filters returns them as one string that starts with `WHERE`.
        
        :param where_filters: 
        :return: 
        """
        if where_filters:
            return 'WHERE {}'.format(cls.parse(where_filters))
        else:
            return ''

    @classmethod
    def parse(cls, dict_to_convert, return_string=True):
        filters = []
        for key, value in dict_to_convert.items():
            if OPERATOR.get(key):
                if OPERATOR[key] == AndOperationParser or OPERATOR[key] == OrOperationParser:
                    filters.append(OPERATOR[key].translator(cls.parse(value, return_string=False)))
                else:
                    filters.append(OPERATOR[key].translator(value, key))
            elif isinstance(value, dict):
                subkey = next(iter(value.keys()))
                if OPERATOR.get(subkey):
                    filters.append(OPERATOR[subkey].translator(value[subkey], key))
            else:
                filters.append(EqOperationParser.translator(value, key))
        if return_string:
            return AndOperationParser.translator(filters)
        else:
            return filters


class MongoGenericOperationParser:
    """
    This generic class is created just as a Interface to implement in all specific OperationParsers, defining in this
    cas only one common method but in a future, several methods can be implemented to be shared between the different
    inheritors.
    """

    @staticmethod
    def translator(value: Any, attribute: Any) -> str:
        """
        Generic method that should be implemented on each new derived MongoGenericOperationParser class.
        :param value: 
        :param attribute: 
        :return: 
        """
        raise Exception('Unimplemented method.')


class EqOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        value = "{}".format(value) if isinstance(value, str) else value
        return '{} = {}'.format(attribute, value)


class OrOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return ' OR '.join(value)


class AndOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return ' AND '.join(value)


class LtOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} < {}'.format(attribute, value)


class LteOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} <= {}'.format(attribute, value)


class GtOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} > {}'.format(attribute, value)


class GteOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} >= {}'.format(attribute, value)


class NeOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} != {}'.format(attribute, value)


class InOperationParser(MongoGenericOperationParser):
    @staticmethod
    def translator(value, attribute: Any = None) -> str:
        return '{} IN ({})'.format(attribute, ', '.join(value))


OPERATOR = {
    OR: OrOperationParser,
    AND: AndOperationParser,
    LT: LtOperationParser,
    LTE: LteOperationParser,
    GT: GtOperationParser,
    GTE: GteOperationParser,
    NE: NeOperationParser,
    IN: InOperationParser,
}
