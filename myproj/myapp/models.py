from __future__ import unicode_literals

from django.db import models


class Bar(models.Model):                                                        
    pass                                                                        


class Foo(models.Model):                                                        
    class Meta:                                                                 
        order_with_respect_to = 'bar'                                           
        unique_together = ('bar', '_order')                                     

    bar = models.ForeignKey(Bar)
