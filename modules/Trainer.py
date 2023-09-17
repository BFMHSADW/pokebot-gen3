import struct

from modules.Console import console
from modules.Memory import GetSaveBlock, ReadSymbol, DecodeString


def FacingDir(direction: int) -> str:
    """
    Returns the direction the trainer is currently facing.

    :param direction: int
    :return: trainer facing direction (str)
    """
    match direction:
        case 0x11:
            return 'Down'
        case 0x22:
            return 'Up'
        case 0x33:
            return 'Left'
        case 0x44:
            return 'Right'


b_Save = GetSaveBlock(2, size=14)  # TODO temp fix, sometimes fails to read pointer if GetTrainer() called before game boots after a reset
def GetTrainer() -> dict:
    """
    Reads trainer data from memory.
    See: https://bulbapedia.bulbagarden.net/wiki/Save_data_structure_(Generation_III)#Section_0_-_Trainer_Info

    name: Trainer's (decoded) name
    gender: boy/girl
    tid: Trainer ID
    sid: Secret ID
    state: ??
    map: tuple (`MapBank`, `MapID`)
    coords: tuple (`xPos`, `yPos`)
    facing: trainer facing direction `Left`/`Right`/`Down`/`Up`
    :return: Trainer (dict)
    """
    try:
        b_gTasks = ReadSymbol('gTasks', 0x57, 3)
        b_gObjectEvents = ReadSymbol('gObjectEvents', 0x10, 9)
        trainer = {
            'name': DecodeString(b_Save[0:7]),
            'gender': 'girl' if int(b_Save[8]) else 'boy',
            'tid': int(struct.unpack('<H', b_Save[10:12])[0]),
            'sid': int(struct.unpack('<H', b_Save[12:14])[0]),
            'map': (int(b_gTasks[2]), int(b_gTasks[1])),
            'coords': (int(b_gObjectEvents[0]) - 7, int(b_gObjectEvents[2]) - 7),
            'facing': FacingDir(int(b_gObjectEvents[8]))
        }
        return trainer
    except:
        console.print_exception(show_locals=True)