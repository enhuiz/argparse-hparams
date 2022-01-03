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


def _load_yaml_recursively(path: Path, base_key):
    with open(path, "r") as f:
        # remove the blank at the end of lines
        lines = f.read().splitlines()
        data = "\n".join([l.rstrip() for l in lines])
        data = yaml.load(data, Loader=yaml.FullLoader) or {}

    # load the default (i.e. base) yaml of the current yaml
    # a left base will be overwriten by the right base
    if base_key in data:
        base_paths = data[base_key]
        if not isinstance(base_paths, list):
            base_paths = [base_paths]
        for base_path in reversed(base_paths):
            if base_path.startswith("."):
                base_path = path.parent / base_path
            base_data = _load_yaml_recursively(base_path, base_key)
            base_data.update(data)
            data = base_data
        del data[base_key]

    return data


def load_yaml(path: Path, base_key: str = "default", delete_flag: str = "<del>"):
    """
    Load yaml recursively.

    Args:
        path: the yaml file where to start loading.
        base_key: where is the base yaml paths stored.
        delete_flag: if the value equals the delete_flag, delete the entry
    """
    data = _load_yaml_recursively(path, base_key)

    for k, v in list(data.items()):
        if v == delete_flag:
            del data[k]

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
