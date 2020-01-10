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
        skin_type = request.GET.get('skin_type')
        assert skin_type

        include = [Ingredient.objects.get(name=x) for x in request.GET.get('include_ingredient').split(',')] \
            if request.GET.get('include_ingredient') else []
        exclude = [Ingredient.objects.get(name=x) for x in request.GET.get('exclude_ingredient').split(',')] \
            if request.GET.get('exclude_ingredient') else []
        category = Category.objects.get(name=request.GET.get('category')) \
            if request.GET.get('category') else None

        extract_prod = []
        products = Product.objects.all()
        if category:
            products = products.filter(category=category)

        for product in products:
            ingreds = product.ingredient.all()
            if set(ingreds) - set(exclude) == set(ingreds) and not len(set(include) - set(ingreds)):
                score = len(product.ingredient.filter(**{skin_type: "O"})) - len(product.ingredient.filter(**{skin_type: "X"}))
                extract_prod.append([score, product])

        extract_prod = sorted(extract_prod, key=lambda x: (-x[0], x[1].price))
        response = list()
        for _, product in extract_prod:
            response.append({
                'score': _,
                'id': product.pk,
                'imgUrl': self.__base_url + product.image_id + '.jpg',
                'name': product.name,
                'price': product.price,
                'ingredients': ','.join([x.name for x in product.ingredient.all()]),
                'monthlySales': product.monthlySales
            })
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
