import yaml
import textwrap
from itertools import chain


def message_box(title, content, aligner="<", max_width=70):
    lines = [textwrap.shorten(line, width=max_width) for line in content.splitlines()]

    width = max(map(len, [title] + lines)) + 2

    nb = width - 2  # number of blanks
    border = f"│{{: ^{nb}}}│"

    out = []
    out.append("┌" + "─" * nb + "┐")
    out.append(border.format(title))
    out.append("├" + "─" * nb + "┤")

    for line in lines:
        out.append(border.replace("^", aligner).format(line.strip()))

    out.append("└" + "─" * nb + "┘")

    return "\n".join(out)


def load_yaml(path):
    with open(path, "r") as f:
        # remove the blank at the end of lines
        lines = f.read().splitlines()
        data = "\n".join([l.rstrip() for l in lines])
        data = yaml.load(data, Loader=yaml.FullLoader) or {}

    for key in list(data.keys()):
        if type(data[key]) is dict:
            del data[key]

    # load the default (i.e. base) yaml of the current yaml
    # a left base will be overwriten by the right base
    if "default" in data:
        bases = data["default"]
        if not isinstance(bases, list):
            bases = [bases]
        for base in reversed(bases):
            base = load_yaml(base)
            base.update(data)
            data = base
        del data["default"]

    return data


def to_val(x):
    if isinstance(x, (tuple, list)):
        return list(chain.from_iterable(map(to_val, x)))
    return [str(x)]


def to_key(k):
    return f"--{k.replace('_', '-')}"


def to_argv(k, v):
    argv = [to_key(k)]
    if v != "":
        argv.extend(to_val(v))
    return argv


def yaml2argv(path, ignored=[]):
    data = load_yaml(path)
    for key in ignored:
        del data[key]
    argv = chain.from_iterable(to_argv(k, v) for k, v in data.items())
    return list(argv)
