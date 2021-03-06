from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from .list_page import ListPage


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the home page and accidentally tries to submit
        # an empty list item. She hits Enter on the empty input box
        list_page = ListPage(self)
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_text:invalid'
        ))

        # She starts typing some text for the new item and the error
        # disappears
        list_page.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # And she can submit it successfully
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy milk', 1)

        # Perversely, she now decides to submit a second blank list item
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Again, the browser will not comply
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # And she can correct it by filling some text in
        list_page.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        list_page.wait_for_row_in_list_table('Make tea', 2)

    def test_cannot_add_duplicate_items(self):
        # Edith goes to the home page and starts a new list
        list_page = ListPage(self) \
            .add_list_item('Buy wellies')

        # She accidentally tries to enter a duplicate item
        list_page.get_item_input_box().send_keys('Buy wellies')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # She sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            list_page.get_error_element().text,
                "You've already got this in your list"
        ))

    def test_error_messages_are_cleared_on_input(self):
        # Edith starts a list and causes a validation error:
        list_page = ListPage(self) \
            .add_list_item('Banter too thick')
        list_page.get_item_input_box().send_keys('Banter too thick')
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertTrue(
            list_page.get_error_element().is_displayed()
        ))

        # She starts typing in the input box to clear the error
        list_page.get_item_input_box().send_keys('a')

        # She is pleased to see that the error message disappears
        self.wait_for(lambda: self.assertFalse(
            list_page.get_error_element().is_displayed()
        ))
