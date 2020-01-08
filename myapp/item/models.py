from django.db import models


def image_path(instance, filename):
    return 'image/{}'.format(filename)


def thumbnail_path(instance, filename):
    return 'image/{}'.format(filename)


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    gender = models.CharField(max_length=6)
    category = models.CharField(max_length=15)
    ingredients = models.TextField(max_length=300)
    monthlySales = models.IntegerField()

    thumbnail = models.ImageField(upload_to=thumbnail_path)
    image = models.ImageField(upload_to=image_path)
    image_id = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    oily = models.CharField(max_length=1, default="")
    dry = models.CharField(max_length=1, default="")
    sensitive = models.CharField(max_length=1, default="")

    def __str__(self):
        return self.name
