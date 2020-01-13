from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Category, Ingredient


def index(request):
    return HttpResponse("HI")


class ProductAPI(APIView):
    __base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"

    def get(self, request):
        skin_type = request.GET.get('skin_type')
        assert skin_type
        # get params
        include = request.GET.get('include_ingredient')
        exclude = request.GET.get('exclude_ingredient')
        category = request.GET.get('category')
        page = int(request.GET.get('page')) if request.GET.get('page') else None

        include = [Ingredient.objects.get(name=x) for x in include.split(',')] if include else []
        exclude = [Ingredient.objects.get(name=x) for x in exclude.split(',')] if exclude else []

        products = Product.objects.prefetch_related('ingredient').select_related('category').filter(category=category).order_by('price')\
            if category else Product.objects.prefetch_related('ingredient').select_related('category').all().order_by('price')
        extract_prod = []

        for product in products:
            ingreds = product.ingredient.all()
            if set(ingreds) - set(exclude) == set(ingreds) and not len(set(include) - set(ingreds)):
                score = 0
                for x in list(ingreds.values_list(skin_type, flat=True)):
                    score += 1 if x == "O" else -1 if x == "X" else 0
                extract_prod.append([score, product])

        extract_prod = sorted(extract_prod, key=lambda x: (-x[0]))

        response = list()
        for _, product in extract_prod:
            response.append({
                'id': product.pk,
                'imgUrl': self.__base_url + product.image_id + '.jpg',
                'name': product.name,
                'price': product.price,
                'ingredients': ','.join([x.name for x in product.ingredient.all()]),
                'monthlySales': product.monthlySales
            })
        start = page * 50 + 1 if page else 0
        end = (page + 1) * 50 + 1 if page else len(response)
        return Response(response[start:end], status=status.HTTP_200_OK)


class ProductDetailAPI(APIView):
    __base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"

    def get(self, request, id):
        skin_type = request.GET.get('skin_type')
        assert skin_type

        product = Product.objects.prefetch_related('ingredient').select_related('category').get(pk=id)
        recommend = Product.objects.prefetch_related('ingredient').select_related('category').\
            filter(category=product.category).order_by('price')
        print(len(recommend))
        response = [{
            'id': product.pk,
            'imgUrl': self.__base_url + product.image_id + '.jpg',
            'name': product.name,
            'price': product.price,
            'gender': product.gender,
            'category': product.category.name,
            'ingredients': ','.join([x.name for x in product.ingredient.all()]),
            'monthlySales': product.monthlySales
        }]

        extract_prod = []
        for product in recommend:
            ingreds = product.ingredient.all()
            score = 0
            for x in list(ingreds.values_list(skin_type, flat=True)):
                score += 1 if x == "O" else -1 if x == "X" else 0
            extract_prod.append([score, product])

        extract_prod = sorted(extract_prod, key=lambda x: (-x[0]))[:3]
        for _, x in extract_prod:
            response.append({
                'id': x.pk,
                'imgUrl': self.__base_url + x.image_id + '.jpg',
                'name': x.name,
                'price': x.price,
            })
        return Response(response, status=status.HTTP_200_OK)
