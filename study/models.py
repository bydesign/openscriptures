from django.db import models

class Person(models.Model):
    """
    This represents any biblical character. It is linked to a text using the Name object.
    For example, Peter could be a person, and when referred to by Simon
    a Name is created that links to Peter.
    """
    name = models.CharField(max_length=255)
    
class Name(Selection):
    person = models.ForeignKey(Person)

class Place(Selection):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Quote(Selection):
    name = models.CharField(max_length=255)
    speaker = models.ForeignKey(Person)
    
class CrossReference(Selection):
    to = models.ForeignKey(Selection)
    description = models.TextField()