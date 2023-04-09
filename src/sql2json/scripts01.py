from __future__ import annotations

from .sqlparse_interchange.extractor import SqlExtractor

from .sqlparse_interchange.column_descriptor import IntDescriptor


def get_text():
    with open("temp.sql", "r") as f:
        content = f.read()
        return content


class Convert:

    def __init__(self, sql_extractor: SqlExtractor):
        self.sql_extractor = sql_extractor

    def execute(self):
        result = []
        columns = self.sql_extractor.columns

        for col in columns:
            import re

            if t := re.search(r"\(.*.\)", col):
                col_size = t.group(0)

                sql_text = re.sub(r"\(.*.\)", '', col).split(" ")

                col_name = sql_text[0]
                col_type = sql_text[1]

                result.append(self.get_inttype(col_name, col_size, col_type, sql_text))

        return result

    def get_inttype(self, col_name, col_size, col_type, sql_text):
        if col_type not in ('smallint', 'int', 'bigint'):
            raise Exception("Type is Not Int")

        # Ex. name int(1) unsigned not null
        if sql_text[2].upper() == 'UNSIGNED' and sql_text[3].upper() == 'NOT' and sql_text[4].upper() == "NULL":
            return IntDescriptor(col_name=col_name, col_type=col_type, col_size=col_size,
                                 is_unsigned=True, is_null=False)
        # Ex. name int(1) default null
        if sql_text[2].upper() != 'UNSIGNED' and sql_text[3].upper() == 'NULL':
            return IntDescriptor(col_name=col_name, col_type=col_type, col_size=col_size,
                                 is_unsigned=False, is_null=True)
        # Ex. name int(1) not null
        if sql_text[2].upper() != 'UNSIGNED' and sql_text[3].upper() == 'NOT':
            return IntDescriptor(col_name=col_name, col_type=col_type, col_size=col_size,
                                 is_unsigned=False, is_null=False)


if __name__ == '__main__':
    convert = Convert(
        sql_extractor=SqlExtractor(get_text())
    )
    convert.execute()
