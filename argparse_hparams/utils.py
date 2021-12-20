import json
import yaml
import textwrap
from itertools import chain
from pathlib import Path


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


def load_yaml(path: Path):
    with open(path, "r") as f:
        # remove the blank at the end of lines
        lines = f.read().splitlines()
        data = "\n".join([l.rstrip() for l in lines])
        data = yaml.load(data, Loader=yaml.FullLoader) or {}

    # load the default (i.e. base) yaml of the current yaml
    # a left base will be overwriten by the right base
    if "default" in data:
        base_paths = data["default"]
        if not isinstance(base_paths, list):
            base_paths = [base_paths]
        for base_path in reversed(base_paths):
            if base_path.startswith("."):
                base_path = path.parent / base_path
            base_data = load_yaml(base_path)
            base_data.update(data)
            data = base_data
        del data["default"]

    return data


def to_val(x):
    if isinstance(x, (tuple, list)):
        return list(chain.from_iterable(map(to_val, x)))
    if isinstance(x, dict):
        return [json.dumps(x)]
    return [str(x)]


def to_key(k):
    return f"--{k.replace('_', '-')}"


def to_argv(k, v):
    argv = [to_key(k)]
    if v != "":
        argv.extend(to_val(v))
    return argv


def yaml2argv(path, ignored=[]):
    data = load_yaml(Path(path))
    for key in ignored:
        del data[key]
    argv = chain.from_iterable(to_argv(k, v) for k, v in data.items())
    return list(argv)
