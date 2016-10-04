from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page

class DummyTest( TestCase ) : 

    def test_root_url_resolves_to_home_page( self ) :

        page_found = resolve( '/' )
        self.assertEqual( page_found.func , home_page ) 


    def test_home_page_returns_correct_html( self ) :

        request = HttpRequest() 
        response = home_page( request )
        self.assertTemplateUsed( 'home.html' )
        self.assertIn( b'<title>To-Do Lists</title>' , response.content )

        # self.assertTrue( response.content.startswith( b'<html>' ))
        # self.assertTrue( response.content.endswith( b'</html>' ))


    def test_home_page_can_save_a_post_request( self ) :
        
        item_text = 'A new list item' 

        request = HttpRequest() 
        request.method = 'POST'
        request.POST['item_text'] = item_text

        response = home_page( request )

        self.assertIn( item_text , response.content.decode() )

        expected_html = render_to_string( 
            'home.html' ,
            { 'new_item_text' : item_text }
        )

        self.assertEqual( response.status_code , 200)
        self.assertContains( response , item_text );
        # self.assertEqual( response.content.decode() , expected_html )

