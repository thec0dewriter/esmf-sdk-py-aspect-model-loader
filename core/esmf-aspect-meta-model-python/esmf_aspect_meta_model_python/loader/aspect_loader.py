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

from pathlib import Path
from typing import Optional, Union

from esmf_aspect_meta_model_python.base.base import Base
from esmf_aspect_meta_model_python.base.property import Property
from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.samm_graph import SAMMGraph


class AspectLoader:
    """Entry point to load an aspect model. To load an aspect model from
    a turtle file call AspectLoader.load_aspect_model(file_path)

    cache strategy to cache created elements to ensure uniqueness and a fast lookup of it.
    The default cache strategy ignores inline defined elements.
    """

    def __init__(self, graph: Optional[SAMMGraph] = None, cache: Optional[DefaultElementCache] = None) -> None:
        self._cache = cache if cache else DefaultElementCache()
        self._graph = graph if graph else SAMMGraph(cache=self._cache)

    def get_graph(self) -> SAMMGraph:
        """Get SAMM graph.

        :return: parsed SAMM Aspect model Graph.
        """
        return self._graph

    def get_samm_version(self) -> str:
        """Get SAMM version of the graph."""
        return self._graph.get_samm_version()

    @staticmethod
    def convert_file_path(file_path: Union[str, Path]) -> str:
        """Convert file_path to the string.

        :param file_path: path to model file
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)

        return file_path

    def load_aspect_model(self, file_path: Union[Path, str]):
        """Load aspect model to RDF GRAPH.

        Create an aspect object with all the including properties and operations with the turtle file

        :param file_path: path to the turtle file. Can be either a string or a Path object
        :return: instance of the aspect
        """
        file_path = self.convert_file_path(file_path)
        _ = self._graph.parse(file_path)
        loaded_aspect_model = self._graph.to_python()

        return loaded_aspect_model

    def find_by_name(self, element_name: str) -> list[Base]:
        """Find a specific model element by name, and returns the found elements

        :param element_name: name or pyload of element
        :return: list of found elements
        """
        return self._cache.get_by_name(element_name)

    def find_by_urn(self, urn: str) -> Optional[Base]:
        """Find a specific model element, and returns it or undefined.

        :param urn: urn of the model element
        :return: found element or None
        """
        return self._cache.get_by_urn(urn)

    def determine_access_path(self, base_element_name: str) -> list[list[str]]:
        """Determine the access path.

        Search for the element in cache first then call "determine_element_access_path" for every found element

        :param base_element_name: name of element
        :return: list of paths found to access the respective value.
        """
        paths: list[list[str]] = []
        base_element_list = self.find_by_name(base_element_name)
        for element in base_element_list:
            paths.extend(self.determine_element_access_path(element))

        return paths

    def determine_element_access_path(self, base_element: Base) -> list[list[str]]:
        """Determine the path to access the respective value in the Aspect JSON object.

        :param base_element: element for determine the path
        :return: list of paths found to access the respective value.
        """
        path: list[list[str]] = []
        if isinstance(base_element, Property):
            if hasattr(base_element, "payload_name") and base_element.payload_name is not None:  # type: ignore
                path.insert(0, [base_element.payload_name])  # type: ignore
            else:
                path.insert(0, [base_element.name])

        return self.__determine_access_path(base_element, path)

    def __determine_access_path(self, base_element: Base, path: list[list[str]]) -> list[list[str]]:
        """Determine access path.

        :param base_element: element for determine the path
        :return: list of paths found to access the respective value.
        """
        if base_element is None or base_element.parent_elements is None or len(base_element.parent_elements) == 0:
            return path

        # in case of multiple parent get the number of additional parents and
        # clone the existing paths
        path.extend(path[0] for _ in range(len(base_element.parent_elements) - 1))

        for index, parent in enumerate(base_element.parent_elements):
            if isinstance(parent, Property):
                if hasattr(parent, "payload_name") and parent.payload_name is not None:  # type: ignore
                    path_segment = parent.payload_name  # type: ignore
                else:
                    path_segment = parent.name

                if (len(path[index]) > 0 and path[index][0] != path_segment) or len(path[0]) == 0:
                    path[index].insert(0, path_segment)

            self.__determine_access_path(parent, path)  # type: ignore

        return path
