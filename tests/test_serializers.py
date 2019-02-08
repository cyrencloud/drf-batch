from rest_framework.exceptions import ErrorDetail
from drf_batch.serializers import RequestSerializer


class TestRequestSerializer(object):
    def test_valid(self):
        s = RequestSerializer(data={'method': 'PUT', 'path': 'some/path/'})
        assert s.is_valid()

    def test_with_data_field(self):
        s = RequestSerializer(data={'method': 'PUT', 'path': 'some/path/', 'data': {'some_field': 'value'}})
        assert s.is_valid()

    def test_wrong_method(self):
        s = RequestSerializer(data={'method': 'GET', 'path': 'some/path/'})
        assert not s.is_valid()
        assert s.errors == {'method': [ErrorDetail(string='"GET" is not a valid choice.', code='invalid_choice')]}

    def test_missing_field(self):
        s = RequestSerializer(data={'method': 'POST'})
        assert not s.is_valid()
        assert s.errors == {'path': [ErrorDetail(string='This field is required.', code='required')]}
