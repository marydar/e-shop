from rest_framework import serializers
from .models import Product

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