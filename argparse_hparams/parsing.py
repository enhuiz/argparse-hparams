import json
from typing import Annotated, Union, Optional, get_args, get_origin
from collections import defaultdict


def get_annotation(t):
    ret = {}
    origin = get_origin(t)
    if origin is Annotated:
        data = get_args(t)[1]
        if isinstance(data, dict):
            ret = data
    return ret


def check_literals(s, literals):
    if s.lower() not in literals:
        raise ValueError(f"s.lower() shoud be within {literals}")


def bool_parser(s):
    check_literals(s, ["true", "false"])
    return s.lower() == "true"


def none_parser(s):
    check_literals(s, ["none", "null"])
    return None


def dict_parser(s):
    return json.loads(s)


def get_parser(t):
    origin = get_origin(t)

    parser = None

    # special handle for basic types
    if t is bool:
        parser = bool_parser
    elif t is type(None):
        parser = none_parser
    elif t is dict:
        parser = dict_parser
    elif origin is None:
        # default parser of the basic type is itself
        parser = t
    # composite types
    elif origin is Annotated:
        data = get_annotation(t)
        parser = data.get("type", None)
        parser = parser or get_parser(get_args(t)[0])
    elif origin is Union:
        priority = defaultdict(lambda: 0, {type(None): 1})
        parser = union_parsers(
            *map(
                get_parser,
                sorted(
                    get_args(t),
                    key=lambda t: priority[t],
                    reverse=True,
                ),
            )
        )

    if parser is None:
        raise NotImplementedError(f"Parser for {t} is not implemented.")

    return parser


def union_parsers(*parsers):
    def parse(s):
        lines = []
        for parser in parsers:
            try:
                return parser(s)
            except Exception as e:
                lines.append(f"\t{parser.__name__}: {str(e)}")
        raise ValueError("union_parsers: \n" + "\n".join(lines))

    return parse


if __name__ == "__main__":
    assert get_parser(Optional[bool])("None") == None
    assert get_parser(bool)("true") == True
    assert get_parser(Annotated[float, ""])("235.5") == 235.5
    assert get_parser(Union[bool, float])("235.5") == 235.5
    assert get_parser(Union[bool, int])("235.5") == 235.5
