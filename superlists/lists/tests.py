from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from django.test import TestCase
from .views import home_page

class HomePageTest(TestCase):

    def remove_csrf_tag(self, text):
    #Remove csrf tag from TEXT
        return re.sub(r'<[^>]*csrfmiddlewaretoken[^>]*>', '', text)

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        print("the output of found is:", found)
        self.assertAlmostEqual(found.func, home_page)
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        self.assertEqual(
            self.remove_csrf_tag(response.content.decode()), 
            self.remove_csrf_tag(expected_html)
            )
    

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertIn('A new list item', response.content.decode(), request.POST)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'}, request=request)
        self.assertEqual(
            self.remove_csrf_tag(response.content.decode()),
            self.remove_csrf_tag(expected_html))