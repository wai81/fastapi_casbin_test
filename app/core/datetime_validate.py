import sys
from datetime import datetime, timezone

from pydantic.datetime_parse import parse_datetime


class DatetimeConvert(datetime):
    @classmethod
    def __get_validators__(cls):
        yield parse_datetime  # default Pydantic behavior
        yield cls.validate

    @classmethod
    def validate(cls, value) -> str:
        print(value.tzinfo)
        print(value)
        if isinstance(value, datetime):
            print('Some request sends datetime not in UNIX format', file=sys.stderr)
            return value.replace(tzinfo=None)
        elif isinstance(value, int):
            return datetime.fromtimestamp(v)
        assert False, 'Datetime came of %s type' % type(value)


