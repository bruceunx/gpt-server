from pathlib import Path

Base = Path(__file__).resolve().parent.parent

APIs = {}

person_file = Base / '.person'

if person_file.is_file():
    with open(Base / ".person", "r") as f:
        for line in f.readlines():
            key, value = line.split("=")
            APIs[key] = value.strip()

    if 'proxy' not in APIs:
        APIs['proxy'] = None  # type: ignore
