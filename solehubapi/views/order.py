"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from solehubapi.models import Order, User

class OrderView(ViewSet):
    """Level up Order view"""

    def create(self, request):
        """Handle GET requests for single order

        Returns:
            Response -- JSON serialized order
        """

        custId = User.objects.get(pk=request.data["customer_id"])
        
        order = Order.objects.create(
            status=request.data["status"],
            customer_id=custId,
            payment_type=request.data["payment_type"]
            
        )
        serializer = OrderSerializer(order)
        return Response(serializer.data)
  
    def retrieve(self, request, pk):
      try:
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
      except order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk):
        """Handle PUT requests for a order

        Returns:
            Response -- Empty body with 204 status code
        """

        order = Order.objects.get(pk=pk)
        order.status = request.data["status"]
        order.customer_id = User.objects.get(pk=request.data["customer_id"])
        order.payment_type = request.data["payment_type"]
        order.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to get all category

        Returns:
            Response -- JSON serialized list of category
        """
        order = Order.objects.all()
        
        customer_id = request.query_params.get('customer_id', None)
        status = request.query_params.get('status')
    
        if customer_id is not None:
            try:
                # customer_id query param is converted to an integer
                customer_id = int(customer_id)
            except ValueError:
                return Response({'message': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)
                 
            #filter orders by customer_id
            order = order.filter(customer_id=customer_id)
            
        if status is not None:
            if status.lower() in ['true', 'false']:
                status = status.lower() == 'true'
                order = order.filter(status=status)
            else:
                return Response({'message': 'Invalid status value'}, status=status.HTTP_400_BAD_REQUEST)
                
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
            
    def destroy(self, request, pk):
        order = Order.objects.get(pk=pk)
        order.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      

class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = Order
        fields = ('id', 'customer_id', 'status', 'payment_type')
        depth = 1
