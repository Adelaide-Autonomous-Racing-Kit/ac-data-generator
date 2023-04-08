from src.tools.data_generation.cars.alfa_romeo_gtr import ALFA_ROMEO_GTR_DATA
from src.tools.data_generation.cars.audi_r8_lms_2016 import AUDI_R8_LMS_2016_DATA
from src.tools.data_generation.cars.invisible_car import INVISIBLE_CAR

"""
Register CarData instances here to make them available during data generation
"""

CAR_DATA = {
    "audi_r8_lms_2016": AUDI_R8_LMS_2016_DATA,
    "alfa_romeo_gtr": ALFA_ROMEO_GTR_DATA,
    "invisible_car": INVISIBLE_CAR,
}
