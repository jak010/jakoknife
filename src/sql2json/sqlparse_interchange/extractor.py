from __future__ import annotations

from functools import cached_property
from typing import Tuple, TYPE_CHECKING, List, Union

import sqlparse
from sqlparse.sql import Identifier
from sqlparse.sql import Parenthesis
from sqlparse.tokens import Whitespace

from .validator import TokenValidation

if TYPE_CHECKING:
    from sqlparse.sql import Statement
    from sqlparse.sql import Token


class SqlExtractor:

    def __init__(self, sql_text):
        self.sql_text = sql_text

    @cached_property
    def validator(self) -> TokenValidation:
        return TokenValidation()

    @property
    def _parse(self) -> Tuple[Statement]:
        return sqlparse.parse(self.sql_text)

    @property
    def get_token(self) -> Tuple[Token]:
        # TODO: parse 결과에서 무조건 첫 번쨰를 꺼내오는 것, SQL 파일에 DDL이 복수개라면 적절한 처리가 필요함
        return tuple(sqlparse.sql.TokenList(self._parse[0].tokens))

    @property
    def columns(self) -> List[str]:
        return [
            x.strip() for x in self._get_parenthesis().value.split("\n")
            if not (x.startswith('(') or x.startswith(')'))
        ]

    def _get_parenthesis(self) -> Parenthesis:
        """ DDL에서 '()' 안에 들어있는 Columns 리턴 """
        for sql in self._extract():
            if isinstance(sql, Parenthesis):
                return sql

    def _extract(self) -> List[Union[Identifier, Token, Parenthesis]]:
        sqls = []
        for token in self.get_token:
            if not self.validator.is_whitespace(token):
                sqls.append(token)
        return sqls
