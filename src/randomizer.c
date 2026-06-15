#include "randomizer.h"

#include "constants/items.h"
#include "generated/held_items.h"
#include "generated/items.h"
#include "generated/pokemon_bsts.h"
#include "generated/progression_items.h"

#include "heap.h"
#include "inlines.h"
#include "item.h"
#include "moves.h"
#include "species.h"

static u16 *sLUTBuffer;

void Randomizer_Init()
{
    // Pre-create the buffer so we aren't constantly doing allocs & frees
    sLUTBuffer = (u16 *)Heap_Alloc(HEAP_ID_SYSTEM, sizeof(u16) * SPECIES_ARCEUS);
}

void Randomizer_Free()
{
    // When would we ever do this lol
    Heap_Free(sLUTBuffer);
}

static inline BOOL _Randomizer_IsUnusedItem(u16 item)
{
    return item >= ITEM_UNUSED_113 && item <= ITEM_UNUSED_134;
}

static inline BOOL _Randomizer_IsMailItem(u16 item)
{
    return item >= ITEM_GRASS_MAIL && item <= ITEM_BRICK_MAIL;
}

static BOOL _Randomizer_IsValidItem(u16 item)
{
    switch (item) {
    case ITEM_REVIVE:
    case ITEM_MAX_REVIVE:
    case ITEM_REVIVAL_HERB:
    case ITEM_REPEL:
    case ITEM_MAX_REPEL:
    case ITEM_SUPER_REPEL:
    case ITEM_MAGMA_STONE: // Does nothing
    case ITEM_CHERISH_BALL:
    case ITEM_CONTEST_PASS:
    case ITEM_RED_CHAIN:
    case ITEM_RULE_BOOK:
    case ITEM_SEAL_BAG:
        return FALSE;
    }
    return !(_Randomizer_IsUnusedItem(item) || Item_ProgressesPlayer(item) || _Randomizer_IsMailItem(item));
}

static BOOL _Randomizer_IsValidMove(u16 moveId)
{
    switch (moveId) {
    case MOVE_STRUGGLE:
    case MOVE_CUT:
    case MOVE_ROCK_SMASH:
    case MOVE_DEFOG:
    case MOVE_SURF:
    case MOVE_FLY:
    case MOVE_WATERFALL:
    case MOVE_STRENGTH:
        return FALSE;
    }
    return TRUE;
}

u16 Randomizer_GetSimilarBSTSpecies(u16 speciesId)
{
    u16 bst = Pokemon_BST_LUT[speciesId];
    u16 counter = 0;
    for (u16 i = SPECIES_BULBASAUR; i <= SPECIES_ARCEUS; ++i) {
        u16 otherBST = Pokemon_BST_LUT[i];
        if (otherBST <= bst) {
            sLUTBuffer[counter++] = i;
        }
    }
    u16 result = counter > 0 ? sLUTBuffer[LCRNG_RandMod(counter)] : speciesId;
    return result;
}

u16 Randomizer_GetSimilarBSTSpeciesWithThreshold(u16 speciesId, u16 threshold)
{
    u16 bst = Pokemon_BST_LUT[speciesId];
    u16 modifier = bst / threshold;
    u16 bstLowerBound = bst - modifier;
    u16 bstUpperBound = bst + modifier;
    u16 counter = 0;
    for (u16 i = SPECIES_BULBASAUR; i <= SPECIES_ARCEUS; ++i) {
        u16 otherBST = Pokemon_BST_LUT[i];
        if (otherBST <= bstUpperBound && otherBST >= bstLowerBound) {
            sLUTBuffer[counter++] = i;
        }
    }
    u16 result = counter > 0 ? sLUTBuffer[LCRNG_RandMod(counter)] : speciesId;
    return result;
}

u16 Randomizer_GetSpecies()
{
    // Make sure to only generate valid mons
    return LCRNG_RandMod(SPECIES_ARCEUS) + SPECIES_BULBASAUR;
}

u16 Randomizer_GetAbility()
{
    return LCRNG_RandMod(123) + 1;
}

u16 Randomizer_GetMove()
{
    // Ensure we never accidentally give a mon Struggle as an actual learnset move
    u16 result;
    u16 counter = 0;
    do {
        result = LCRNG_RandMod(MAX_MOVES) + 1;
        counter++;
    } while (counter <= 1500 && !_Randomizer_IsValidMove(result));
    // The odds of rolling Struggle 1500 times in a row are basically zero, but defense-in-depth or w/e
    return (counter <= 1500 && _Randomizer_IsValidMove(result)) ? result : MOVE_TACKLE;
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
    } while (counter <= 1500 && !_Randomizer_IsValidItem(result));
    return (counter <= 1500 && _Randomizer_IsValidItem(result)) ? result : ITEM_MAX_POTION;
}

u16 Randomizer_GetHeldItem()
{
    u16 result;
    u16 counter = 0;
    do {
        result = Item_Held_LUT[LCRNG_RandMod(NELEMS(Item_Held_LUT))];
    } while (counter <= 1500 && !_Randomizer_IsValidItem(result));
    return (counter <= 1500 && _Randomizer_IsValidItem(result)) ? result : ITEM_SITRUS_BERRY;
}
