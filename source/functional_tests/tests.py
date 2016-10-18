import unittest, time 
import sys 

from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# class NewVisitorTest( unittest.TestCase ) :
# class NewVisitorTest( LiveServerTestCase ) : 
class NewVisitorTest( StaticLiveServerTestCase ) : 

    # LiveServerTestCase always assumes that you want to use its own test server
    # Sometimes, we want the ability to tell it not to bother, and use a real server instead 

    # executed once, before all tests
    @classmethod
    def setUpClass( cls ) : 

        # check to see if 'liveserver' is in our system arguments
        for arg in sys.argv : 
            if 'liveserver' in arg : 

                # skip the normal setUpClass() and store our staging server URL in a varuable called server_url
                cls.server_url = 'http://' + arg.split( '=' )[ 1 ]
                return

        # otherwise, run the regular setUpClass, and set the server_url to match the default live_server_url 
        # NOTE : in python 2.x super() has to be called with the class name and the inital argument provided 
        # in python 3, you can call super without arguments, like this: super()
        super( NewVisitorTest , cls ).setUpClass()
        cls.server_url = cls.live_server_url


#    # executed once, after all tests
#    @classmethod 
#    def tearDownClass( cls ) :
#
#        # clean up after ourselves if we happen to be running our tests on the live server 
#        if cls.server_url == cls.live_server_url: 
#            super( NewVisitorTest , cls ).tearDownClass()
            

    # executed before every test
    def setUp( self ) : 

        self.browser = webdriver.Chrome()

        # wait for 3 seconds, if needed 
        self.browser.implicitly_wait( 3 ) 


    # executed after every test 
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
        self.browser.get( self.server_url ) 
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

        # When she hits enter, she is taken to a new URL, and now the page lists:
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys( Keys.ENTER )
    
        # check that the URL reflects that the user is in the lists section
        edith_list_url = self.browser.current_url
        self.assertRegexpMatches( edith_list_url , '/lists/.+' )

        # ensure that the item entered appears on the page
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

        # A new user, Francis, comes to the website

        ## We use a new browser session to make sure no information leaks between users
        ## Meta-comments are made using two hashes
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Francis visits the home page, and there is no sign of Edith's shit
        self.browser.get( self.server_url ) 
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( first_item_text , page_text )
        self.assertNotIn( second_item_text , page_text )

        # Francis starts a list by entering a new item 
        inputbox = self.browser.find_element_by_id( 'add-new-item' )
        inputbox.send_keys( 'Buy milk' )
        inputbox.send_keys( Keys.ENTER )

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegexpMatches( francis_list_url , '/lists/.+' )
        self.assertNotEqual( francis_list_url , edith_list_url )

        # Again, there is no trace of Edith's list 
        page_text = self.browser.find_element_by_tag_name( 'body' ).text
        self.assertNotIn( first_item_text , page_text )
        self.assertNotIn( second_item_text , page_text )

        # However, Francis' item is visible on the page
        self.assertIn( 'Buy milk' , page_text )

        # Satisfied, both users leave the site


    # visual tests
    def test_styling_and_layout( self ) : 

        # Edith goes to the home page
        self.browser.get( self.server_url ) 
        self.browser.set_window_size( 1024 , 768 ) 

        # She notices the input box is nicely centered
        input_box = self.browser.find_element_by_id( 'add-new-item' ) 
        self.assertAlmostEqual( 
            input_box.location[ 'x' ] + input_box.size[ 'width' ] / 2 , 
            512 , 
            delta = 5   # works with AlmostEqual to give a +/- 5 pixel reading
        )

        # She starts a new list and notices the text is nicely centered 
        input_box.send_keys( 'testing\n' )

        input_box = self.browser.find_element_by_id( 'add-new-item' )
        self.assertAlmostEqual( 
            input_box.location[ 'x' ] + input_box.size[ 'width' ] / 2 ,
            512 , 
            delta = 5
        )


# run the test
if __name__ == '__main__' : 
    unittest.main()

