from rest_framework import serializers

from .models import Product


class ProductsSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField('get_ingredients', read_only=True)
    imgUrl = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"
        return base_url + obj.image_id + '.jpg'

    def get_ingredients(self, obj):
        return ','.join([x.name for x in obj.ingredient.all()])

    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price', 'ingredients', 'monthly_sales']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category', read_only=True)
    ingredients = serializers.SerializerMethodField('get_ingredients', read_only=True)
    imgUrl = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/"
        return base_url + obj.image_id + '.jpg'

    def get_ingredients(self, obj):
        return ','.join([x.name for x in obj.ingredient.all()])

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price', 'gender', 'category', 'ingredients', 'monthly_sales']


class ProductRecommendSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField('get_image')

    def get_image(self, obj):
        base_url = "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/"
        return base_url + obj.image_id + '.jpg'

    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price']
