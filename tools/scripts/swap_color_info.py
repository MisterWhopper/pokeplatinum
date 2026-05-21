#!/usr/bin/env python3

from pathlib import Path
from shutil import copyfile
from sys import exit

BASE_PATH = Path(__file__).parent
ITEM_ICON_DIR = BASE_PATH.parent.parent / "res" / "items" / "icons"
CANDY_PALETTE = ITEM_ICON_DIR / "rare_candy.pal"
OUTPUT_PALETTE = ITEM_ICON_DIR / "box_of_candy.pal"
ICON_COPY_DEST = ITEM_ICON_DIR / "box_of_candy.png"


def die(msg: str, error_code: int = 1):
    print(msg)
    exit(error_code)


def flip_gb_data(color_entry: str) -> str:
    numbers = list(map(int, color_entry.strip().split()))
    # There's def a 'smart' way to do this, but a little hardcoding never hurt anyone
    new_entry = [numbers[0], numbers[2], numbers[1]]
    return " ".join(str(n) for n in new_entry)


def main():
    if not CANDY_PALETTE.exists():
        die(
            f"ERROR: Could not find rare candy palette file at expected location ('{CANDY_PALETTE}')"
        )
    content = CANDY_PALETTE.read_text()
    with open(OUTPUT_PALETTE, "w") as fout:
        lines = content.splitlines()
        for header in lines[:3]:
            fout.write(f"{header}\r\n")
        for line in lines[3:]:
            new_line = flip_gb_data(line)
            # nitrogfx.exe flips out if line endings aren't CRLF
            fout.write(f"{new_line}\r\n")

    if not (ICON_COPY_DEST.exists() and ICON_COPY_DEST.is_file()):
        copyfile(
            src=ITEM_ICON_DIR / CANDY_PALETTE.with_suffix("png"), dst=ICON_COPY_DEST
        )


if __name__ == "__main__":
    main()
