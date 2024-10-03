from acdg.tracks.monza import MONZA_DATA
from acdg.tracks.nordschleife import NORDSCHLEIFE_DATA
from acdg.tracks.silverstone import SILVERSTONE_DATA
from acdg.tracks.spa import SPA_DATA
from acdg.tracks.vallelunga import VALLELUNGA_DATA
from acdg.tracks.yas_marina import YAS_MARINA_DATA
from acdg.tracks.mt_panorama import MT_PANORAMA_DATA

"""
Register TrackData instances here to make them available during data generation
"""

TRACK_DATA = {
    "monza": MONZA_DATA,
    "silverstone": SILVERSTONE_DATA,
    "spa": SPA_DATA,
    "vallelunga": VALLELUNGA_DATA,
    "nordschleife": NORDSCHLEIFE_DATA,
    "yas_marina": YAS_MARINA_DATA,
    "mount_panorama": MT_PANORAMA_DATA,
}
