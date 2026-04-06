import shutil
from pathlib import Path
import kagglehub

DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_and_prepare():
    print("Downloading dataset from Kaggle...")

    path = kagglehub.dataset_download(
        "kaushalnandania/credit-card-fraud-detection"
    )

    print("Downloaded to:", path)

    # Move files into your project structure
    source_path = Path(path)

    for file in source_path.glob("*.csv"):
        destination = DATA_DIR / file.name

        if not destination.exists():
            print(f"Moving {file.name} → {destination}")
            shutil.copy(file, destination)
        else:
            print(f"{file.name} already exists, skipping.")

    print("Dataset ready in data/raw/")


if __name__ == "__main__":
    download_and_prepare()
