from django.shortcuts import render
from django.http import HttpResponse

import stripe

# Create your views here.
def stripe_home( request ) : 
    return render( request , 'payments/stripe-home.html' )


def stripe_process( request ) :

    # Set your secret key: remember to change this to your live secret key in production
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    stripe.api_key = "sk_test_Qh6X6qmJeoFgMlqEJKtDFx5g"

    # Get the credit card details submitted by the form
    token = request.POST['stripeToken']

    if not token : 
        print "no token was provided"

    else : 
        print "got a token!"
        print token

    # return HttpResponse( request , token )

    # Create a charge: this will charge the user's card
    try:
        charge = stripe.Charge.create(
            amount = 1000 , # Amount in cents
            currency = "cad" ,
            source = token ,
            description = "Example charge"
        )
    except stripe.error.CardError as e:
        # The card has been declined
        pass

    return HttpResponse( token )

