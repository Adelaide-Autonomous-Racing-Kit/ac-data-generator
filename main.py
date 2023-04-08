import os
import sys
from pathlib import Path

from src.generate_data import MultiprocessDataGenerator


def main():
    config_path = sys.argv[0]
    root_path = Path(os.path.dirname(__file__))
    config_path = root_path.joinpath(config_path)
    data_generator = MultiprocessDataGenerator(config_path)
    data_generator.start()


if __name__ == "__main__":
    main()
