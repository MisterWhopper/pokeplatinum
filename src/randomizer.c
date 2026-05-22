#include "randomizer.h"

#include "generated/pokemon_bsts.h"

#include "heap.h"
#include "inlines.h"
#include "species.h"

u16 Randomizer_GetSimilarBSTSpecies(u16 speciesId)
{
    u16 bst = Pokemon_BSTLUT[speciesId];
    u16 *buff = (u16 *)Heap_Alloc(HEAP_ID_SYSTEM, sizeof(u16) * 492);
    u16 counter = 0;
    for (u16 i = SPECIES_BULBASAUR; i <= SPECIES_ARCEUS; ++i) {
        u16 otherBST = Pokemon_BSTLUT[i];
        if (otherBST <= bst) {
            buff[counter++] = i;
        }
    }
    u16 result = buff[LCRNG_RandMod(counter)];
    Heap_Free(buff);
    return result;
}

u16 Randomizer_GetSpecies()
{
    // Make sure to only generate valid mons
    return LCRNG_RandMod(493) + 1;
}

u16 Randomizer_GetAbility()
{
    // return LCRNG_RandMod(lengthof__Abilities);
    return LCRNG_RandMod(124) + 1;
}

u16 Randomizer_GetMove()
{
    // return LCRNG_RandMod(lengthof__Moves);
    return LCRNG_RandMod(469) + 1;
}
