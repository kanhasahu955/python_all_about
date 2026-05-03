# from time import perf_counter

# def task():
#     result = 0 
#     for _ in range(10**8):
#         result += 1
#     return result

# if __name__ == "__main__":
#     start_time = perf_counter()
#     task()
#     task()
#     end_time = perf_counter()
#     print(f'Time taken: {end_time - start_time} seconds')


# from multiprocessing import Process
# from time import perf_counter

# def task()->int:
#     result = 0
#     for _ in range(10**8):
#         result += 1
#     return result

# if __name__ == "__main__":
#     start_time = perf_counter()
#     process_1 = Process(target=task)
#     process_2 = Process(target=task)

#     process_1.start()
#     process_2.start()

#     process_1.join()
#     process_2.join()

#     end_time = perf_counter()

#     print(f'Time taken: {end_time - start_time} seconds')


import os
from multiprocessing import Process
from pathlib import Path
from time import perf_counter

from PIL import Image

BASE = Path(__file__).resolve().parent
IMAGES_DIR = BASE / "images"
THUMBS_DIR = BASE / "thumbs"


def ensure_demo_images() -> None:
    """Create sample JPEGs if missing so the script runs without extra assets."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    THUMBS_DIR.mkdir(parents=True, exist_ok=True)
    for i in range(1, 6):
        path = IMAGES_DIR / f"{i}.jpg"
        if not path.exists():
            color = (i * 40 % 256, 100, (200 - i * 30) % 256)
            Image.new("RGB", (200, 200), color=color).save(path, "JPEG")


def create_thumbnail(
    filename: str, size: tuple[int, int] = (50, 50), thumbnail_dir: Path | str | None = None
) -> None:
    out_dir = Path(thumbnail_dir) if thumbnail_dir is not None else THUMBS_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    img = Image.open(filename)
    img.thumbnail(size)
    img.save(out_dir / os.path.basename(filename))
    print(f"{filename} was processed")


if __name__ == "__main__":
    ensure_demo_images()
    filenames = [str(IMAGES_DIR / f"{i}.jpg") for i in range(1, 6)]

    start_time = perf_counter()
    processes = [Process(target=create_thumbnail, args=(fn,)) for fn in filenames]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    end_time = perf_counter()
    print(f"Time taken: {end_time - start_time} seconds")

