from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.models import Item , List
from lists.views import home_page

class HomePageTest( TestCase ) : 

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


class ListAndItemModelsTest( TestCase ) : 
    
    def test_saving_and_retrieving_items( self ) : 

        a_list = List()
        a_list.save()

        first_item = Item() 
        first_item.text = 'The first (ever) list item'
        first_item.list = a_list
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.list = a_list
        second_item.save()

        third_item = Item()
        third_item.text = 'The third item'
        third_item.list = a_list
        third_item.save()

        saved_list = List.objects.first()
        self.assertEqual( saved_list , a_list )

        saved_items = Item.objects.all()
        self.assertEqual( saved_items.count() , 3 )

        first_saved_item = saved_items[ 0 ] 
        second_saved_item = saved_items[ 1 ] 
        third_saved_item = saved_items[ 2 ] 

        self.assertEqual( first_saved_item.text , 'The first (ever) list item' )
        self.assertEqual( second_saved_item.text , 'The second item' )
        self.assertEqual( third_saved_item.text , 'The third item' )

        # lists are compared by checking if their primary key (.id attribute) is the same 
        self.assertEqual( first_saved_item.list , a_list )
        self.assertEqual( second_saved_item.list , a_list )
        self.assertEqual( third_saved_item.list , a_list )


    def test_can_save_a_post_request( self ) :
        
        item_text = 'A new list item'

        self.client.post(
            '/lists/new' , 
            data = {
                'item_text' : item_text 
            }
        )

        # check that one new item has been saved to the database
        self.assertEqual( Item.objects.count() , 1 )

        # verify that the object's text matches what we tried to save
        new_item = Item.objects.first()
        self.assertEqual( new_item.text , item_text ) 


    def test_redirects_after_a_post_request( self ) :

        item_text = 'A new list item' 

        response = self.client.post( 
            '/lists/new' , 
            data = {
                'item_text' : item_text  
            }
        )

        # grab the list item we just created 
        new_list = List.objects.first()
        
        self.assertRedirects( response , '/lists/%d/' % new_list.id )

        # self.assertRedirects( response , '/lists/the-only-list-in-the-world/' )
        # self.assertEqual( response.status_code , 302 ) 
        # self.assertEqual( response[ 'location' ] , '/lists/the-only-list-in-the-world/' )


    def test_displays_all_items( self ) :

        a_list = List.objects.create()

        item_1_text = 'Some item'
        item_2_text = 'Another item' 

        Item.objects.create( text = item_1_text , list = a_list )
        Item.objects.create( text = item_2_text , list = a_list )

        # use Django test client to retrieve URL, instead of calling the view directly
        response = self.client.get( '/lists/%d/' % a_list.id )

        self.assertContains( response , item_1_text )
        self.assertContains( response , item_2_text )


class ListViewTest( TestCase ) : 

    def test_uses_list_template( self ) :

        a_list = List.objects.create()
        response = self.client.get( '/lists/%d/' % a_list.id )
        self.assertTemplateUsed( response , 'list.html' )


    def test_list_only_displays_its_own_items ( self ) :

        list_1_item_1 = 'Some item'
        list_1_item_2 = 'Another item'
        list_2_item_1 = 'Wrong item'
        list_2_item_2 = 'Another incorrect item'

        correct_list = List.objects.create() 
        Item.objects.create( text = list_1_item_1 , list = correct_list )
        Item.objects.create( text = list_1_item_2 , list = correct_list )

        wrong_list = List.objects.create()
        Item.objects.create( text = list_2_item_1 , list = wrong_list )
        Item.objects.create( text = list_2_item_2 , list = wrong_list )

        # submit the page and check its contents
        response = self.client.get( '/lists/%d/' % (correct_list.id,) )

        self.assertContains( response , list_1_item_1 )
        self.assertContains( response , list_1_item_2 )
        self.assertNotContains( response , list_2_item_1 )
        self.assertNotContains( response , list_2_item_2  )


# reference : 

    # def test_some_example :

        # self.assertEqual( response.status_code , 200)
        # self.assertContains( response , item_text );
        # self.assertEqual( response.content.decode() , expected_html )

