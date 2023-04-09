from __future__ import annotations

from typing import TYPE_CHECKING

from .sql2json.sqlparse_interchange.extractor import SqlExtractor
from .sql2json.scripts01 import Convert

if TYPE_CHECKING:
    from .sql2json.sqlparse_interchange.column_descriptor import IntDescriptor


def test_int_column_01():
    sql_text = """create table foo (
    _id int(1) DEFAULT NULL
    ) Engnine=Innodb charset=utf8;    
    """

    convert = Convert(
        sql_extractor=SqlExtractor(sql_text=sql_text)
    )
    result: IntDescriptor = convert.execute()[0]

    assert result.col_name == '_id'
    assert result.col_type == 'int'
    assert result.col_size == '(1)'
    assert result.is_unsigned is False
    assert result.is_null is True


def test_int_column_02():
    sql_text = """create table foo (
    _id int(1) UNSIGNED NOT NULL
    ) Engnine=Innodb charset=utf8;    
    """

    convert = Convert(
        sql_extractor=SqlExtractor(sql_text=sql_text)
    )
    result: IntDescriptor = convert.execute()[0]

    assert result.col_name == '_id'
    assert result.col_type == 'int'
    assert result.col_size == '(1)'
    assert result.is_unsigned is True
    assert result.is_null is False


def test_int_column_03():
    sql_text = """create table foo (
    _id int(1)  NOT NULL
    ) Engnine=Innodb charset=utf8;    
    """

    convert = Convert(
        sql_extractor=SqlExtractor(sql_text=sql_text)
    )
    result: IntDescriptor = convert.execute()[0]

    assert result.col_name == '_id'
    assert result.col_type == 'int'
    assert result.col_size == '(1)'
    assert result.is_unsigned is False
    assert result.is_null is False
