from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError

from lists.views import home_page
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_do_not_save_on_GET(self):
        self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)

    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_save_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(second_save_item.text, second_save_item.text)
    
class ListAndItemTest(TestCase):
    def test_cannot_save_empty_list(self):
        list_ = List.objects.create()
        item = Item(list=list_, text = '')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()