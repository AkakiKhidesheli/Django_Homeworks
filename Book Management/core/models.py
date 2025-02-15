from django.db import models


# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name


class Languages(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'languages'

    def __str__(self):
        return self.name


class Books(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    author = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, related_name='books', null=True, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shelf = models.PositiveIntegerField(null=True, blank=True)
    genre = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='books', null=True, blank=True)

    class Meta:
        db_table = 'books'
