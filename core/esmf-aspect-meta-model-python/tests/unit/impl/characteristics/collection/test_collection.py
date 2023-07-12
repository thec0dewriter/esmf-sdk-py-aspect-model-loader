"""DefaultCollection class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultCollection


class TestDefaultCollection:
    """DefaultCollection unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")
    characteristic_mock = mock.MagicMock(name="characteristic")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCollection._set_parent_element_on_child_element"
    )
    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_init(self, super_mock, set_parent_element_on_child_element_mock):
        result = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        assert result._element_characteristic == self.characteristic_mock
        set_parent_element_on_child_element_mock.assert_called_once()

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_set_parent_element_on_child_element_mock(self, _):
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)

        self.characteristic_mock.append_parent_element.assert_called_once_with(collection)

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.collection.default_collection."
        "DefaultCharacteristic.__init__"
    )
    def test_element_characteristic(self, _):
        collection = DefaultCollection(self.meta_model_mock, self.data_type_mock, self.characteristic_mock)
        result = collection.element_characteristic

        assert result == self.characteristic_mock
