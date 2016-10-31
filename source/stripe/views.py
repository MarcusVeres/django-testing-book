from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def stripe_home( request ) : 
    return render( request , 'stripe/stripe-home.html' )

