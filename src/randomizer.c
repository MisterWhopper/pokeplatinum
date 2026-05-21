#include "randomizer.h"

// #include "generated/abilities.h"
// #include "generated/moves.h"
// #include "generated/species.h"
#include "inlines.h"

u16 GetRandomMonSpecies() {
    //return LCRNG_RandMod(lengthof__Species);
    return LCRNG_RandMod(496);
}

u16 GetRandomMonAbility() {
    //return LCRNG_RandMod(lengthof__Abilities);
    return LCRNG_RandMod(124);
}

u16 GetRandomMonMove() {
     //return LCRNG_RandMod(lengthof__Moves);
    return LCRNG_RandMod(469);
}
