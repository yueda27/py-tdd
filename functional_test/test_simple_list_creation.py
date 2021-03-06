from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from functional_test.base import FunctionalTest
import time
import unittest
import os

MAX_WAIT = 3
class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.live_server_url)

        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        user_1_list_url = self.browser.current_url
        self.assertRegex(user_1_list_url, 'lists/.+')

        #Ensure second user does not see first user list

        self.browser.quit()
        options = webdriver.FirefoxOptions()
        options.headless = True
        self.browser = webdriver.Firefox(options = options)
        
        

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text

        def ensure_no_user1_list(page_text):
            self.assertNotIn('Buy peacock feathers', page_text)
            self.assertNotIn('Use peacock feathers to make a fly', page_text)

        ensure_no_user1_list(page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        user_2_list_url = self.browser.current_url
        self.assertRegex(user_2_list_url, 'lists/+')
        self.assertNotEqual(user_1_list_url, user_2_list_url)
        self.browser.get(user_2_list_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        ensure_no_user1_list(page_text)
