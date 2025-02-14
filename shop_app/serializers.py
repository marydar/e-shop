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
    

class CartItemSerializer(serializers.ModelSerializer):
    Product = ProductSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    class Meta:
        model = CartItem    
        fields = ['id', 'quantity', 'Product', 'total']
    def get_total(self, cart_item):
        price = cart_item.Product.price * cart_item.quantity
        return price
        
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(read_only=True, many=True)
    sum_total = serializers.SerializerMethodField()
    num_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'items', 'sum_total', 'num_of_items', 'created_at', 'modified_at']
        
    def get_sum_total(self, cart):
        items = cart.items.all()
        total = sum([item.quantity * item.Product.price for item in items])
        return total
    
    def get_num_of_items(self, cart):
        num_of_items = cart.items.all()
        total = sum([item.quantity for item in num_of_items])
        return total
        
class SimpleCartSerializer(serializers.ModelSerializer):
    number_of_items = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'cart_code', 'number_of_items']
        
    def get_number_of_items(self, cart):
        number_of_items = sum([item.quantity for item in cart.items.all()])
        return number_of_items
        
