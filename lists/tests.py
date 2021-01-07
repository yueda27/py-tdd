from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string

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
    

class ListViewTest(TestCase):

    def test_use_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response, 'list.html')
    
    def test_displays_only_item_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey1', list = correct_list)
        Item.objects.create(text='itemey2', list = correct_list)
        other_list = List.objects.create()
        Item.objects.create(text = 'other list item 1', list = other_list)
        Item.objects.create(text = 'other list item 2', list = other_list)

        response = self.client.get(f'/lists/{correct_list.id}/')

        self.assertContains(response, 'itemey1')
        self.assertContains(response, 'itemey2')
        self.assertNotContains(response, 'other list item 1')
        self.assertNotContains(response, 'other list')

class NewListTest(TestCase):
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/lists/new', data = {'item_text': 'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()

        self.assertEqual(new_item.text, 'A new list item')

    def test_redirect_after_POST(self):
        response = self.client.post('/lists/new', data = {'item_text': 'A new list item'})
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

class ListObjectTest(TestCase):
    def test_can_save_list(self):
        my_list = List.objects.create()
        Item.objects.create(text='itemey1', list = my_list)
        Item.objects.create(text='itemey2', list = my_list)
