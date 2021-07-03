from re import findall
from constants import DICT_REGEX
from typing import Any, Tuple, Union


class StringToDictParser:
    @classmethod
    def parse(cls, string_to_parse: str) -> Any:
        """
        This method allows to parse an incoming string with a mongodb query format into a dict.

        :param string_to_parse:
        :return:
        """

        if string_to_parse is None:
            return {}
        if DictParser.is_type_of_this_class(string_to_parse):
            keys, values = DictParser.get_dict_key_values(string_to_parse)
            # This allows to recursively parse the inner elements of a dictionary
            return dict(zip(
                keys,
                map(cls.parse, values),
            ))
        elif ListParser.is_type_of_this_class(string_to_parse):
            values = ListParser.get_list_values(string_to_parse)
            return list(map(cls.parse, values))
        elif ValueParser.is_type_of_this_class(string_to_parse):
            return ValueParser.transform_value(string_to_parse)


class GenericParser:
    @staticmethod
    def is_type_of_this_class(string: str) -> bool:
        """
        Generic method to get if the type of the string after parsing would be the same as the class determines

        :param string:
        :return:
        """
        raise Exception('Unimplemented method')


class DictParser(GenericParser):
    @staticmethod
    def is_type_of_this_class(string: str) -> bool:
        return string.startswith('{')

    @staticmethod
    def get_dict_key_values(string: str) -> Tuple[list, list]:
        matched_result = findall(DICT_REGEX, string)
        keys = []
        values = []
        for result_tuple in matched_result:
            keys.append(result_tuple[0].strip())
            values.append(result_tuple[1])
        return keys, values


class ListParser(GenericParser):
    @staticmethod
    def is_type_of_this_class(string: str) -> bool:
        return string.startswith('[')

    @staticmethod
    def get_list_values(string: str) -> list:
        string = string[1:-1]
        return string.split(',')


class ValueParser(GenericParser):
    @classmethod
    def is_type_of_this_class(cls, string: str) -> bool:
        return cls._is_string(string) or cls._is_number(string)

    @staticmethod
    def _is_string(string: str) -> bool:
        return string.strip().startswith("'") or string.strip().startswith('"')

    @staticmethod
    def _is_number(string: str) -> bool:
        return string.isdigit()

    @classmethod
    def transform_value(cls, string: str) -> Union[str, int]:
        if cls._is_number(string):
            return int(string)
        elif cls._is_string(string):
            return string.strip()
