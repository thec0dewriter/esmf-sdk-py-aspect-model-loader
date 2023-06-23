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

from typing import Optional


class HasUrn(metaclass=abc.ABCMeta):
    """Base class from which all Meta Model Elements inherit.
    Class prescribes method to get the element urn and samm version.
    """

    @property
    def urn(self) -> Optional[str]:
        raise NotImplementedError

    @property
    def meta_model_version(self) -> str:
        raise NotImplementedError
