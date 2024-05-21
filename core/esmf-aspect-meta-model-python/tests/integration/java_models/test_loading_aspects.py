"""Collect statistics about loading test Aspect models."""

import csv

from glob import glob
from os.path import join
from pathlib import Path

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader

SAMM_VERSION = "2.0.0"


def get_test_files():
    """Get ttl models for testing."""
    base_path = Path(__file__).parent.absolute()
    samm_folder_name = f"samm_{SAMM_VERSION.replace('.', '_')}"
    search_pattern = join(base_path, "resources", "**", samm_folder_name, "**", "*.ttl")
    test_model_files = glob(search_pattern, recursive=True)

    return test_model_files


def load_test_models():
    """Test for loading Aspect models."""
    test_files = get_test_files()
    result = []
    all_test_files = len(test_files)
    i = 0
    step = 10
    print("Loading test Aspect models...")

    for test_file in test_files:
        i += 1
        if i % step == 0:
            print(f"{i}/{all_test_files}")

        test_file_path = Path(test_file)
        data = {
            "file_name": test_file_path.name,
            "folder_name": join(test_file_path.parents[1].name, test_file_path.parents[0].name),
            "status": "initializing",
            "error": None,
        }

        try:
            loader = AspectLoader()
            model_elements = loader.load_aspect_model(test_file)
            if not model_elements:
                raise Exception("No elements loaded")
        except Exception as error:
            data["error"] = str(error)
            data["status"] = "exception"
        else:
            data["status"] = "success"

        result.append(data)

    print(f"{i}/{all_test_files}")
    return result


def run_test_loading():
    """Run loading of all test Aspect models."""
    report = load_test_models()

    base_path = Path(__file__).parent.absolute()
    with open(join(base_path, "loading_models_test_report.csv"), "w", newline="") as csvfile:
        fieldnames = ["folder_name", "file_name", "status", "error"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in report:
            writer.writerow(row)


if __name__ == "__main__":
    run_test_loading()
