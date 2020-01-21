from django.test import TestCase, Client

from ..models import Category, Product, Ingredient


class ProductsTestCase(TestCase):

    """      D  O  S   Price    Cat
         1   3 -1 -1    4900   base
         2   2 -1  0    3200   base
         3   2 -1  0     100   base
         4   0  2  0    4000   base
         5   3  0 -2    1900   base
         6   2  0  0   17900   skin
         7  -1  1  4   12000   skin
         8   1  2  2    8000   skin
         9   0 -1  2    9900   skin
         10 -2  2  2    9500   skin
    """

    @classmethod
    def setUpTestData(cls):
        basemakeup = Category.objects.create(name='basemakeup')
        skincare = Category.objects.create(name='skincare')

        dry1 = Ingredient.objects.create(name='dry1', dry='O', oily='X', sensitive='X')
        dry2 = Ingredient.objects.create(name='dry2', dry='O', oily='', sensitive='X')
        dry3 = Ingredient.objects.create(name='dry3', dry='O', oily='', sensitive='O')
        oily1 = Ingredient.objects.create(name='oily1', dry='', oily='O', sensitive='X')
        oily2 = Ingredient.objects.create(name='oily2', dry='X', oily='O', sensitive='O')
        sensitive1 = Ingredient.objects.create(name='sensitive1', dry='X', oily='X', sensitive='O')
        sensitive2 = Ingredient.objects.create(name='sensitive2', dry='', oily='O', sensitive='O')

        prod1 = Product(id=1, category=basemakeup, name='1_3-1-1', price=4900, gender='female', image_id='abc', monthlySales=580)
        prod1.save()
        prod1.ingredient.add(dry1, dry2, dry3)

        prod2 = Product(id=2, category=basemakeup, name='2_2-10', price=3200, gender='female', image_id='abc', monthlySales=540)
        prod2.save()
        prod2.ingredient.add(dry1, dry3)

        prod3 = Product(id=3, category=basemakeup, name='3_2-10', price=100, gender='female', image_id='abc', monthlySales=1580)
        prod3.save()
        prod3.ingredient.add(dry1, dry3)

        prod4 = Product(id=4, category=basemakeup, name='4_020', price=4000, gender='male', image_id='abc', monthlySales=1200)
        prod4.save()
        prod4.ingredient.add(oily1, sensitive2)

        prod5 = Product(id=5, category=basemakeup, name='6_30-2', price=1900, gender='all', image_id='abc', monthlySales=1299)
        prod5.save()
        prod5.ingredient.add(dry1, dry2, dry3, oily1)

        prod6 = Product(id=6, category=skincare, name='6_200', price=17900, gender='female', image_id='abc', monthlySales=990)
        prod6.save()
        prod6.ingredient.add(dry1, dry2, dry3, oily2)

        prod7 = Product(id=7, category=skincare, name='7_-114', price=12000, gender='female', image_id='abc', monthlySales=810)
        prod7.save()
        prod7.ingredient.add(dry3, oily2, sensitive1, sensitive2)

        prod8 = Product(id=8, category=skincare, name='8_122', price=8000, gender='female', image_id='abc', monthlySales=646)
        prod8.save()
        prod8.ingredient.add(dry2, dry3, oily2, sensitive2)

        prod9 = Product(id=9, category=skincare, name='9_0-12', price=9900, gender='female', image_id='abc', monthlySales=990)
        prod9.save()
        prod9.ingredient.add(dry1, dry3, oily2, sensitive1)

        prod10 = Product(id=10, category=skincare, name='10_-222', price=9500, gender='all', image_id='abc', monthlySales=1200)
        prod10.save()
        prod10.ingredient.add(oily1, oily2, sensitive1, sensitive2)