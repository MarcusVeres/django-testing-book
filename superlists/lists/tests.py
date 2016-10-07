from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item 
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


    def test_home_page_only_saves_items_when_necessary( self ) :

        request = HttpRequest()
        home_page( request )
        self.assertEqual( Item.objects.count() , 0 )


class ItemModelTest( TestCase ) : 
    
    def test_saving_and_retrieving_items( self ) : 

        first_item = Item() 
        first_item.text = 'The first (ever) list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        third_item = Item()
        third_item.text = 'The third item'
        third_item.save()

        saved_items = Item.objects.all()
        self.assertEqual( saved_items.count() , 3 )

        first_saved_item = saved_items[ 0 ] 
        second_saved_item = saved_items[ 1 ] 
        third_saved_item = saved_items[ 2 ] 

        self.assertEqual( first_saved_item.text , 'The first (ever) list item' )
        self.assertEqual( second_saved_item.text , 'The second item' )
        self.assertEqual( third_saved_item.text , 'The third item' )


class ListViewTest( TestCase ) : 

    def test_uses_list_template( self ) :

        response = self.client.get( '/lists/the-only-list-in-the-world/' )
        self.assertTemplateUsed( response , 'list.html' )


    def test_can_save_a_post_request( self ) :
        
        item_text = 'A new list item'

        request = HttpRequest()
        request.method = 'POST'
        request.POST[ 'item_text' ] = item_text

        response = home_page( request )

        # check that one new item has been saved to the database
        self.assertEqual( Item.objects.count() , 1 )

        # verify that the object's text matches what we tried to save
        new_item = Item.objects.first()
        self.assertEqual( new_item.text , item_text ) 


    def test_redirects_after_a_post_request( self ) :

        item_text = 'A new list item' 

        request = HttpRequest()
        request.method = 'POST'
        request.POST[ 'item_text' ] = item_text 

        response = home_page( request ) 

        self.assertEqual( response.status_code , 302 ) 
        self.assertEqual( response[ 'location' ] , '/lists/the-only-list-in-the-world/' )


    def test_displays_all_items( self ) :

        item_1_text = 'Some item'
        item_2_text = 'Another item' 

        Item.objects.create( text = item_1_text )
        Item.objects.create( text = item_2_text )

        # use Django test client to retrieve URL, instead of calling the view directly
        response = self.client.get( '/lists/the-only-list-in-the-world/' )

        self.assertContains( response , item_1_text )
        self.assertContains( response , item_2_text )


# reference : 

    # def test_some_example :

        # self.assertEqual( response.status_code , 200)
        # self.assertContains( response , item_text );
        # self.assertEqual( response.content.decode() , expected_html )

