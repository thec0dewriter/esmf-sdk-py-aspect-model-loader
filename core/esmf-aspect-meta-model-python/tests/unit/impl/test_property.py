"""DefaultProperty class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultProperty


class TestDefaultProperty:
    """DefaultProperty unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")
    characteristic_mock = mock.MagicMock(name="characteristic")
    example_value = "example_value"
    property_mock = mock.MagicMock(name="property")
    abstract = True
    optional = True
    not_in_payload = True
    payload_name = "payload_name"

    @mock.patch("esmf_aspect_meta_model_python.impl.default_property.BaseImpl.__init__")
    def test_init(self, super_mock):
        result = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )

        super_mock.assert_called_once_with(self.meta_model_mock)
        self.characteristic_mock.append_parent_element.assert_called_once_with(result)
        assert result._characteristic == self.characteristic_mock
        assert result._example_value == self.example_value
        assert result._is_abstract == self.abstract
        assert result._extends == self.property_mock
        assert result._optional == self.optional
        assert result._not_in_payload == self.not_in_payload
        assert result._payload_name == self.payload_name

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_characteristic(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.characteristic

        assert result == self.characteristic_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_example_value(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.example_value

        assert result == self.example_value

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_abstract(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.is_abstract

        assert result == self.abstract

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_extends(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.extends

        assert result == self.property_mock

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_optional(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.is_optional

        assert result == self.optional

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_is_not_in_payload(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.is_not_in_payload

        assert result == self.not_in_payload

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_payload_name(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=self.property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        result = property_cls.payload_name

        assert result == self.payload_name

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_preferred_names_no_extends(self, _):
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=None,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        property_cls._preferred_names = "preferred_names"
        result = property_cls.preferred_names

        assert result == "preferred_names"

    @mock.patch("esmf_aspect_meta_model_python.impl.default_operation.super")
    def test_preferred_names_extends(self, _):
        property_mock = mock.MagicMock(name="property")
        property_mock.preferred_names = {"property_preferred_names": "preferred_names"}
        property_cls = DefaultProperty(
            meta_model_base_attributes=self.meta_model_mock,
            characteristic=self.characteristic_mock,
            example_value=self.example_value,
            extends=property_mock,
            abstract=self.abstract,
            optional=self.optional,
            not_in_payload=self.not_in_payload,
            payload_name=self.payload_name,
        )
        property_cls._preferred_names = {"base_preferred_names": "preferred_names"}
        result = property_cls.preferred_names

        assert "property_preferred_names" in result
        assert "base_preferred_names" in result
