from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from solehubapi.models import Cart, Order, Product

class CartView(ViewSet):
  
    def retrieve(self, request, pk):
          """Handle GET requests for single cart
          Returns:
              Response -- JSON serialized cart 
          """
          try:
              cart = Cart.objects.get(pk=pk)
              serializer = CartSerialzer(cart)
              return Response(serializer.data)
          except Cart.DoesNotExist:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all cart 

        Returns:
            Response -- JSON serialized list of cart
        """
        cart = Cart.objects.all()
        serializer = CartSerialzer(cart, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
      
    def create(self, request):
 
       
        orderId = Order.objects.get(pk=request.data["order_id"])
        productId = Product.objects.get(pk=request.data["product_id"])

        cart = Cart.objects.create(
            order_id = orderId,
            product_id =productId 
        )
        serializer = CartSerialzer(cart)
        return Response(serializer.data)  

    def update(self, request, pk):
          
            cart = Cart.objects.get(pk=pk)
            cart.product_id= Product.objects.get(pk=request.data["product_id"])
            cart.order_id = Order.objects.get(pk=request.data["order_id"])
            
            cart.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        
    def destroy(self, request, pk):
        cart = Cart.objects.get(pk=pk)
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      

        
class CartSerialzer(serializers.ModelSerializer):
    """JSON serializer for carts
    """
    class Meta:
        model = Cart
        fields = ('id', 'order_id', 'product_id')

    