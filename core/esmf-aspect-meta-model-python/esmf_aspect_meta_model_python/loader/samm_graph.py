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

from pathlib import Path
from typing import List, Union

from rdflib import RDF, Graph, URIRef
from rdflib.graph import Node

from esmf_aspect_meta_model_python.loader.default_element_cache import DefaultElementCache
from esmf_aspect_meta_model_python.loader.model_element_factory import ModelElementFactory
from esmf_aspect_meta_model_python.resolver.base import AspectModelResolver, BaseResolver
from esmf_aspect_meta_model_python.vocabulary.SAMM import SAMM


class SAMMGraph:
    """SAMM graph."""

    samm_prefix = "urn:samm:org.eclipse.esmf.samm"

    def __init__(
        self,
        graph: Graph | None = None,
        resolver: BaseResolver | None = None,
        cache: DefaultElementCache | None = None,
    ):
        super().__init__()

        self._graph = graph if graph else Graph()
        self._resolver = resolver if resolver else AspectModelResolver()
        self._cache = cache if cache else DefaultElementCache()
        self._samm_version = ""
        self._file_path: str = ""

    def __repr__(self) -> str:
        return repr(self._graph)

    def __str__(self) -> str:
        return f"SAMM {self._graph}"

    def get_rdf_graph(self) -> Graph:
        """Get RDF graph."""
        return self._graph

    def get_samm_version(self) -> str:
        """Get SAMM version from the graph."""
        version = ""

        for prefix, namespace in self._graph.namespace_manager.namespaces():
            if prefix == "samm":
                urn_parts = namespace.split(":")
                version = urn_parts[-1].replace("#", "")

        return version

    @staticmethod
    def convert_file_path(file_path: Union[Path, str]) -> str:
        """Convert file_path to the string.

        :param file_path: path to model file
        """
        if isinstance(file_path, Path):
            file_path = str(file_path)

        return file_path

    def parse(self, file_path: Union[Path, str]) -> Graph:
        """Parse a file to the SAMM graph.

        :param file_path: Path to the *ttl file.
        """
        self._file_path = self.convert_file_path(file_path)
        self._graph.parse(self._file_path)
        self._samm_version = self.get_samm_version()
        self._resolver.resolve(self._graph, self._file_path, self._samm_version)

        return self._graph

    def _get_model_file_path(self, model_file_path: str = "") -> str:
        """Get a model file path.

        :param model_file_path: str with path to the model
        :return: validated path rto the model fiel
        """
        model_file_path = model_file_path if model_file_path else self._file_path
        if not model_file_path:
            raise ValueError("Path to the model is empty")

        return model_file_path

    def get_nodes_from_graph(self, model_file_path: str = "") -> List[Node]:
        """Get a list of URIRef to nodes from the base model file."""
        nodes = []
        model_file_path = self._get_model_file_path(model_file_path)
        base_graph = Graph().parse(model_file_path, format="turtle")

        # Search for Aspect elements
        samm = SAMM(self._samm_version)
        for subject in base_graph.subjects(predicate=RDF.type, object=samm.get_urn(SAMM.aspect)):  # type: ignore
            nodes.append(subject)

        if not nodes:
            for subject, object in base_graph.subject_objects(predicate=RDF.type, unique=True):
                prefix_data = str(object)[1:-1].split(":")
                if ":".join(prefix_data[:3]) == self.samm_prefix:
                    nodes.append(subject)

        return nodes

    def get_base_nodes(self, aspect_urn: URIRef | str = "") -> List[Node]:
        """Get a list of base graph elements.

        :param aspect_urn: URN of the Aspect node.
        :return: List of base graph elements.
        """
        base_elements: list[Node] = []

        if aspect_urn:
            base_elements += [aspect_urn if isinstance(aspect_urn, URIRef) else URIRef(aspect_urn)]
        else:
            base_elements += self.get_nodes_from_graph()

        return base_elements

    def to_python(self, aspect_urn: URIRef | str = "") -> List[URIRef | None]:
        """Convert SAMM graph to Python objects."""
        base_nodes = self.get_base_nodes(aspect_urn)
        model_element_factory = ModelElementFactory(self._samm_version, self._graph, self._cache)
        aspect_elements = model_element_factory.create_all_graph_elements(base_nodes)

        return aspect_elements
