import unittest 
from selenium import webdriver


class NewVisitorTest( unittest.TestCase ) : 

    # executed before all tests
    def setUp( self ) : 

        self.browser = webdriver.Chrome()

        # wait for 3 seconds, if needed 
        self.browser.implicitly_wait( 3 ) 


    # executed after all tests
    def tearDown( self ) : 

        self.browser.quit()


    def test_can_create_a_list_and_retrieve_it_later( self ) :

        # Edith has heard about a cool new online to-do app. 
        # She goes to check out its homepage
        self.browser.get( 'http://localhost:9090' )

        # She notices the page title and header mention to-do lists
        self.assertIn( 'To-Do' , self.browser.title )

        self.fail( 'Finish writing the test!' )

        # She is invited to enter a to-do item straight away

        # She types "Buy peacock feathers" into a text box (Edith's hobby is tying fly-fishing lures)

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a text box inviting her to add another item. 
        # She enters "Use peacock feathers to make a fly" (Edith is very methodical)

        # The page updates again, and now shows both items on her list

        # Edith wonders whether the site will remember her list. 
        # Then she sees that the site has generated a unique URL for her 
        # there is some explanatory text to that effect.

        # She visits that URL - her to-do list is still there.

        # Satisfied, she goes back to sleep

# run the test
if __name__ == '__main__' : 
    unittest.main()

