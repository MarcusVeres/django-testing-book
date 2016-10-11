from __future__ import unicode_literals

from django.db import models


class List( models.Model ) : 
    
    pass


class Item( models.Model ) : 

    # the TextField is not null-able, so we'll need to provide a default value
    text = models.TextField( default = '' ) 

    # create a foreign key to a different object
    # NOTE : without a default, Items *must* have a list set
    list = models.ForeignKey( List , default = None )

