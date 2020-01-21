import json

from django.test import TestCase, Client

from myapp.item.models import Category, Product, Ingredient
from .data_setup import ProductsTestCase


class TestCase1(ProductsTestCase):

    def test_dry_products(self):
        client = Client()
        response = client.get('/products/', {'skin_type': 'dry'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [5, 1, 3, 2, 6, 8, 4, 9, 7, 10])

    def test_oily_products(self):
        client = Client()
        response = client.get('/products/', {'skin_type': 'oily'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [4, 8, 10, 7, 5, 6, 3, 2, 1, 9])

    def test_sensitive_products(self):
        client = Client()
        response = client.get('/products/', {'skin_type': 'sensitive'})
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [7, 8, 10, 9, 3, 2, 4, 6, 1, 5])

    def test_parameter_exclude(self):
        client = Client()
        params = {'skin_type': 'dry', 'exclude_ingredient': 'dry1'} # dry1 exclude prod : 4 7 8 10
        response = client.get('/products/', params)
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [8, 4, 7, 10])

    def test_parameter_exclude_two(self):
        client = Client()
        params = {'skin_type': 'dry', 'exclude_ingredient': 'dry1,dry2'} # dry1, dry2 exclude prod : 2 3 4 7 8 9 10
        response = client.get('/products/', params)
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [3, 2, 8, 4, 9, 7, 10])

    def test_parameter_include(self):
        client = Client()
        params = {'skin_type': 'oily', 'include_ingredient': 'dry2'} # dry2 prod : 1 5 6 8
        response = client.get('/products/', params)
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [8, 5, 6, 1])

    def test_parameter_exc_inc(self):
        client = Client()
        params = {'skin_type': 'sensitive', 'exclude_ingredient': 'dry2', 'include_ingredient': 'dry1'}  # prod : 2 3 9
        response = client.get('/products/', params)
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [9, 3, 2])

    def test_parameter_category(self):
        client = Client()
        params = {'skin_type': 'sensitive', 'category': 'skincare'} # prod : 6 7 8 9 10
        response = client.get('/products/', params)
        res = [x.get('id') for x in response.json()]
        self.assertEqual(res, [7, 8, 10, 9, 6])
