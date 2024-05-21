#  Copyright (c) 2024 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from os import mkdir, remove
from os.path import exists, join
from pathlib import Path
from zipfile import ZipFile

import requests


FOLDER_TO_EXTRACT = "valid"
TEST_MODELS_PATH = join("tests", "integration", "java_models", "resources")
VERSION = "2.7.0"


def get_model_files_path(version: str) -> str:
    """Get a path for storing test models."""
    base_path = Path(__file__).parents[1].absolute()
    models_path = join(base_path, TEST_MODELS_PATH, f"esmf-test-aspect-models-{version}.jar")

    return models_path


def download_test_models(version: str = VERSION):
    """Downloads and extract the esmf-test-aspect-models."""
    model_files_path = get_model_files_path(version)

    print(f"Start downloading esmf-test-aspect-models version {version}")
    url = (
        f"https://repo1.maven.org/maven2/org/eclipse/esmf/esmf-test-aspect-models/{version}/"
        f"esmf-test-aspect-models-{version}.jar"
    )
    response = requests.get(url, allow_redirects=True)

    resource_folder = Path(model_files_path).parent.absolute()
    if not exists(resource_folder):
        mkdir(resource_folder)

    with open(model_files_path, "wb") as f:
        f.write(response.content)
    print("JAR-File Downloaded")

    print(f"Start extracting files from {model_files_path}")
    extracted_file_path = Path(model_files_path).parents[0].absolute()
    archive = ZipFile(model_files_path)
    for file_name in archive.namelist():
        if file_name.startswith(FOLDER_TO_EXTRACT):
            archive.extract(file_name, extracted_file_path)

    archive.close()
    print("Done extracting files.")

    print("Deleting esmf-test-aspect-models JAR file.")
    remove(model_files_path)


if __name__ == "__main__":
    download_test_models()
