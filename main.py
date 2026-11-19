"""Copy the submitted image to the required output path, byte for byte."""
from pathlib import Path
import shutil


def main() -> None:
    source = Path(__file__).resolve().with_name("entry.png")
    destination = Path("/output/entry.png")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


if __name__ == "__main__":
    main()
