from django.core.urlresolvers import resolve
from django.test import TestCase
from lists.views import home_page


class DummyTest( TestCase ) : 

    def test_root_url_resolves_to_home_page( self ) :

        page_found = resolve( '/' )
        self.assertEqual( page_found.func , home_page ) 



# don't forget about templateUsed()

