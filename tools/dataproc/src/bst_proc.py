#!/usr/bin/env python3

import json
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from string import Template

# The string to replace from the template file
MAGIC_STRING = "/* =========== MAGIC CONTENT MARKER =========== */"
LUT_ENTRY_TEMPLATE = Template("\t// ${speciesIdentifier}\n\t${BST},")
BASE_PATH = Path(__file__).parent
TOP_PATH = BASE_PATH.parents[2]
INPUT_TEMPLATE = BASE_PATH.parent / "data" / "pokemon_bsts.h.template"
BUILD_DIR = TOP_PATH / ".build"
OUTPUT_TARGET = BUILD_DIR / "generated" / INPUT_TEMPLATE.with_suffix("").name
OUTPUT_JSON = TOP_PATH / "res" / "pokemon" / "bst_mapping.json"
SPECIES_TXT = TOP_PATH / "generated" / "species.txt"
DATA_DIR = TOP_PATH / "res" / "pokemon"


SPECIES_LIST: list[str] = SPECIES_TXT.read_text().splitlines()


@dataclass
class MonInfo:
    species_identifier: str
    species_number: int
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int

    @cached_property
    def bst(self):
        return sum(
            (
                self.hp,
                self.attack,
                self.defense,
                self.sp_attack,
                self.sp_defense,
                self.speed,
            )
        )

    @staticmethod
    def from_folder(folder: str | Path) -> "MonInfo":
        mon_path = folder if isinstance(folder, Path) else Path(folder)
        json_path = mon_path / "data.json"
        assert json_path.exists() and json_path.is_file(), (
            f"Supplied folder '{mon_path.name}' does not have the required data.json file for parsing."
        )
        json_data = json.loads(json_path.read_text())
        mon_identifier = f"SPECIES_{mon_path.stem.upper()}"
        species_number = SPECIES_LIST.index(mon_identifier)
        base_stats: dict[str, int] = json_data.get("base_stats", {})
        return MonInfo(
            species_identifier=mon_identifier,
            species_number=species_number,  # FIXME: How tf am I supposed to get this value
            hp=base_stats["hp"],
            attack=base_stats["attack"],
            defense=base_stats["defense"],
            sp_attack=base_stats["special_attack"],
            sp_defense=base_stats["special_defense"],
            speed=base_stats["speed"],
        )


def get_mon_data() -> list[MonInfo]:
    assert DATA_DIR.exists() and DATA_DIR.is_dir(), "Data folder not found"
    results = []
    for item in DATA_DIR.iterdir():
        if not (item.is_dir() and "data.json" in [i.name for i in item.iterdir()]):
            continue
        results.append(MonInfo.from_folder(item))
    return results


def main():
    mon_data = sorted(get_mon_data(), key=lambda m: m.species_number)
    define_strs = []
    for mon in mon_data:
        define_strs.append(
            LUT_ENTRY_TEMPLATE.substitute(
                {"speciesIdentifier": mon.species_identifier, "BST": str(mon.bst)}
            )
        )
    with open(OUTPUT_TARGET, "w+") as fout:
        new_content = INPUT_TEMPLATE.read_text().replace(
            MAGIC_STRING, "\n".join(define_strs)
        )
        fout.write(new_content)


if __name__ == "__main__":
    main()
