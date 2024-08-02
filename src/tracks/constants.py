from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class ClassInformation:
    name: str
    train_id: int
    colour: Tuple[int]


SEMANTIC_CLASSES = [
    ClassInformation("drivable", 0, (0, 255, 249)),
    ClassInformation("road", 1, (84, 84, 84)),
    ClassInformation("curb", 2, (255, 119, 51)),
    ClassInformation("track_limit", 3, (255, 255, 255)),
    ClassInformation("sand", 4, (255, 255, 0)),
    ClassInformation("grass", 5, (170, 255, 128)),
    ClassInformation("vehicle", 6, (255, 42, 0)),
    ClassInformation("structure", 7, (153, 153, 255)),
    ClassInformation("people", 8, (255, 179, 204)),
    ClassInformation("vegetation", 9, (0, 255, 238)),
    ClassInformation("carpet", 10, (0, 102, 17)),
    ClassInformation("water", 11, (0, 0, 255)),
    ClassInformation("void", -1, (0, 0, 0)),
]

SEMANTIC_NAME_TO_COLOUR = {info.name: info.colour for info in SEMANTIC_CLASSES}
SEMANTIC_NAME_TO_ID = {info.name: info.train_id for info in SEMANTIC_CLASSES}

COLOUR_LIST = [
    info.colour
    for info in sorted(SEMANTIC_CLASSES, key=lambda x: x.train_id)
    if info.train_id > -1
]
COLOUR_LIST.append(SEMANTIC_CLASSES[-1].colour)
COLOUR_LIST = np.asarray(COLOUR_LIST, dtype=np.uint8)

TRAIN_ID_LIST = [
    info.train_id
    for info in sorted(SEMANTIC_CLASSES, key=lambda x: x.train_id)
    if info.train_id > -1
]
TRAIN_ID_LIST.append(SEMANTIC_CLASSES[-1].train_id)
TRAIN_ID_LIST = np.asarray(TRAIN_ID_LIST, dtype=np.int8)
