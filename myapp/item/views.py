import time

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ProductsSerializer, ProductSerializer, ProductRecommendSerializer
from .models import Product, Ingredient


def index(request):
    return HttpResponse("HI")


class ProductAPI(APIView):
    def get(self, request):
        starts = time.clock()

        skin_type = request.GET.get('skin_type')
        assert skin_type
        # get params
        include = request.GET.get('include_ingredient')
        exclude = request.GET.get('exclude_ingredient')
        category = request.GET.get('category')
        page = int(request.GET.get('page')) if request.GET.get('page') else None

        # processing data
        include = [Ingredient.objects.get(name=x) for x in include.split(',')] if include else []
        exclude = [Ingredient.objects.get(name=x) for x in exclude.split(',')] if exclude else []

        products = Product.objects.prefetch_related('ingredient').select_related('category').all().order_by('price')
        if category:
            products = products.filter(category=category)

        extract_prod = []
        for product in products:
            ingredients = product.ingredient.all()
            if set(ingredients) - set(exclude) == set(ingredients) and not len(set(include) - set(ingredients)):
                score = 0
                for x in [getattr(ingred, skin_type) for ingred in ingredients]:
                    score += 1 if x == "O" else -1 if x == "X" else 0
                extract_prod.append([score, product])
        extract_prod = sorted(extract_prod, key=lambda x: x[0], reverse=True)

        response = [ProductsSerializer(product).data for _, product in extract_prod]

        if page is not None:
            max_page = len(response) // 50 if not len(response) % 50 else len(response) // 50 + 1
            if not 1 <= page <= max_page:
                return Response(status.HTTP_400_BAD_REQUEST)
            start, end = page * 50 + 1, (page + 1) * 50 + 1
            print(len(response), time.clock() - starts)
            return Response(response[start:end], status=status.HTTP_200_OK)
        print(len(response), time.clock() - starts)
        return Response(response, status=status.HTTP_200_OK)


class ProductDetailAPI(APIView):
    def get(self, request, id):
        start = time.clock()
        skin_type = request.GET.get('skin_type')
        assert skin_type

        product = Product.objects.prefetch_related('ingredient').select_related('category').get(pk=id)
        response = list()
        response.append(ProductSerializer(product).data)

        recommend = Product.objects.prefetch_related('ingredient').select_related('category'). \
            filter(category=product.category).order_by('price')

        extract_prod = []
        for product in recommend:
            ingredients = product.ingredient.all()
            score = 0
            for x in [getattr(ingred, skin_type) for ingred in ingredients]:
                score += 1 if x == "O" else -1 if x == "X" else 0
            extract_prod.append([score, product])

        extract_prod = sorted(extract_prod, key=lambda x: x[0], reverse=True)[:3]
        for _, prod in extract_prod:
            response.append(ProductRecommendSerializer(prod).data)
        print(len(response), time.clock() - start)
        return Response(response, status=status.HTTP_200_OK)