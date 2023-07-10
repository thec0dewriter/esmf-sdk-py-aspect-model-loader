"""DefaultEither class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultEither


class TestDefaultEither:
    """DefaultEither unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    data_type_mock = mock.MagicMock(name="data_type")
    left_mock = mock.MagicMock(name="left")
    right_mock = mock.MagicMock(name="right")

    @mock.patch("esmf_aspect_meta_model_python.impl.characteristics.default_either.DefaultCharacteristic.__init__")
    def test_init(self, super_mock):
        result = DefaultEither(self.meta_model_mock, self.data_type_mock, self.left_mock, self.right_mock)

        super_mock.assert_called_once_with(self.meta_model_mock, self.data_type_mock)
        self.left_mock.append_parent_element.assert_called_once_with(result)
        assert result._left == self.left_mock
        self.right_mock.append_parent_element.assert_called_once_with(result)
        assert result._right == self.right_mock

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.DefaultCharacteristic.__init__"
    )
    def test_left(self, _):
        characteristic = DefaultEither(self.meta_model_mock, self.data_type_mock, self.left_mock, self.right_mock)
        result = characteristic.left

        assert result == self.left_mock

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.characteristics.default_characteristic.DefaultCharacteristic.__init__"
    )
    def test_right(self, _):
        characteristic = DefaultEither(self.meta_model_mock, self.data_type_mock, self.left_mock, self.right_mock)
        result = characteristic.right

        assert result == self.right_mock
