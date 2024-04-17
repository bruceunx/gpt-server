from pathlib import Path

Base = Path(__file__).resolve().parent.parent

APIs = {}
with open(Base / ".person", "r") as f:
    for line in f.readlines():
        key, value = line.split("=")
        APIs[key] = value.strip()
