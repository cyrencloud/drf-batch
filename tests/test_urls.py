from django.urls import reverse


class TestURLs(object):
    def test_name(self):
        assert reverse('batch:batch') == '/batch/'
