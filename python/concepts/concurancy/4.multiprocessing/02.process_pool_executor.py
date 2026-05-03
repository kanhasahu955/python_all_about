import os
from time import perf_counter
from pathlib import Path
from PIL import Image, ImageFilter

from concurrent.futures import ProcessPoolExecutor

BASE = Path(__file__).resolve().parent
IMAGES_DIR = BASE / "images"
THUMBS_DIR = BASE / "thumbs"

def create_thumbnail(
    filename: str, size: tuple[int, int] = (50, 50), thumbnail_dir: Path | str | None = None
) -> None:
    out_dir = Path(thumbnail_dir) if thumbnail_dir is not None else THUMBS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(filename)
    img = img.filter(ImageFilter.GaussianBlur())
    img.thumbnail(size)
    img.save(out_dir / os.path.basename(filename))

    print(f"{filename} was processed")

def main():
    start_time = perf_counter()
    with ProcessPoolExecutor() as executor:
        executor.map(create_thumbnail, [str(IMAGES_DIR / f"{i}.jpg") for i in range(1, 6)])
    end_time = perf_counter()
    print(f'Time taken: {end_time - start_time} seconds')

if __name__ == "__main__":
    main()
