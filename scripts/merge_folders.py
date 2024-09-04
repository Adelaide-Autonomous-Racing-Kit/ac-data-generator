import shutil
from pathlib import Path
from concurrent.futures import as_completed, ThreadPoolExecutor

from tqdm import tqdm

root = Path(
    "/home/james/Desktop/"
)
folder_a = root.joinpath("out_1")
folder_b = root.joinpath("")
out = root.joinpath("val")


def copy_sample_files(input_image: str, i: int):
    # Copy image
    output_image = out.joinpath(f"{i}.jpeg")
    shutil.copyfile(input_image, output_image)
    # Copy class ids
    if Path(f"{str(input_image).split('.')[0]}-trainids.png").is_file():
        input_train_ids = f"{str(input_image).split('.')[0]}-trainids.png"
    else:
        input_train_ids = f"{str(input_image).split('.')[0]}-ids.png"
    output_train_ids = out.joinpath(f"{i}-ids.png")
    shutil.copyfile(input_train_ids, output_train_ids)
    # Copy visualisation
    if Path(f"{str(input_image).split('.')[0]}-seg_colour.png").is_file():
        input_visualisation = f"{str(input_image).split('.')[0]}-seg_colour.png"
    else:
        input_visualisation = f"{str(input_image).split('.')[0]}-colour.png"
    output_visualisation = out.joinpath(f"{i}-colour.png")
    shutil.copyfile(input_visualisation, output_visualisation)


def main():
    promises = []
    out.mkdir(parents=True, exist_ok=True)
    input_images = sorted(list(folder_a.glob("*.jpeg")))
    input_images.extend(sorted(list(folder_b.glob("*.jpeg"))))
    progress_bar = tqdm(total=len(input_images))
    with ThreadPoolExecutor(max_workers=8) as executor:
        for i, input_image in enumerate(input_images):
            promises.append(executor.submit(copy_sample_files, input_image, i))
        for promise in as_completed(promises):
            progress_bar.update(1)


if __name__ == "__main__":
    main()
