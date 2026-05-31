#!/usr/bin/env python3

from pathlib import Path
from sys import exit

BASE_PATH = Path(__file__).parent
ITEM_ICON_DIR = BASE_PATH.parent.parent / "res" / "items" / "icons"

PALETTE_OUTPUT_MAPPINGS = {
    ITEM_ICON_DIR / "rare_candy.pal": ITEM_ICON_DIR / "box_of_candy.pal",
    ITEM_ICON_DIR / "max_repel.pal": ITEM_ICON_DIR / "repellant_scent.pal",
}


def die(msg: str, error_code: int = 1):
    print(msg)
    exit(error_code)


def flip_gb_data(color_entry: str) -> str:
    numbers = list(map(int, color_entry.strip().split()))
    # There's def a 'smart' way to do this, but a little hardcoding never hurt anyone
    new_entry = [numbers[0], numbers[2], numbers[1]]
    return " ".join(str(n) for n in new_entry)


def main():
    for pal_in, pal_out in PALETTE_OUTPUT_MAPPINGS.items():
        if not pal_in.exists():
            die(f"ERROR: Could not find palette file at expected location ('{pal_in}')")
        content = pal_in.read_text()
        with open(pal_out, "w") as fout:
            lines = content.splitlines()
            for header in lines[:3]:
                fout.write(f"{header}\r\n")
            for line in lines[3:]:
                new_line = flip_gb_data(line)
                # nitrogfx.exe flips out if line endings aren't CRLF
                fout.write(f"{new_line}\r\n")


if __name__ == "__main__":
    main()
