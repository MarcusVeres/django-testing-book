from django.http import HttpResponse
from django.shortcuts import render

from lists.models import Item 


def home_page( request ):

    # create a new to-do item, grab its details, and save it to the database 
    item = Item() 
    item.text = request.POST.get( 'item_text' , '' )
    item.save()

    return render( request , 'home.html' , {
        'new_item_text' : item.text
    })

    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    # return render( request , 'home.html' )

