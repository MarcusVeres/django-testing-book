from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page( request ):

    return render( request , 'home.html' , {
        # 'new_item_text' : request.POST['item_text']
        'new_item_text' : request.POST.get( 'item_text' , '' )
    })

    # return HttpResponse('<html><title>To-Do Lists</title></html>')
    # return render( request , 'home.html' )
