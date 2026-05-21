import json
from pathlib import Path

BASE_PATH = Path(__file__).parent
MONDATA_DIR = BASE_PATH.parent.parent / "res" / "pokemon"


def is_valid_mondir(item: Path):
    return item.is_dir() and "data.json" in [f.name for f in item.iterdir()]


def try_fetch_json_path(data: dict, path: str) -> str | None:
    path_components = path.split(".")
    next = data
    for p in path_components[:-1]:
        item = next.get(p)
        if item is None:
            return None
        else:
            next = item
    result = next.get(path_components[-1])
    return result


def update_mon(item: Path):
    target = item / "data.json"
    data = json.loads(target.read_text())
    current_name = try_fetch_json_path(data, "pokedex_data.en.name")
    if current_name is not None:
        new_name = current_name.title()
        print(f"{item.name}: '{current_name}' => '{new_name}'")
        with open(target, "w") as fout:
            data["pokedex_data"]["en"]["name"] = new_name
            fout.write(json.dumps(data, indent=2))


def main():
    for child in MONDATA_DIR.iterdir():
        if is_valid_mondir(child):
            update_mon(child)


if __name__ == "__main__":
    main()
