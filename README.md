# Argparse HParams

> A simple argparser for HParams.

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


if __name__ == "__main__":
    test = HParamsTest()
    test.show()
```

Outputs:

```
┌────────────┐
│ Arguments  │
├────────────┤
│x: 0        │
│y: BAD      │
│pair: (2, 3)│
│ok: False   │
└────────────┘
```
