from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from functional_test.base import FunctionalTest
import time
import unittest
import os

class ItemValidationTest(FunctionalTest):
    @unittest.skip
    def test_cannot_add_empty_list_items(self):
        pass