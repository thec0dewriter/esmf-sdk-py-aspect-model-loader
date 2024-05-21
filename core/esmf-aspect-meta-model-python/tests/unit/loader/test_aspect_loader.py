"""Aspect model Loader test suite."""

from pathlib import Path
from unittest import mock

from esmf_aspect_meta_model_python.loader.aspect_loader import AspectLoader


class TestAspectLoader:
    """Aspect model Loader test suite."""

    def test_init(self):
        result = AspectLoader("graph", "cache")

        assert result._cache == "cache"
        assert result._graph == "graph"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.SAMMGraph")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.DefaultElementCache")
    def test_init_with_defaults(self, default_element_cache_mock, samm_graph_mock):
        default_element_cache_mock.return_value = "cache"
        samm_graph_mock.return_value = "graph"
        result = AspectLoader()

        assert result._cache == "cache"
        assert result._graph == "graph"
        default_element_cache_mock.assert_called_once()
        samm_graph_mock.assert_called_once_with(cache="cache")

    def test_get_graph(self):
        loader = AspectLoader("graph", "cache")
        result = loader.get_graph()

        assert result == "graph"

    def test_get_samm_version(self):
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.get_samm_version.return_value = "samm_version"
        loader = AspectLoader(graph_mock, "cache")
        result = loader.get_samm_version()

        assert result == "samm_version"
        graph_mock.get_samm_version.assert_called_once()

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_prepare_file_path(self, isinstance_mock):
        isinstance_mock.return_value = True
        file_path = Path("file_path")
        result = AspectLoader.convert_file_path(file_path)

        assert result == "file_path"
        isinstance_mock.assert_called_once_with(file_path, Path)

    def test_load_aspect_model(self):
        graph_mock = mock.MagicMock(name="graph")
        graph_mock.parse.return_value = "graph"
        graph_mock.to_python.return_value = "loaded_aspect_model"
        loader = AspectLoader(graph_mock, "cache")
        result = loader.load_aspect_model("file_path")

        assert result == "loaded_aspect_model"
        graph_mock.parse.assert_called_once_with("file_path")
        graph_mock.to_python.assert_called_once()

    def test_find_by_name(self):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_name.return_value = "graph_node"
        loader = AspectLoader("graph", cache=cache_mock)
        result = loader.find_by_name("element_name")

        assert result == "graph_node"
        cache_mock.get_by_name.assert_called_once_with("element_name")

    def test_find_by_urn(self):
        cache_mock = mock.MagicMock(name="cache")
        cache_mock.get_by_urn.return_value = "graph_node"
        loader = AspectLoader("graph", cache_mock)
        result = loader.find_by_urn("urn")

        assert result == "graph_node"
        cache_mock.get_by_urn.assert_called_once_with("urn")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.determine_element_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader.find_by_name")
    def test_determine_access_path(self, find_by_name_mock, determine_element_access_path_mock):
        find_by_name_mock.side_effect = (["base_element"], [])
        determine_element_access_path_mock.return_value = ["access_path"]
        loader = AspectLoader("graph", "cache")
        result = loader.determine_access_path("base_element_name")

        assert result == ["access_path"]
        find_by_name_mock.assert_called_once_with("base_element_name")
        determine_element_access_path_mock.assert_called_once_with("base_element")

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._AspectLoader__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_determine_element_access_path_with_payload_name(
        self,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.payload_name = "payload_name"
        determine_access_path_mock.return_value = "element_access_path"
        loader = AspectLoader("graph", "cache")
        result = loader.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["payload_name"]])

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.AspectLoader._AspectLoader__determine_access_path")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.Property")
    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_determine_element_access_path_base_element_name(
        self,
        isinstance_mock,
        property_mock,
        determine_access_path_mock,
    ):
        isinstance_mock.return_value = True
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.name = "base_element_name"
        base_element_mock.payload_name = None
        determine_access_path_mock.return_value = "element_access_path"
        loader = AspectLoader("graph", "cache")
        result = loader.determine_element_access_path(base_element_mock)

        assert result == "element_access_path"
        isinstance_mock.assert_called_once_with(base_element_mock, property_mock)
        determine_access_path_mock.assert_called_once_with(base_element_mock, [["base_element_name"]])

    def test_determine_access_path_base_element_is_none(self):
        loader = AspectLoader("graph", "cache")
        result = loader._AspectLoader__determine_access_path(None, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_none(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = None
        loader = AspectLoader("graph", "cache")
        result = loader._AspectLoader__determine_access_path(base_element_mock, "path")

        assert result == "path"

    def test_determine_access_path_parent_element_is_empty_list(self):
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = []
        loader = AspectLoader("graph", "cache")
        result = loader._AspectLoader__determine_access_path(base_element_mock, "path")

        assert result == "path"

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_private_determine_access_path_parent_payload_name(self, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = "payload_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        loader = AspectLoader("graph", "cache")
        result = loader._AspectLoader__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_name", "path"]]

    @mock.patch("esmf_aspect_meta_model_python.loader.aspect_loader.isinstance")
    def test_private_determine_access_path_parent_name(self, isinstance_mock):
        parent_element_mock = mock.MagicMock(name="parent_element")
        parent_element_mock.parent_elements = []
        parent_element_mock.payload_name = None
        parent_element_mock.name = "payload_element_name"
        base_element_mock = mock.MagicMock(name="base_element")
        base_element_mock.parent_elements = [parent_element_mock]
        isinstance_mock.return_value = True
        loader = AspectLoader("graph", "cache")
        result = loader._AspectLoader__determine_access_path(base_element_mock, [["path"]])

        assert result == [["payload_element_name", "path"]]
