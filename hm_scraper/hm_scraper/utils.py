import json
from pathlib import Path


def load_urls_for_scraping() -> list[str]:
    """
    The point is flexibility, so we can load as many product urls as we want without changing the code
    """
    project_root = Path(__file__).resolve().parent.parent.parent
    urls_file = project_root / "urls_for_scraping.json"
    example_urls_file = project_root / "urls_for_scraping_example.json"

    file_to_use = urls_file if urls_file.exists() else example_urls_file

    with file_to_use.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("urls_for_scraping", [])
