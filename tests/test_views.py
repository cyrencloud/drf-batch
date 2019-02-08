from django.test import override_settings
from django.urls import reverse, set_script_prefix, clear_script_prefix
from rest_framework.test import APITestCase


class TestBatch(APITestCase):
    def setUp(self):
        self.url = reverse('batch:batch')

    def tearDown(self):
        clear_script_prefix()

    def test_success(self):
        data = [
            {
                'method': 'PATCH',
                'path': reverse('view-200'),
                'data': {'test': '200'}
            },
            {
                'method': 'POST',
                'path': reverse('view-201'),
                'data': {'test': '201'}
            }
        ]
        response = self.client.post(self.url, data=data)
        assert response.status_code == 200
        assert response.json() == [
            {
                'method': 'PATCH',
                'path': reverse('view-200'),
                'data': {'test': '200'},
                'response': {
                    'status_code': 200,
                    'data': {'test': '200'}
                }
            },
            {
                'method': 'POST',
                'path': reverse('view-201'),
                'data': {'test': '201'},
                'response': {
                    'status_code': 201,
                    'data': {'test': '201'}
                }
            }
        ]

    def test_bad_request(self):
        data = [
            {
                'method': 'PUT',
                'path': reverse('view-400'),
                'data': {'test': '400'}
            },
            {
                'method': 'POST',
                'path': reverse('view-201'),
                'data': {'test': '201'}
            }
        ]
        response = self.client.post(self.url, data=data)
        assert response.status_code == 400
        assert response.json() == {
            'method': 'PUT',
            'path': reverse('view-400'),
            'data': {'test': '400'},
            'response': {
                'status_code': 400,
                'data': {'test': '400'}
            }
        }

    @override_settings(DRF_BATCH={'DEFAULT_SKIP_ERRORS': True})
    def test_skip_errors(self):
        data = [
            {
                'method': 'PUT',
                'path': reverse('view-400'),
                'data': {'test': '400'}
            },
            {
                'method': 'POST',
                'path': reverse('view-201'),
                'data': {'test': '201'}
            }
        ]
        response = self.client.post(self.url, data=data)
        assert response.status_code == 200
        assert response.json() == [
            {
                'method': 'PUT',
                'path': reverse('view-400'),
                'data': {'test': '400'},
                'response': {
                    'status_code': 400,
                    'data': {'test': '400'}
                }
            },
            {
                'method': 'POST',
                'path': reverse('view-201'),
                'data': {'test': '201'},
                'response': {
                    'status_code': 201,
                    'data': {'test': '201'}
                }
            }
        ]

    def test_unknown_path(self):
        data = [
            {
                'method': 'PUT',
                'path': 'unknown'
            }
        ]
        response = self.client.post(self.url, data=data)
        assert response.status_code == 404
        assert response.json() == {
            'method': 'PUT',
            'path': 'unknown',
            'response': {
                'status_code': 404
            }
        }

    def test_script_name(self):
        set_script_prefix("/script")
        path = reverse('view-200')
        assert "/script" in path
        data = [
            {
                'method': 'PATCH',
                'path': path,
                'data': {'test': '200'}
            }
        ]
        response = self.client.post(self.url, data=data)
        assert response.status_code == 200
        assert response.json() == [
            {
                'method': 'PATCH',
                'path': path,
                'data': {'test': '200'},
                'response': {
                    'status_code': 200,
                    'data': {'test': '200'}
                }
            }
        ]
