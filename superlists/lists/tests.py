from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from django.test import TestCase
from .views import home_page
from lists.models import Item

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

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        self.assertIn('A new list item', response.content.decode())#, request.POST)
        expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'}, request=request)
        self.assertEqual(
            self.remove_csrf_tag(response.content.decode()),
            self.remove_csrf_tag(expected_html))
    
class ItemModelTest(TestCase):

    def test_saving_amd_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')