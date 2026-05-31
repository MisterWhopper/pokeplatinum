#!/usr/bin/env python3

from pathlib import Path
from string import Template

# The string to replace from the template file
MAGIC_STRING = "/* =========== MAGIC CONTENT MARKER =========== */"
LUT_ENTRY_TEMPLATE = Template("\t${itemName},")
BASE_PATH = Path(__file__).parent
TOP_PATH = BASE_PATH.parents[2]
INPUT_TEMPLATE = BASE_PATH.parent / "data" / "held_items.h.template"
BUILD_DIR = TOP_PATH / ".build"
OUTPUT_TARGET = BUILD_DIR / "generated" / INPUT_TEMPLATE.with_suffix("").name
HELD_ITEMS_TXT = TOP_PATH / "generated" / "held_items.txt"


def main():
    progress_item_data = HELD_ITEMS_TXT.read_text().splitlines()
    result = []
    for item in progress_item_data:
        result.append(LUT_ENTRY_TEMPLATE.substitute({"itemName": item}))
    original_content = INPUT_TEMPLATE.read_text()
    with open(OUTPUT_TARGET, "w+") as fout:
        fout.write(original_content.replace(MAGIC_STRING, "\n".join(result)))


if __name__ == "__main__":
    main()
