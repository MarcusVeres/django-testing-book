from django.core.urlresolvers import resolve 
from django.test import TestCase

from stripe.views import stripe_home

class HomePageTests( TestCase ) : 

    def test_stripe_root_resolves_to_stripe_home_page( self ) : 
        page_found = resolve( '/stripe/' )
        self.assertEqual( page_found.func , stripe_home )

    def test_stripe_root_uses_correct_template( self ) :
        response = self.client.get( '/stripe/' )
        self.assertTemplateUsed( response , 'stripe/stripe-home.html' )

