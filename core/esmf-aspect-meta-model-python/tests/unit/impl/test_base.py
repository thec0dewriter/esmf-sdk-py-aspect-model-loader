"""BaseElement class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import BaseImpl


def get_meta_model_mock():
    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    meta_model_mock.meta_model_version = "meta_model_version"
    meta_model_mock.urn = "urn"
    meta_model_mock.name = "name"
    meta_model_mock.preferred_names = "preferred_names"
    meta_model_mock.descriptions = "descriptions"
    meta_model_mock.see = "see"

    return meta_model_mock


class TestBaseImpl:
    """BaseImpl unit tests class."""

    meta_model_mock = get_meta_model_mock()

    def test_init(self):
        result = BaseImpl(self.meta_model_mock)

        assert result._meta_model_version == "meta_model_version"
        assert result._urn == "urn"
        assert result._name == "name"
        assert result._preferred_names == "preferred_names"
        assert result._descriptions == "descriptions"
        assert result._see == "see"
        assert result._parent_elements is None

    def test_parent_elements_getter_none(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.parent_elements

        assert result is None

    def test_parent_elements_getter_list(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [element_mock]

    def test_parent_elements_setter_none(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.parent_elements = element_mock
        result = base.parent_elements

        assert result is None

    def test_parent_elements_setter_value(self):
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.parent_elements = [element_mock]
        result = base.parent_elements

        assert result == [element_mock]

    def test_append_parent_element_no_parent_elements(self):
        base = BaseImpl(self.meta_model_mock)
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(element_mock)
        result = base._parent_elements

        assert result == [element_mock]

    def test_append_parent_element(self):
        base = BaseImpl(self.meta_model_mock)
        initial_element_mock = mock.MagicMock(name="init_element")
        element_mock = mock.MagicMock(name="element")
        base.append_parent_element(initial_element_mock)
        base.append_parent_element(element_mock)
        result = base.parent_elements

        assert result == [initial_element_mock, element_mock]

    def test_meta_model_version(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.meta_model_version

        assert result == "meta_model_version"

    def test_preferred_names(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.preferred_names

        assert result == "preferred_names"

    def test_descriptions(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.descriptions

        assert result == "descriptions"

    def test_see(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.see

        assert result == "see"

    def test_urn(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.urn

        assert result == "urn"

    def test_name(self):
        base = BaseImpl(self.meta_model_mock)
        result = base.name

        assert result == "name"
