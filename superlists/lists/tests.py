from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

class DummyTest( TestCase ) : 

    def test_root_url_resolves_to_home_page( self ) :

        page_found = resolve( '/' )
        self.assertEqual( page_found.func , home_page ) 


    def test_home_page_returns_correct_html( self ) :

        request = HttpRequest() 
        response = home_page( request )
        self.assertTrue( response.content.startswith( b'<html>' ))
        self.assertIn( b'<title>To-Do Lists</title>' , response.content )
        self.assertTrue( response.content.endswith( b'</html>' ))

# don't forget about templateUsed()

