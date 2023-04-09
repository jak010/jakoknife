class IntDescriptor:
    def __init__(self,
                 col_name,
                 col_type,
                 col_size,
                 is_unsigned: bool = False,
                 is_null: bool = False
                 ):
        self.col_name = col_name
        self.col_type = col_type
        self.col_size = col_size
        self.is_unsigned = is_unsigned
        self.is_null = is_null

    def set_unsigned(self, value):
        self.is_unsigned = value

    def set_null(self, value):
        self.is_null = value

    def __repr__(self):
        return f"IntColumn=(\n" \
               f" col_name={self.col_name},\n" \
               f" col_type={self.col_type},\n" \
               f" col_size={self.col_size},\n" \
               f" is_unsigned={self.is_unsigned},\n" \
               f" is_null={self.is_null})"


class ColumnDescriptor:
    def __init__(self, c_name, c_type, c_size, is_null):
        self.c_name = self.name_clear(c_name)
        self.c_type = str(c_type)
        self.c_size = c_size
        self.is_null = is_null

    def name_clear(self, c_name):
        if '`' in c_name:
            return c_name.replace('`', '')

    def __repr__(self):
        return f"SqlDataType=({self.c_name}, {self.c_type}, {self.is_null})"

    def to_dict(self):
        return f'"{self.c_name}":"{self.c_type}"'
