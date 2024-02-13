#  Copyright (c) 2023 Robert Bosch Manufacturing Solutions GmbH
#
#  See the AUTHORS file(s) distributed with this work for additional
#  information regarding authorship.
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
#   SPDX-License-Identifier: MPL-2.0

from os import getcwd
from pathlib import Path

from esmf_aspect_meta_model_python import AspectLoader

RESOURCE_PATH = Path("tests/integration/resources/com.bosch.test.models/0.2.0")


def test_resolve_elements_references():
    file_path = getcwd() / RESOURCE_PATH / "AspectWithProperties.ttl"
    aspect_loader = AspectLoader()
    aspect = aspect_loader.load_aspect_model(file_path)

    assert aspect.get_preferred_name("en") == "Aspect with properties"
    assert aspect.name == "ProcessParameters"
    assert aspect.get_preferred_name("en") == "Aspect with properties"
    assert aspect.get_description("en") == "Test aspect with properties ifrom different files."

    part_identifier = aspect.properties[0]
    assert part_identifier.name == "ExternalIdentifier"
    assert part_identifier.get_preferred_name("en") == "External identifier"
    assert part_identifier.get_description("en") == "External identifier description."

    processed_part_id = part_identifier.properties[0]
    assert processed_part_id.name == "processedPartId"
    assert processed_part_id.get_preferred_name("en") == "Processed Part ID"
    assert processed_part_id.get_description("en") == "The identification of the processed part based on part number."
    assert str(processed_part_id.example_value) == "F03Z1234560213107000283011234567990"

    part_number = processed_part_id.characteristic
    assert part_number.name == "PartNumber"
    assert part_number.see == ["https://inside-docupedia.bosch.com/confluence/x/ssq0O"]
    assert part_number.base_characteristic.get_preferred_name("en") == "Part Number"
    assert part_number.constraints[0].value == "[A-Z0-9-]{10,68}"

    material_number = part_identifier.properties[1]
    assert material_number.name == "materialNumber"
    assert material_number.get_preferred_name("en") == "Material Number"
    assert material_number.get_preferred_name("de") == "Materialnummer"
    assert material_number.get_description("en") == (
        "The identification of the product based on the SAP material number."
    )
    assert material_number.characteristic.constraints[0].value == "[A-Z0-9]{9,13}"
