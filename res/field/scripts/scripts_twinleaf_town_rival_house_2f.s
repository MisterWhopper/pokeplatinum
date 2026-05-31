#include "macros/scrcmd.inc"
#include "res/text/bank/twinleaf_town_rival_house_2f.h"
#include "res/field/events/events_twinleaf_town_rival_house_2f.h"


    ScriptEntry TwinleafTownRivalHouse2F_RivalNoticesPlayerAndLeaves
    ScriptEntry TwinleafTownRivalHouse2F_Wii
    ScriptEntry TwinleafTownRivalHouse2F_PC
    ScriptEntryEnd

TwinleafTownRivalHouse2F_RivalNoticesPlayerAndLeaves:
    LockAll
    RemoveObject LOCALID_RIVAL
    ReleaseAll
    End

    .balign 4, 0
TwinleafTownRivalHouse2F_Movement_RivalNoticePlayer:
    WalkOnSpotNormalWest
    EmoteExclamationMark
    EndMovement

    .balign 4, 0
TwinleafTownRivalHouse2F_Movement_RivalLeave:
    WalkFastWest 4
    WalkFastNorth
    WalkFastWest 3
    SetInvisible
    EndMovement

    .balign 4, 0
TwinleafTownRivalHouse2F_Movement_PlayerMoveAwayFromStairs:
    Delay8 2
    WalkNormalSouth
    WalkOnSpotNormalNorth
    EndMovement

TwinleafTownRivalHouse2F_Wii:
    EventMessage TwinleafTownRivalHouse2F_Text_ItsAWii
    End

TwinleafTownRivalHouse2F_PC:
    PlaySE SEQ_SE_CONFIRM
    LockAll
    BufferPlayerName 0
    Message TwinleafTownRivalHouse2F_Text_PCAdventureRules
    WaitButton
    CloseMessage
    ReleaseAll
    End

    .balign 4, 0
