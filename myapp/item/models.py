from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    oily = models.CharField(max_length=1)
    dry = models.CharField(max_length=1)
    sensitive = models.CharField(max_length=1)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.IntegerField()
    gender = models.CharField(max_length=6)
    monthly_sales = models.IntegerField()
    image_id = models.CharField(max_length=50)
    ingredient = models.ManyToManyField(Ingredient, through='Constitute', through_fields=('product', 'ingredient'))

    def __str__(self):
        return self.name

    def calc_score(self, skin_type):
        score = 0
        for x in [getattr(ingred, skin_type) for ingred in self.ingredient.all()]:
            score += 1 if x == "O" else -1 if x == "X" else 0
        return score

    def is_exclude(self, exclude):
        return set(self.ingredient.all()).union(set(exclude)) != set(self.ingredient.all()) or not exclude

    def is_include(self, include):
        return not set(include) - set(self.ingredient.all())


class Constitute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + "__" + self.ingredient.name
