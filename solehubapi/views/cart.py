from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, status
from solehubapi.models import Cart, Order, Product, User

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
        user = request.query_params.get('customer_id', None)
        status = request.query_params.get('status')
        order_id = request.query_params.get('order_id')        
        cart = Cart.objects.all()


        if user is not None:
            userId = User.objects.get(pk=user)
            cart = Cart.objects.filter(order_id__customer_id=userId)
            
        if order_id is not None:  # Check if order_id parameter is provided
            cart = cart.filter(order_id=order_id)  # Filter by order_id
        
        if status is not None:
            
            if status.lower() in ['true', 'false']:
                status = status.lower() == 'true'
                cart = cart.filter(order_id__status=status)
            else:
                return Response({'message': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST) 
                
        serializer = CartSerialzer(cart, many=True)
        return Response(serializer.data)
      
    def create(self, request):
 
        print(request.data)
        userId = User.objects.get(pk=request.data["userId"])
        orderId, _ = Order.objects.get_or_create(customer_id=userId, status=True)
        productId = Product.objects.get(pk=request.data["productId"])

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
        cart_id = pk  # Assuming you're passing cart ID in the URL
        cart = Cart.objects.all()
        
        order_id = request.query_params.get('order_id', None)
        status_param = request.query_params.get('status', None)
        
        if order_id is not None:
            try:
                order_id = int(order_id)
            except ValueError:
                return Response({'message': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)
            
        if cart_id:
            cart = cart.filter(id=cart_id)
            
        if order_id is not None:
            cart = cart.filter(order_id=order_id)
            
        if status_param is not None:
            if status_param.lower() in ['true', 'false']:
                status_value = status_param.lower() == 'false'
                cart = cart.filter(order__status=status_value)
            else:
                return Response({'message': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
           
        cart.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
    # @action(methods=['delete'], detail=True)
    # def remove(self, request, pk):
    #     """Delete request for a user to leave an event"""

    #     user = User.objects.get(pk=pk)
    #     order = Order.objects.get(customer_id=user, open=True)
    #     product = Product.objects.get(pk=pk)
    #     cart_products = Cart.objects.filter(product_id=product, order_id=order)
    #     cart_products.delete()
    #     if not Cart.objects.filter(order_id=order).exists():
    #         order.delete()

    #     return Response({'message': 'Remove favorite'}, status=status.HTTP_204_NO_CONTENT)
    

class CartSerialzer(serializers.ModelSerializer):
    """JSON serializer for carts
    """
    class Meta:
        model = Cart
        fields = ('id', 'order_id', 'product_id')
        depth = 1

    