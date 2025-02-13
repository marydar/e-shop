from rest_framework import serializers
from .models import Product, Cart, CartItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'category', 'price']
        
class DetailedProductSerializer(serializers.ModelSerializer):
    similar_products = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'image', 'description', 'price', 'similar_products']

    def get_similar_products(self, product):
        similar_products = Product.objects.filter(category=product.category).exclude(id=product.id)
        serializer = ProductSerializer(similar_products, many=True)
        return serializer.data
    
    
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'created_at', 'modified_at']
        
class SimpleCartSerializer(serializers.ModelSerializer):
    number_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'number_of_items']
        
    def get_number_of_items(self, cart):
        number_of_items = sum([item.quantity for item in cart.items.all()])
        return number_of_items
        
class CartItemSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
    Cart = CartSerializer(read_only=True)
    class Meta:
        model = CartItem    
        fields = ['id', 'quantity', 'Product', 'Cart']