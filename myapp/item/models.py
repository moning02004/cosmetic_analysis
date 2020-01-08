from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    oily = models.CharField(max_length=1, default="")
    dry = models.CharField(max_length=1, default="")
    sensitive = models.CharField(max_length=1, default="")

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    gender = models.CharField(max_length=6)
    monthlySales = models.IntegerField()
    image_id = models.CharField(max_length=50)
    ingredient = models.ManyToManyField(Ingredient, through='Constitute', through_fields=('product', 'ingredient'))

    def __str__(self):
        return self.name


class Constitute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + "__" + self.ingredient.name