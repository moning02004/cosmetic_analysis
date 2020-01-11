import time

from django.db.models import Q, Count, F
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Ingredient


def index(request):
    return HttpResponse("HI")


class ProductsAPI(APIView):
    __base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"

    def get(self, request):
        start = time.clock()
        skin_type = request.GET.get('skin_type')
        assert skin_type
        # get params
        include = request.GET.get('include_ingredient')
        exclude = request.GET.get('exclude_ingredient')
        category = request.GET.get('category')

        include = [Ingredient.objects.get(name=x) for x in include.split(',')] if include else []
        exclude = [Ingredient.objects.get(name=x) for x in exclude.split(',')] if exclude else []

        products = Category.objects.get(name=category).product_set.all() if category else Product.objects.all()

        extract_prod = []
        for product in products:
            ingreds = product.ingredient.all()
            if set(ingreds) - set(exclude) == set(ingreds) and not len(set(include) - set(ingreds)):
                score = len(ingreds.filter(**{skin_type: "O"})) - len(ingreds.filter(**{skin_type: "X"}))
                extract_prod.append([score, product, ingreds])

        extract_prod = sorted(extract_prod, key=lambda x: (-x[0], x[1].price))
        response = list()
        for _, product, ingred in extract_prod:
            response.append({
                'id': product.pk,
                'imgUrl': self.__base_url + product.image_id + '.jpg',
                'name': product.name,
                'price': product.price,
                'ingredients': ','.join([x.name for x in ingred]),
                'monthlySales': product.monthlySales
            })
        print(time.clock() - start)
        print(len(response))
        return Response(response, status=status.HTTP_200_OK)


class ProductAPI(APIView):
    __base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"

    def get(self, request, id):
        skin_type = request.GET.get('skin_type')
        assert skin_type

        product = Product.objects.get(pk=id)
        response = list()
        category = Category.objects.get(pk=product.category)

        return Response(status=status.HTTP_200_OK)
