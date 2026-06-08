import time
from selenium.webdriver.common.by import By

import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page import UrbanRoutesPage as page


class TestUrbanRoutes:
    driver = None
    from_field = data.ADDRESS_FROM
    to_field = data.ADDRESS_TO
    phone_number = data.PHONE_NUMBER

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        cls.driver.implicitly_wait(5)

    def test_set_route(self):
        page.set_route(self.from_field, self.to_field)
        page.assert_route(self.from_field, self.to_field)

    def test_select_plan(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()
        page.assert_comfort_plan_selected()

    def test_fill_phone_number(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()
        page.set_phone_number(self.phone_number)
        page.assert_phone_number(self.phone_number)

    def test_fill_card(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_comment_for_driver(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_order_blanket_and_handkerchiefs(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_order_2_ice_creams(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_car_search_model_appears(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_driver_info_appears(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()

    def test_car_search_model_appears(self):
        page.set_route(select.from_field, select.to_field)
        page.select_comfort_plan()
        page.set_phone_number(self.phone_number)
        page.set_card_info.phone_number(self.phone_number)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
