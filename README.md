# Argparse HParams

> A simple argument parser for hyper-parameters.

## Installation

From PyPI:

```
pip install argparse-hparams
```

From Github:

```
pip install git+https://github.com/enhuiz/argparse-hparams.git
```

## Example

```python
from argparse_hparams import dataclass, HParams, Annotated, Flag
from dataclasses import dataclass, field


@dataclass
class HParamsTest(HParams):
    # This will call: parser.add_argument(type=int, default=0)
    x: int = 0

    # You may annotate custom data for parser.add_argument(...).
    # The annotated default will overwrite dataclass default
    # This will call: parser.add_argument(type=str.upper, default='bad')
    y: Annotated[str, dict(type=str.upper, default="bad")] = "good"

    # This will call: parser.add_argument(type=int, nargs=2, default=(2, 3))
    pair: Annotated[tuple[int, int], dict(type=int, nargs=2)] = (2, 3)

    # This will call: parser.add_argument(action="store_true", default=False)
    ok: Flag = False

    # When positional is set, the argument is a positional argument instead of an option
    # i.e., there will be no '--' added before the name when calling parser.add_argument
    pos: Annotated[str, dict(positional=True)] = ""

    # Dict is parsed using json.loads
    payload: dict = field(default_factory=dict)


if __name__ == "__main__":
    # Priority: dataclass default < annotated default < YAML default < manually specified value (sys.argv)
    test = HParamsTest()
    test.show(sort=True)
```

```
$ python example.py
usage: example.py [-h] [--x int] [--y upper] [--pair int int] [--ok] [--payload dict_parser] [--default Path] str
example.py: error: the following arguments are required: pos

$ python example.py 123
┌────────────┐
│  HParams   │
├────────────┤
│ok: False   │
│pair: (2, 3)│
│payload: {} │
│pos: 123    │
│x: 0        │
│y: BAD      │
└────────────┘

$ python example.py --default default.yml 123
┌────────────────────────────────────────────────┐
│                    HParams                     │
├────────────────────────────────────────────────┤
│ok: False                                       │
│pair: [4, 5]                                    │
│payload: {'some': 'payload', 'here': 'for test'}│
│pos: 123                                        │
│x: 0                                            │
│y: 1                                            │
└────────────────────────────────────────────────┘

$ python example.py --help
usage: example.py [-h] [--x int] [--y upper] [--pair int int] [--ok] [--payload dict_parser] [--default Path] str

positional arguments:
  str                   pos

optional arguments:
  -h, --help            show this help message and exit
  --x int               x (default: 0)
  --y upper             y (default: bad)
  --pair int int        pair (default: (2, 3))
  --ok                  ok (default: False)
  --payload dict_parser
                        payload (default: {})
  --default Path        A YAML configuration file that overrides the defaults (default: None)

$ python example.py --payload '{"oops": "it is overwriten."}' --default default.yml 123
┌──────────────────────────────────────┐
│               HParams                │
├──────────────────────────────────────┤
│ok: False                             │
│pair: [4, 5]                          │
│payload: {'oops': 'it is overwriten.'}│
│pos: 123                              │
│x: 0                                  │
│y: 1                                  │
└──────────────────────────────────────┘
```
