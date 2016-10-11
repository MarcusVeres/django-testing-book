from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item 


def new_list( request ) :

    # create a new list item using the provided item text
    Item.objects.create( 
        text = request.POST.get( 'item_text' )
    )

    # redirect the user to a list page
    return redirect( '/lists/the-only-list-in-the-world/' )


def view_list( request ) :  

    # pull all list items 
    items = Item.objects.all() 
    return render( request , 'list.html' , { 'items' : items } )


def home_page( request ):

    if request.method == 'POST' : 

        # extract necessary data from the request 
        new_item_text = request.POST.get( 'item_text' )

        # objects.create is a shorthand for creating a new Item() without having to call save() after
        Item.objects.create( text = new_item_text )

        # "always redirect after a post"
        return redirect( '/lists/the-only-list-in-the-world/' )


    # return the home page for all other requets
    return render( request , 'home.html' )


    # return render( request , 'home.html' , {
    #     'new_item_text' : new_item_text 
    # })

    # item = Item() 
    # item.text = request.POST.get( 'item_text' , '' )
    # item.save()

    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    # return render( request , 'home.html' )

