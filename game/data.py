import csv
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
IMAGE_DIR = BASE_DIR / "ISO_Image_Library" / "Icons_200px"
CSV_PATH = IMAGE_DIR / "icon_image_key.csv"


@dataclass
class Icon:
    title: str
    image_path: Path


class GameData:
    def __init__(self):
        self.icons: list[Icon] = self._load()

    def _load(self) -> list[Icon]:
        icons = []
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row["Image Downloaded"].strip() != "True":
                    continue
                image_url = row["Image Path"].strip()
                # URL ends like ".../grs/<uuid>_" — append "200.png" to get local filename
                uuid_part = image_url.split("/")[-1]
                filename = f"{uuid_part}200.png"
                image_path = IMAGE_DIR / filename
                if image_path.exists():
                    icons.append(Icon(title=row["Title"].strip(), image_path=image_path))
        return icons

    def __len__(self) -> int:
        return len(self.icons)
