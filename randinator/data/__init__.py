from pathlib import Path


def get_package_filepath(filename: str | Path) -> Path:
    here = Path(__file__).resolve().parent
    filenames = list(map(lambda f: f.name, here.glob("*.txt")))
    assert filename in filenames, f"{filename=} not available"
    return Path(__file__).resolve().parent / filename
