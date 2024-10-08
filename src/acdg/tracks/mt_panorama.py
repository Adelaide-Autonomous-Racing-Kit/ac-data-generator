from acdg.tracks.data import TrackData

GEOMETRIES_TO_REMOVE = [
    "110",
    "asphalt_COLOR_0",
    "contrails",
    "groove",
    "KERBDECAL",
    "MARBLES",
    "NODE",
    "None__wood1_dds",
    "physics",
    "80",
    "Tree_Tropical_Pruned",
    "Treewall_Cap",
    "Oak_Monterrey_001",
    "Prototype_VEG_X_Tree_A_001",
    "G_Bush_Hedge_A_Trimmed_Leaf_",
    "VEG_Bush_Hedge_A_Trimmed_001_VEG_Bush_Hedge_A_Trimmed_Leaf_",
    "VEG_Bush_Hedge_A_Trimmed_Leaf_001_veg_bush_hedge_a_trim_b4c",
    "VEG_BUSH_Leafy_A_Trimmed_001",
    "VEG_Bush_Shrub_A_GroundCover_Leaves_001",
    "VEG_FM6_X_Plant_Flower_A_GroundCover_Leaves_001",
    "Veg_Nurb_Tree_Pine_B_Xlarge_Background_002",
    "VEG_Nurb_X_Bush_Common_B_Medium_001",
    "VEG_Nurb_X_Bush_Small_B_Wide_001",
    "VEG_Nurb_X_Tree_Common_A_Medium",
    "VEG_Nurb_X_Tree_Common_C_Medium_002",
    "VEG_Nurb_X_tree_Oak_C_Large_001",
    "VEG_Nurb_X_Tree_Pine_A_001",
    "VEG_Nurb_X_Tree_Pine_A_Thick_001",
    "VEG_Nurb_X_Tree_Pine_A_Thin_001",
    "Veg_Nurb_x_Tree_Pine_B_Xlarge_001",
    "VEG_Nurb_X_Tree_Poplar_C_Background_001",
    "VEG_Plant_Ivy_A_Leaf",
    "VEG_Tree_Maple_A_Tall_Bark_001_veg_bush_hedge_a_trimmed_25e",
    "VEG_X_Bush_A_001",
    "VEG_X_Bush_A_002",
    "VEG_X_Bush_Common_A_Large_001",
    "VEG_X_Bush_Common_C_Large_001",
    "VEG_X_Bush_Leafy_A_Medium_001",
    "VEG_X_Bush_Leafy_D_Medium_001",
    "VEG_X_Bush_Pine_B_001",
    "VEG_X_Bush_Shrub_B_GroundCover_001",
    "VEG_X_Plant_Flower_A_GroundCover_001",
    "VEG_X_Tree_Oak_B_Large_001",
    "VEG_X_Tree_Pine_B_Stone_001",
    "VEG_X_Tree_Pine_B_Tall_Sparse",
    "VEG_X_Tree_Pine_C_Stone_001",
    "VEG_X_Tree_Pine_D_Stone_001",
]

