from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()


# class Item(models.Model):
#     name = models.CharField(max_length=50)
#     image_id = models.CharField(max_length=50)
#     price = models.IntegerField()
#     gender = models.CharField(max_length=6)
#     category = models.CharField(max_length=15)
#     ingredients = models.TextField(max_length=300)
#     monthlySales = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
