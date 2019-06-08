from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    title = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    name = models.CharField(max_length=20)
    author = models.ForeignKey(User, models.PROTECT)
    authors = models.ManyToManyField(User, blank=True, null=True)
