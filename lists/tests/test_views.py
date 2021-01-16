from django.test import TestCase
from django.urls import resolve
from django.template.loader import render_to_string
from django.utils.html import escape

from lists.views import home_page
from lists.models import Item, List

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

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data = {'item_text': ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        expected_error = escape("You can't have an empty list")
        self.assertContains(response, expected_error)
    
    def test_invalid_list_item_not_saved(self):
        self.client.post('/lists/new', data = {'item_text': ""})
        self.assertEqual(List.objects.count(), 0)

class ListObjectTest(TestCase):
    def test_can_save_list(self):
        my_list = List.objects.create()
        Item.objects.create(text='itemey1', list = my_list)
        Item.objects.create(text='itemey2', list = my_list)

class NewItemTest(TestCase):
    # def test_can_save_a_POST_request_to_existing_list(self):
    #     other_list = List.objects.create()
    #     correct_list = List.objects.create()

    #     self.client.post(f'/list/{correct_list.id}/add_item',
    #         data = {'item_text': 'A new item for an existing list'})
        
    #     #self.assertEqual(Item.objects.count(), 1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'A new item for an existing list')
    #     self.assertEqual(new_item.list, correct_list)
    
    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        response = self.client.post(f'/lists/{correct_list.id}/add_item', 
            data = {'item_text': 'A new item'})
        print(response)
        self.assertRedirects(response, f'/lists/{correct_list.id}/')