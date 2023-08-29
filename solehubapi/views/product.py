"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from solehubapi.models import User, Product

class ProductView(ViewSet):
    """Level up products view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except product.DoesNotExist:
          return Response({'message': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all products

        Returns:
            Response -- JSON serialized list of products
        """
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def create(self, request):
 
        userId = User.objects.get(pk=request.data["userId"])
        sellerId = User.objects.get(uid=request.data["sellerId"])

        product = Product.objects.create(
            name=request.data["name"],
            image=request.data["image"],
            description=request.data["description"],
            condition=request.data["condition"],
            price=request.data["price"],
            color=request.data["color"],
            brand=request.data["brand"],
            seller_id=sellerId,
            user_id=userId    
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.image = request.data["image"]
        product.description=request.data["description"]
        product.price=request.data["price"]
        product.color=request.data["color"]        
        product.brand=request.data["brand"]
        product.seller_id= User.objects.get(uid=request.data["sellerId"])
        product.user_id= User.objects.get(pk=request.data["userId"])
       

        product.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Product
        fields = ('id' ,'name', 'image', 'description','seller_id', 'price','brand','color','user_id')
        depth = 1
