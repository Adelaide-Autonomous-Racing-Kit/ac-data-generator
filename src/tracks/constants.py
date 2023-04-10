from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class ClassInformation:
    name: str
    train_id: int
    colour: Tuple[int]


SEMANTIC_CLASSES = [
    ClassInformation("road", 0, (84, 84, 84)),
    ClassInformation("curb", 1, (255, 119, 51)),
    ClassInformation("track_limit", 2, (255, 255, 255)),
    ClassInformation("sand", 3, (255, 255, 0)),
    ClassInformation("grass", 4, (170, 255, 128)),
    ClassInformation("vehicle", 5, (255, 42, 0)),
    ClassInformation("structure", 6, (153, 153, 255)),
    ClassInformation("vegetation", 7, (0, 255, 238)),
    ClassInformation("people", 8, (255, 179, 204)),
    ClassInformation("carpet", 9, (0, 102, 17)),
    ClassInformation("water", 10, (0, 0, 255)),
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
TRAIN_ID_LIST = np.asarray(TRAIN_ID_LIST, dtype=np.uint8)
