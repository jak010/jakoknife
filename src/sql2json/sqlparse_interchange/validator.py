from __future__ import annotations

from typing import TYPE_CHECKING

from sqlparse.tokens import Whitespace

if TYPE_CHECKING:
    from sqlparse.sql import Token


class TokenValidation:
    def is_whitespace(self, token: Token):
        return token.ttype == Whitespace

    def token_is_create(self, token: Token):
        return token.value == 'create'
