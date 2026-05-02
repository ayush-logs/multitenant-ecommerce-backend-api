from django.db.models import Sum
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.carts.models import Cart, CartItem
from apps.products.models import Product


class CartItemProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = CartItemProductSerializer(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "subtotal"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "item_count"]

    def get_item_count(self, obj):
        return obj.items.aggregate(total=Sum("quantity"))["total"] or 0


class CartItemAddSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]

    def validate(self, attrs):
        product = attrs["product"]
        quantity = attrs["quantity"]

        if quantity > product.stock:
            raise serializers.ValidationError(
                {"quantity": "Requested quantity exceeds available stock."}
            )
        return attrs

    def create(self, validated_data):
        cart = validated_data["cart"]
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={"quantity": quantity}
        )

        if not created:
            item.quantity = item.quantity + quantity
            item.save()

        return item


class CartItemUpdateSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["id", "quantity"]

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be greater than 0.")
        if value > self.instance.product.stock:
            raise serializers.ValidationError("Quantity exceeds available stock.")
        return value
