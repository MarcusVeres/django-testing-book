from __future__ import unicode_literals

from django.db import models


class Item( models.Model ) : 

    # the TextField is not null-able, so we'll need to provide a default value
    text = models.TextField( default = '' ) 

