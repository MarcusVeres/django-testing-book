import unittest, time 

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# class NewVisitorTest( unittest.TestCase ) :
class NewVisitorTest( LiveServerTestCase ) : 

    # executed before all tests
    def setUp( self ) : 

        self.browser = webdriver.Chrome()

        # wait for 3 seconds, if needed 
        self.browser.implicitly_wait( 3 ) 


    # executed after all tests
    def tearDown( self ) : 

        self.browser.quit()


    # helper methods 
    def check_for_text_in_list_table( self , row_text ) : 

        table = self.browser.find_element_by_id( 'list-table' )
        rows = table.find_elements_by_tag_name( 'tr' )
        self.assertIn( row_text , [ row.text for row in rows ] )


    # 
    def test_can_create_a_list_and_retrieve_it_later( self ) :

        # Edith has heard about a cool new online to-do app. 
        # She goes to check out its homepage
        self.browser.get( self.live_server_url ) 
            # self.browser.get( 'http://localhost:9090' )


        # She notices the page title and header mention to-do lists
        self.assertIn( 'To-Do' , self.browser.title )
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn( 'To-Do' , header_text )

        # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id( 'add-new-item' )
        self.assertEqual( 
            inputbox.get_attribute( 'placeholder' ) , 
            'Enter a to-do item' 
        )

        # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)
        first_item_text = 'Buy peacock feathers' 
        inputbox.send_keys( first_item_text )

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys( Keys.ENTER )
        self.check_for_text_in_list_table( '1: ' + first_item_text )

        # There is still a text box inviting her to add another item. 
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)
        second_item_text = 'Use peacock feathers to make a fly'
        inputbox = self.browser.find_element_by_id( 'add-new-item' )
        inputbox.send_keys( second_item_text )
        inputbox.send_keys( Keys.ENTER )

        # The page updates again, and now shows both items on her list
        self.check_for_text_in_list_table( '1: ' + first_item_text )
        self.check_for_text_in_list_table( '2: ' + second_item_text )

        # Edith wonders whether the site will remember her list. 
        # Then she sees that the site has generated a unique URL for her 
        # there is some explanatory text to that effect.
        self.fail( 'Finish writing the test!' )

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

# run the test
if __name__ == '__main__' : 
    unittest.main()
