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

from esmf_aspect_meta_model_python.base.contraints.constraint import Constraint


class RegularExpressionConstraint(Constraint, metaclass=abc.ABCMeta):
    """Restricts a string value to a regular expression as defined by
    XQuery 1.0 and XPath 2.0 Functions and Operators [xpath-functions]."""

    @property
    def value(self) -> str:
        raise NotImplementedError