MATERIAL_TO_SEMANTIC_CLASS = {
    "100": "structure",
    "101": "road",
    "103": "structure",
    "105": "structure",
    "106": "structure",
    "107": "structure",
    "108": "structure",
    "109": "structure",
    "11": "structure",
    # "110": "structure",
    "111": "structure",
    "112": "structure",
    "113": "road",
    "114": "structure",
    "116": "structure",
    "117": "structure",
    "12": "structure",
    "13": "structure",
    "14": "structure",
    "15": "structure",
    "16": "structure",
    "17": "structure",
    "18": "structure",
    "2": "structure",
    "20": "structure",
    "21": "structure",
    "22": "structure",
    "24": "grass",
    "26": "road",
    "27": "structure",
    "29": "structure",
    "3": "structure",
    "30": "structure",
    "32": "structure",
    "34": "structure",
    "35": "structure",
    "36": "sand",
    "37": "structure",
    "38": "grass",
    "4": "structure",
    "41": "road",
    "42": "grass",
    "43": "structure",
    "44": "structure",
    "45": "structure",
    "46": "structure",
    "47": "structure",
    "48": "structure",
    "49": "structure",
    "5": "structure",
    "50": "structure",
    "51": "structure",
    "52": "structure",
    "53": "structure",
    "54": "structure",
    "56": "structure",
    "57": "structure",
    "58": "road",
    "59": "grass",
    "6": "structure",
    "60": "grass",
    "61": "structure",
    "62": "structure",
    "63": "structure",
    "65": "road",
    "66": "curb",
    "67": "structure",
    "69": "road",
    "7": "structure",
    "70": "grass",
    "71": "structure",
    "72": "structure",
    "73": "structure",
    "74": "structure",
    "75": "structure",
    "76": "road",
    "77": "structure",
    "78": "structure",
    "79": "track_limit",
    "8": "structure",
    "81": "grass",
    "82": "grass",
    "82nograss": "grass",
    "83": "grass",
    "84": "structure",
    "85": "structure",
    "86": "structure",
    "87": "structure",
    "88": "grass",
    "89": "structure",
    "9": "structure",
    "90": "structure",
    "91": "grass",
    "92": "structure",
    "95": "structure",
    "96": "road",
    "99": "structure",
    "75": "structure",
    "balloon_flame": "structure",
    "baloon": "structure",
    "blackgridfence": "structure",
    "blackmetalfence": "structure",
    "boardspoly": "structure",
    "boardspoly": "structure",
    "CarGlass_COLOR_0": "vehicle",
    "CargoBoxTent_COLOR_0": "structure",
    "CoastGuardHelicopter": "vehicle",
    "CoastGuardHelicopter_Glass": "vehicle",
    "decal2": "structure",
    "DECALSSMASH": "structure",
    "Default": "vehicle",
    "drivable": "drivable",
    "fire": "vehicle",
    "Gazebo_Tent": "structure",
    "GENERIC_tent_COLOR_0": "structure",
    "GENERIC_Truck_Block_COLOR_0": "vehicle",
    "heligreen": "vehicle",
    "helired": "vehicle",
    "heliwhite": "vehicle",
    "Hughes500_Body": "vehicle",
    "Hughes500_Glass": "vehicle",
    "Hughes500_GreenLight": "vehicle",
    "Hughes500_RedLight": "vehicle",
    "Hughes500_WhiteLights": "vehicle",
    "ignition": "vehicle",
    "marshall": "people",
    "Material_#4": "structure",
    "Material_#5": "structure",
    "MI_ambulance": "vehicle",
    "MI_jersey": "structure",
    "MI_service_COLOR_0": "vehicle",
    "NEW_SKYRING2": "grass",
    "ParkingCars_COLOR_0": "vehicle",
    "pzero4": "vehicle",
    "REDLINE": "track_limit",
    "REDSTARTLIGHTS": "structure",
    "rotax": "vehicle",
    "Rotor": "vehicle",
    "Rotor2": "vehicle",
    "SANDEDGES": "grass",
    "sbanc2": "structure",
    "servicetruck_2": "vehicle",
    "SimpleFlag_COLOR_0": "structure",
    "Structures_AT": "structure",
    "strutture_pubblicitarie_ponti": "structure",
    "supercheapflag": "structure",
    "TENNIS": "grass",
    "TIRES": "structure",
    "Truck2_COLOR_0": "vehicle",
    # "80": "vegetation",
    # "Tree_Tropical_Pruned": "vegetation",
    # "Treewall_Cap": "vegetation",
    # "Oak_Monterrey_001": "vegetation",
    # "Prototype_VEG_X_Tree_A_001": "vegetation",
    # "G_Bush_Hedge_A_Trimmed_Leaf_": "vegetation",
    # "VEG_Bush_Hedge_A_Trimmed_001_VEG_Bush_Hedge_A_Trimmed_Leaf_": "vegetation",
    # "VEG_Bush_Hedge_A_Trimmed_Leaf_001_veg_bush_hedge_a_trim_b4c": "vegetation",
    # "VEG_BUSH_Leafy_A_Trimmed_001": "vegetation",
    # "VEG_Bush_Shrub_A_GroundCover_Leaves_001": "vegetation",
    # "VEG_FM6_X_Plant_Flower_A_GroundCover_Leaves_001": "vegetation",
    # "Veg_Nurb_Tree_Pine_B_Xlarge_Background_002": "vegetation",
    # "VEG_Nurb_X_Bush_Common_B_Medium_001": "vegetation",
    # "VEG_Nurb_X_Bush_Small_B_Wide_001": "vegetation",
    # "VEG_Nurb_X_Tree_Common_A_Medium": "vegetation",
    # "VEG_Nurb_X_Tree_Common_C_Medium_002": "vegetation",
    # "VEG_Nurb_X_tree_Oak_C_Large_001": "vegetation",
    # "VEG_Nurb_X_Tree_Pine_A_001": "vegetation",
    # "VEG_Nurb_X_Tree_Pine_A_Thick_001": "vegetation",
    # "VEG_Nurb_X_Tree_Pine_A_Thin_001": "vegetation",
    # "Veg_Nurb_x_Tree_Pine_B_Xlarge_001": "vegetation",
    # "VEG_Nurb_X_Tree_Poplar_C_Background_001": "vegetation",
    # "VEG_Plant_Ivy_A_Leaf": "vegetation",
    # "VEG_Tree_Maple_A_Tall_Bark_001_veg_bush_hedge_a_trimmed_25e": "vegetation",
    # "VEG_X_Bush_A_001": "vegetation",
    # "VEG_X_Bush_A_002": "vegetation",
    # "VEG_X_Bush_Common_A_Large_001": "vegetation",
    # "VEG_X_Bush_Common_C_Large_001": "vegetation",
    # "VEG_X_Bush_Leafy_A_Medium_001": "vegetation",
    # "VEG_X_Bush_Leafy_D_Medium_001": "vegetation",
    # "VEG_X_Bush_Pine_B_001": "vegetation",
    # "VEG_X_Bush_Shrub_B_GroundCover_001": "vegetation",
    # "VEG_X_Plant_Flower_A_GroundCover_001": "vegetation",
    # "VEG_X_Tree_Oak_B_Large_001": "vegetation",
    # "VEG_X_Tree_Pine_B_Stone_001": "vegetation",
    # "VEG_X_Tree_Pine_B_Tall_Sparse": "vegetation",
    # "VEG_X_Tree_Pine_C_Stone_001": "vegetation",
    # "VEG_X_Tree_Pine_D_Stone_001": "vegetation",
    "Walls_B": "structure",
    "work_machine_COLOR_0": "vehicle",
    "WorldGridMaterial": "structure",
    "yellowline": "track_limit",
}

VERTEX_GROUPS_TO_MODIFY = [
    "AC_AUDIO",
    "AC_PIT",
    "AC_SEMAPHORE_GREEN",
    "AC_SEMAPHORE_RED",
    "AC_START",
    "AC_TIME",
    "AC_REVERB_ECHO",
]


MT_PANORAMA_DATA = TrackData(
    geometries_to_remove=GEOMETRIES_TO_REMOVE,
    vertex_groups_to_modify=VERTEX_GROUPS_TO_MODIFY,
    material_to_semantics=MATERIAL_TO_SEMANTIC_CLASS,
)