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
        for prod in products:
            ingredients = prod.ingredient.all()
            if set(ingredients) - set(exclude) == set(ingredients) and not len(set(include) - set(ingredients)):
                score = 0
                for x in [getattr(ingred, skin_type) for ingred in ingredients]:
                    score += 1 if x == "O" else -1 if x == "X" else 0
                extract_prod.append([score, prod])
        extract_prod = sorted(extract_prod, key=lambda x: x[0], reverse=True)

        response = [ProductsSerializer(product).data for _, product in extract_prod]

        if page is not None:
            max_page = len(response) // 50 if not len(response) % 50 else len(response) // 50 + 1
            if not 1 <= page <= max_page:
                return Response(status.HTTP_400_BAD_REQUEST)
            start, end = page * 50 + 1, (page + 1) * 50 + 1
            return Response(response[start:end], status=status.HTTP_200_OK)
        return Response(response, status=status.HTTP_200_OK)


class ProductDetailAPI(APIView):
    def get(self, request, id):
        skin_type = request.GET.get('skin_type')
        assert skin_type

        # 상품 소개와는 상관없이 추천 상품에도 해당 상품도 표시한다.
        # 추천하는 최상위 상품이 소개된 상품보다 더 좋은지 안 좋은지 알 수 없기 때문이다.
        # 가격이나 성분만으로 소비자는 구분하기 어렵다.
        product = Product.objects.prefetch_related('ingredient').select_related('category').get(pk=id)
        recommend = Product.objects.prefetch_related('ingredient').select_related('category'). \
            filter(category=product.category).order_by('price')

        extract_prod = []
        for prod in recommend:
            ingredients = prod.ingredient.all()
            score = 0
            for x in [getattr(ingred, skin_type) for ingred in ingredients]:
                score += 1 if x == "O" else -1 if x == "X" else 0
            extract_prod.append([score, prod])
        extract_prod = sorted(extract_prod, key=lambda x: x[0], reverse=True)[:3]

        response = list()
        response.append(ProductSerializer(product).data)
        response.extend(ProductRecommendSerializer(prod).data for _, prod in extract_prod)
        return Response(response, status=status.HTTP_200_OK)