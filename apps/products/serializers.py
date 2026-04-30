from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.products.models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "stock"]


class CategoryListSerializer(ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "products_count"]

    def get_products_count(self, obj):
        return obj.products.count()


class CategoryDetailSerializer(ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
            "products_count",
            "products",
        ]

    def get_products_count(self, obj):
        return obj.products.count()


class ProductListSerializer(ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "stock",
            "category",
        ]


class ProductDetailSerializer(ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "category",
            "created_at",
        ]
