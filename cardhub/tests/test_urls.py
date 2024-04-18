
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cardhub.views.signup import Signup


class TestUrls(SimpleTestCase):
    
    def test_signup_url_is_resolved(self):
        url = reverse('signup')
        assert self._is_the_correct_view_being_rendered(url, Signup)
        
        
    def _is_the_correct_view_being_rendered(self, url: str, view: Signup) -> bool:
        if not self._is_correct_url(url=url): return False
        return resolve(url).func.view_class == view
        

    def _is_correct_url(self, url: str) -> bool:
        return self._is_url_a_string(url=url) and self._is_expected_url(url=url)


    def _is_expected_url(self, url):
        CONST_EXPECTED_URL: str = "/signup/"
        return CONST_EXPECTED_URL == url


    def _is_url_a_string(self, url: str) -> bool:
        return isinstance(url, str)
