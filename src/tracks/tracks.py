from src.tracks.monza import MONZA_DATA
from src.tools.data_generation.tracks.spa import SPA_DATA

"""
Register TrackData instances here to make them available during data generation
"""

TRACK_DATA = {
    "monza": MONZA_DATA,
    "spa": SPA_DATA,
}
