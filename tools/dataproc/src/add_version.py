#!/usr/bin/env python3
from dataclasses import dataclass
from pathlib import Path
from string import Template
import subprocess
from sys import exit

BASE_PATH = Path(__file__).parent
PROJ_PATH = BASE_PATH.parents[2]
TARGET_FILE = PROJ_PATH / "res" / "text" / "title_screen.json"
TEMPLATE_FILE = BASE_PATH.parent / "data" / "title_screen.json.template"
VERSION_FILE = PROJ_PATH / ".version.txt"


@dataclass
class GitData:
    last_commit: str
    is_synced: bool


def try_get_git_short_hash() -> GitData:
    try:
        sha_proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"], check=True, capture_output=True
        )
        status_proc = subprocess.run(
            ["git", "status", "--short"], check=True, capture_output=True
        )
    except Exception as err:
        print(f"ERROR: {err}")
        exit(1)
    else:
        return GitData(
            last_commit=sha_proc.stdout.decode().strip(),
            is_synced=len(status_proc.stdout.decode().strip()) == 0,
        )


def try_get_version() -> str:
    if VERSION_FILE.exists() and VERSION_FILE.is_file():
        return f"v{VERSION_FILE.read_text()}"
    git_data = try_get_git_short_hash()
    return f"{'*' if not git_data.is_synced else ''}git-{git_data.last_commit}"


def main():
    if TEMPLATE_FILE.exists() and TEMPLATE_FILE.is_file():
        content = TEMPLATE_FILE.read_text()
        if len(content) != 0:
            tmpl = Template(content)
            version_str = try_get_version()
            new_content = tmpl.substitute({"version": version_str})
            TARGET_FILE.write_text(new_content)


if __name__ == "__main__":
    main()
