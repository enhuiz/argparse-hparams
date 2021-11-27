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

    # when positional is set, the argument is a positional argument
    pos: Annotated[str, dict(positional=True)] = ""


if __name__ == "__main__":
    test = HParamsTest()
    test.show()
```

```
$ python example.py
usage: example.py [-h] [--x int] [--y upper] [--pair int int] [--ok] [--default Path] str
example.py: error: the following arguments are required: pos

$ python example.py 123
┌────────────┐
│  HParams   │
├────────────┤
│x: 0        │
│y: BAD      │
│pair: (2, 3)│
│ok: False   │
│pos: 123    │
└────────────┘

$ python example.py --default default.yml 123
┌────────────┐
│  HParams   │
├────────────┤
│x: 0        │
│y: 1        │
│pair: [4, 5]│
│ok: False   │
│pos: 123    │
└────────────┘

$ python example.py --help
usage: example.py [-h] [--x int] [--y upper] [--pair int int] [--ok] [--default Path] str

positional arguments:
  str             pos

optional arguments:
  -h, --help      show this help message and exit
  --x int         x (default: 0)
  --y upper       y (default: bad)
  --pair int int  pair (default: (2, 3))
  --ok            ok (default: False)
  --default Path  A YAML configuration file that overrides the defaults (default: None)
```
