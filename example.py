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
