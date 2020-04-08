import time

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Ingredient
from .serializers import ProductsSerializer, ProductSerializer, ProductRecommendSerializer
from ..pagination import OnlyBodyPagination


def index(request):
    return HttpResponse("HI")


class ProductAPI(ListAPIView):
    serializer_class = ProductsSerializer
    pagination_class = OnlyBodyPagination

    def get_queryset(self):
        params = self.request.query_params
        self.pagination_class = None if not params.get('page') else self.pagination_class

        category = params.get('category')
        include = params.get('include_ingredient')
        exclude = params.get('include_ingredient')

        product_list = Product.objects.prefetch_related('ingredient').select_related('category').all().order_by('price')
        if category:
            product_list = product_list.filter(category=category)

        include = [Ingredient.objects.get(name=x) for x in include.split(',')] if include else []
        exclude = [Ingredient.objects.get(name=x) for x in exclude.split(',')] if exclude else []

        product_list = [[product.calc_score(params.get('skin_type')), product] \
                        for product in product_list if product.is_exclude(exclude) and product.is_include(include)]
        product_list = [product for _, product in sorted(product_list, key=lambda x: -x[0])]
        return product_list

    def get(self, request, *args, **kwargs):
        if 'skin_type' not in request.query_params.keys():
            return Response({'detail': "'skin_type' is required"}, status=status.HTTP_400_BAD_REQUEST)
        return super().get(request)


class ProductDetailAPI(APIView):

    # 상품 소개와는 상관없이 추천 상품에도 해당 상품도 표시한다.
    # 추천하는 최상위 상품이 소개된 상품보다 더 좋은지 안 좋은지 알 수 없기 때문이다.
    # 가격이나 성분만으로 소비자는 구분하기 어렵다.
    def get(self, request, id):
        skin_type = request.GET.get('skin_type')
        assert skin_type

        product = Product.objects.prefetch_related('ingredient').select_related('category').get(pk=id)
        recommend = Product.objects.prefetch_related('ingredient').select_related('category'). \
            filter(category=product.category).order_by('price')

        extract_prod = []
        for prod in recommend:
            score = prod.calc_score(skin_type)
            extract_prod.append([score, prod])
        extract_prod = sorted(extract_prod, key=lambda x: x[0], reverse=True)[:3]

        response = list()
        response.append(ProductSerializer(product).data)
        response.extend(ProductRecommendSerializer(prod).data for _, prod in extract_prod)
        return Response(response, status=status.HTTP_200_OK)
