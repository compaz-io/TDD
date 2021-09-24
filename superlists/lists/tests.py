from django.urls import resolve
from django.test import TestCase
from .views import home_page

class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        print("the output of found is:", found)
        self.assertAlmostEqual(found.func, home_page)