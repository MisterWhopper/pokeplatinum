#!/usr/bin/env bash
if (podman image exists pokeplatinum-builder); then
    podman run --rm --userns=keep-id -v ./:/app:Z pokeplatinum-builder:latest
    if [[ -s ./.build/pokeplatinum.us.nds ]]; then
        mv ./.build/pokeplatinum.us.nds .
    fi
else
    podman build -t pokeplatinum-builder:latest .
fi
