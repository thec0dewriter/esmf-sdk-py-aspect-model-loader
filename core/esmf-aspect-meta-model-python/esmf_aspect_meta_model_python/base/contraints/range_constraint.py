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

import abc

from typing import Any, Optional

from esmf_aspect_meta_model_python.base.bound_definition import BoundDefinition
from esmf_aspect_meta_model_python.base.contraints.constraint import Constraint


class RangeConstraint(Constraint, metaclass=abc.ABCMeta):
    """Restricts the value range of a Property.
    At least one of samm-c:maxValue or samm-c:minValue must be present in a
    Range Constraint. Additionally the BoundDefinition can specify whether
    the upper and lower value are included in the range.
    """

    @property
    def min_value(self) -> Optional[Any]:
        raise NotImplementedError

    @property
    def max_value(self) -> Optional[Any]:
        raise NotImplementedError

    @property
    def lower_bound_definition(self) -> Optional[BoundDefinition]:
        raise NotImplementedError

    @property
    def upper_bound_definition(self) -> Optional[BoundDefinition]:
        raise NotImplementedError
