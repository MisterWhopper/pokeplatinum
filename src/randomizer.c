#include "randomizer.h"

#include "constants/items.h"
#include "generated/items.h"
#include "generated/pokemon_bsts.h"
#include "generated/progression_items.h"

#include "heap.h"
#include "inlines.h"
#include "item.h"
#include "species.h"

u16 Randomizer_GetSimilarBSTSpecies(u16 speciesId)
{
    u16 bst = Pokemon_BST_LUT[speciesId];
    u16 *buff = (u16 *)Heap_Alloc(HEAP_ID_SYSTEM, sizeof(u16) * SPECIES_ARCEUS);
    u16 counter = 0;
    for (u16 i = SPECIES_BULBASAUR; i <= SPECIES_ARCEUS; ++i) {
        u16 otherBST = Pokemon_BST_LUT[i];
        if (otherBST <= bst) {
            buff[counter++] = i;
        }
    }
    u16 result = counter > 0 ? buff[LCRNG_RandMod(counter)] : speciesId;
    Heap_Free(buff);
    return result;
}

u16 Randomizer_GetSpecies()
{
    // Make sure to only generate valid mons
    return LCRNG_RandMod(SPECIES_ARCEUS) + 1;
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

u16 Randomizer_GetItem()
{
    u16 result;
    // There are unfortunately unused item IDs, which are right in the heart of the smack of the dab
    // of our item ID range. So we have to do this nonsense and hope this doesn't lock up the game *too* horribly
    // and add a failsafe (a max repel) in case we loop for too long.
    u16 counter = 0;
    do {
        result = LCRNG_RandMod(MAX_ITEMS) + 1;
        counter++;
    } while (counter <= 1500 && (result >= ITEM_UNUSED_113 && result <= ITEM_UNUSED_134) || Item_ProgressesPlayer(result));
    return counter <= 1500 ? result : ITEM_MAX_REPEL;
}
