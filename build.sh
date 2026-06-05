#!/usr/bin/env bash

for i in "$@"; do 
    case $i in 
    --release=*)
        version="${i#*=}"
        echo -n "$version" > ./.version.txt
    esac
done

tools/dataproc/src/add_version.py

if !(podman image exists pokeplatinum-builder); then
    podman build -t pokeplatinum-builder:latest .
fi

podman run -t --rm --userns=keep-id -v ./:/app:Z pokeplatinum-builder:latest
if [[ -s ./.build/pokeplatinum.us.nds ]]; then
    mv ./.build/pokeplatinum.us.nds .
fi

if [[ -s ./.version.txt ]]; then
    rm ./.version.txt
fi

if [[ -s ./res/text/title_screen.json ]]; then
    rm ./res/text/title_screen.json
fi
