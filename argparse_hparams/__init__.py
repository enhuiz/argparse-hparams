import sys
import argparse
from argparse import MetavarTypeHelpFormatter, ArgumentDefaultsHelpFormatter
from dataclasses import dataclass, fields
from pathlib import Path

from .parsing import Annotated, get_parser, get_annotation
from .utils import message_box, yaml2argv

Flag = Annotated[bool, dict(action="store_true", default=False)]


class DefaultFormatter(MetavarTypeHelpFormatter, ArgumentDefaultsHelpFormatter):
    pass


@dataclass
class HParams:
    def __post_init__(self):
        parser = argparse.ArgumentParser(formatter_class=self.formatter_class)

        for field in fields(type(self)):
            annotation = get_annotation(field.type)

            positional = False
            if "positional" in annotation:
                positional = annotation["positional"]
                del annotation["positional"]

            kwargs = {
                "default": getattr(self, field.name),
                "help": field.name,
            }
            if field.type is not Flag:
                kwargs["type"] = get_parser(field.type)
            kwargs.update(annotation)

            parser.add_argument(
                ("" if positional else "--") + f"{field.name.replace('_', '-')}",
                **kwargs,
            )

        parser.add_argument(
            "--default",
            type=Path,
            default=None,
            help="A YAML configuration file that overrides the defaults",
        )

        args = parser.parse_args()

        if args.default:
            # priority: default < YAML default < sys.argv
            argv = yaml2argv(args.default) + sys.argv[1:]
            args = parser.parse_args(argv)

        for field in fields(type(self)):
            setattr(self, field.name, getattr(args, field.name))

    @property
    def formatter_class(self):
        return DefaultFormatter

    def show(self, sort=False):
        args = [f"{k}: {v}" for k, v in vars(self).items()]
        if sort:
            args = sorted(args)
        print(message_box("HParams", "\n".join(args)))
