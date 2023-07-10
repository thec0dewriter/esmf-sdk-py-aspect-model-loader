"""DefaultFixedPointConstraint class unit tests suit."""

from unittest import mock

from esmf_aspect_meta_model_python.impl import DefaultFixedPointConstraint


class TestDefaultFixedPointConstraint:
    """DefaultFixedPointConstraint unit tests class."""

    meta_model_mock = mock.MagicMock(name="meta_model_base_attributes")

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_init(self, super_mock):
        result = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)

        super_mock.assert_called_once_with(self.meta_model_mock)
        assert result._scale == 0
        assert result._integer == 1

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_value(self, _):
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        result = fixed_point_constraint.scale

        assert result == 0

    @mock.patch(
        "esmf_aspect_meta_model_python.impl.constraints.default_fixed_point_constraint.DefaultConstraint.__init__"
    )
    def test_integer(self, _):
        fixed_point_constraint = DefaultFixedPointConstraint(self.meta_model_mock, 0, 1)
        result = fixed_point_constraint.integer

        assert result == 1
