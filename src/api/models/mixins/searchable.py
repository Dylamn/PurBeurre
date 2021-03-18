class Searchable(object):
    """A simple mixin used by models that may need a `search` filter."""

    @classmethod
    def search(cls, string_input: str, operator='REGEXP'):
        """Apply a regexp constraint to the where clause on the name column."""

        # `REGEXP` operator works for MySQL and not for all SGBD.
        # For example, in PostgreSQL, it should be a tilde `~`.
        return cls.query.filter(cls.name.op(operator)(string_input))
