from src.tracks.silverstone import SILVERSTONE_DATA
from src.tracks.spa import SPA_DATA
from src.tracks.monza import MONZA_DATA
from src.tracks.vallelunga import VALLELUNGA_DATA

"""
Register TrackData instances here to make them available during data generation
"""

TRACK_DATA = {
    "monza": MONZA_DATA,
    "silverstone": SILVERSTONE_DATA,
    "spa": SPA_DATA,
    "vallelunga": VALLELUNGA_DATA,
}
