from django.http import HttpResponse
from django.shortcuts import redirect, render

from lists.models import Item , List


def view_list( request , list_id ) :  

    current_list = List.objects.get( id = list_id )
    return render( request , 'list.html' , { 'list' : current_list } )
    # items = Item.objects.filter( list = current_list ) 


def new_list( request ) :

    # create a new parent list for the item to belong to
    a_list = List.objects.create()

    # create a new list item using the provided item text
    Item.objects.create( 
        text = request.POST.get( 'item_text' ) , 
        list = a_list , 
    )

    # redirect the user to a list page
    return redirect( '/lists/%d/' % a_list.id )


def add_item( request , list_id ) : 

    item_text = request.POST.get( 'item_text' )
    current_list = List.objects.get( id = list_id ) 

    Item.objects.create(
        text = item_text , 
        list = current_list
    )

    return redirect( '/lists/%d/' % current_list.id )


def home_page( request ):

    return render( request , 'home.html' )

    # return render( request , 'home.html' , {
    #     'new_item_text' : new_item_text 
    # })

    # item = Item() 
    # item.text = request.POST.get( 'item_text' , '' )
    # item.save()

    # new_item_text = request.POST.get( 'item_text' )
    # Item.objects.create( text = new_item_text )

    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    # return render( request , 'home.html' )

