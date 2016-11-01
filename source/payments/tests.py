from django.core.urlresolvers import resolve 
from django.test import TestCase

import stripe
from payments.views import stripe_home

class HomePageTests( TestCase ) : 

    def test_stripe_root_resolves_to_stripe_home_page( self ) : 
        page_found = resolve( '/payments/' )
        self.assertEqual( page_found.func , stripe_home )

    def test_stripe_root_uses_correct_template( self ) :
        response = self.client.get( '/payments/' )
        self.assertTemplateUsed( response , 'payments/stripe-home.html' )


class PaymentProcessTest( TestCase ):

    def test_payment_process_receives_a_token( self ) :
        return

    def test_charge_test_credit_card( self ) :

        stripe.api_key = 'sk_test_Qh6X6qmJeoFgMlqEJKtDFx5g'

        resp = stripe.Charge.create(
            amount = 200,
            currency = 'cad',
            card = {
                'number': '4242424242424242',
                'exp_month': 10,
                'exp_year': 2018
            },
            description = 'customer@gmail.com'
        )

        return

