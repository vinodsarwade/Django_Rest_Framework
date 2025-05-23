from django.db import models

# Create your models here.
class Author(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length = 50)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

class Book(models.Model):
    title = models.CharField(max_length = 50)
    rating = models.CharField(max_length=10)
    author = models.ForeignKey(Author, related_name = 'books', on_delete= models.CASCADE )
