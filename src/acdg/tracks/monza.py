from acdg.tracks.data import TrackData

GEOMETRIES_TO_REMOVE = [
    "shadow_serraglio",
    "groove2",
    "groove2b",
    "tree_shadow",
    "horizont",
    "physics",
    "trees",
    "tree8",
    "misc_alphatest",
    "treesline",
    "branch5",
    "hedge",
    "bushes",
    "misc_alpha",
    "Bark",
    "antennas",
]

MATERIAL_TO_SEMANTIC_CLASS = {
    "groove": "drivable",
    "Pannello_Skin_00": "structure",
    "driver_face": "people",
    "driver_suit": "people",
    "Pitlane_Props_BASE": "structure",
    "whiteline": "track_limit",
    "grs_brd": "grass",
    "brd2": "road",
    "gstand-alpha": "structure",
    # "antennas": "structure",
    # "treesline": "vegetation",
    "fences2": "structure",
    "fences1": "structure",
    # "hedge": "vegetation",
    "paddk": "structure",
    "metals-alpha": "structure",
    # "branch5": "vegetation",
    # "trees": "vegetation",
    # "tree8": "vegetation",
    # "misc_alphatest": "vegetation",
    "serraglio": "structure",
    "flag1": "structure",
    "flag3": "structure",
    "flag4": "structure",
    "flag5": "structure",
    "flag6": "structure",
    "flag2": "structure",
    "flag7": "structure",
    "flag8": "structure",
    "top_new": "grass",
    "top_B": "grass",
    "apsh-shader-norm": "road",
    "asph-pitlane": "road",
    "grass-shader": "grass",
    "apsh-shader-mid": "road",
    "curb-NM": "curb",
    "curb-shader": "curb",
    "apsh-shader2": "road",
    "apsh-shader-scuro": "road",
    "gstand": "structure",
    "BBgrass": "grass",
    # "bushes": "vegetation",
    "lights": "structure",
    # "misc_alpha": "vegetation",
    "objects1": "vehicle",
    "marshall": "people",
    "Vehicles": "vehicle",
    "adv_add": "structure",
    "walls": "structure",
    "box_M": "structure",
    "metals": "structure",
    "tyres": "structure",
    "bridges": "structure",
    "wall2": "structure",
    "grille": "curb",
    # "Bark": "vegetation",
    "MB_Sprinter_2014": "vehicle",
    "box": "structure",
    "sand": "sand",
    "billboards": "structure",
    "glass": "structure",
    "glass_B": "structure",
    "misc1": "structure",
}

VERTEX_GROUPS_TO_MODIFY = [
    "AC_PIT",
    "AC_START",
    "AC_AUDIO",
    "HOT_LAP_START",
    "AC_POBJECT",
    "AC_TIME_ATTACK",
]


MONZA_DATA = TrackData(
    geometries_to_remove=GEOMETRIES_TO_REMOVE,
    vertex_groups_to_modify=VERTEX_GROUPS_TO_MODIFY,
    material_to_semantics=MATERIAL_TO_SEMANTIC_CLASS,
)