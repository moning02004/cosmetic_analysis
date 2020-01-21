import json

from django.test import TestCase, Client

from myapp.item.models import Category, Product, Ingredient
from .data_setup import ProductsTestCase


class TestCase1(ProductsTestCase):

    def test_basemakeup_dry(self):
        client = Client()
        response = client.get('/product/1/', {'skin_type': 'dry'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [1, 5, 1, 3])

    def test_skincare_oily(self):
        client = Client()
        response = client.get('/product/6/', {'skin_type': 'oily'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [6, 8, 10, 7])

    def test_skincare_sensitive(self):
        client = Client()
        response = client.get('/product/9/', {'skin_type': 'sensitive'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [9, 7, 8, 10])

