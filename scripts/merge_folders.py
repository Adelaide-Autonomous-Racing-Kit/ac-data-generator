import argparse
import shutil
from pathlib import Path
from concurrent.futures import as_completed, ThreadPoolExecutor

from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-1", type=str, help="Path to folder to be merged")
    parser.add_argument("--input-2", type=str, help="Path to folder to be merged")
    parser.add_argument("--output", type=str, help="Path to output folfer")
    return parser.parse_args()


def copy_sample_files(output_path: Path, input_image: Path, i: int):
    # Copy image
    output_image = output_path.joinpath(f"{i}.jpeg")
    shutil.copyfile(input_image, output_image)
    # Copy class ids
    if Path(f"{str(input_image).split('.')[0]}-trainids.png").is_file():
        input_train_ids = f"{str(input_image).split('.')[0]}-trainids.png"
    else:
        input_train_ids = f"{str(input_image).split('.')[0]}-ids.png"
    output_train_ids = output_path.joinpath(f"{i}-ids.png")
    shutil.copyfile(input_train_ids, output_train_ids)
    # Copy visualisation
    if Path(f"{str(input_image).split('.')[0]}-seg_colour.png").is_file():
        input_visualisation = f"{str(input_image).split('.')[0]}-seg_colour.png"
    else:
        input_visualisation = f"{str(input_image).split('.')[0]}-colour.png"
    output_visualisation = output_path.joinpath(f"{i}-colour.png")
    shutil.copyfile(input_visualisation, output_visualisation)


def main():
    args = parse_arguments()
    output_path = Path(args.output)
    promises = []
    output_path.mkdir(parents=True, exist_ok=True)
    input_images = sorted(list(Path(args.input_1).glob("*.jpeg")))
    if args.input_2:
        input_images.extend(sorted(list(Path(args.input_2).glob("*.jpeg"))))
    progress_bar = tqdm(total=len(input_images))
    with ThreadPoolExecutor(max_workers=8) as executor:
        for i, input_image in enumerate(input_images):
            promises.append(
                executor.submit(copy_sample_files, output_path, input_image, i)
            )
        for promise in as_completed(promises):
            progress_bar.update(1)


if __name__ == "__main__":
    main()
