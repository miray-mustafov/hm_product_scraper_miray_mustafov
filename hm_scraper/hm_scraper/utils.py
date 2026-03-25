from pathlib import Path


def yield_urls_for_scraping():
    """
    The point is flexibility, so we can load as many product urls as we want without changing the code
    Generator used to pass urls one by one for memory efficiency
    """
    project_root = Path(__file__).resolve().parent.parent.parent
    urls_file = project_root / "urls_for_scraping.txt"
    example_urls_file = project_root / "urls_for_scraping_example.txt"

    file_to_use = urls_file if urls_file.exists() else example_urls_file

    with file_to_use.open("r", encoding="utf-8") as file:
        for line in file:
            url = line.strip()
            if url:
                yield url
