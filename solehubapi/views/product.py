"""View module for handling requests about products"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from solehubapi.models import User, Product, Order, Cart

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
        user = request.query_params.get('customer_id', None)
        if user is not None:
            userId = User.objects.get(pk=user)
            orderId = Order.objects.get(customer_id=userId, status=True)
            product = Product.objects.filter(cart_products__order_id=orderId)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
   
    def create(self, request):
 
        seller_id = User.objects.get(pk=request.data["sellerId"])

        product = Product.objects.create(
            name=request.data["name"],
            image=request.data["image"],
            description=request.data["description"],
            condition=request.data["condition"],
            price=request.data["price"],
            color=request.data["color"],
            brand=request.data["brand"],
            seller_id=seller_id,
        )
        serializer = ProductSerializer(product)
        return Response(serializer.data)  
    
    def update(self, request, pk):

        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.image = request.data["image"]
        product.description=request.data["description"]
        product.condition=request.data["condition"],
        product.price=request.data["price"]
        product.color=request.data["color"]        
        product.brand=request.data["brand"]
        product.seller_id= User.objects.get(pk=request.data["sellerId"])
       

        product.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)   
    
    def destroy(self, request, pk):
        product = Product.objects.get(pk=pk)
        
        product.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
   
    # Custom action that adds a book to a customer
    @action(methods=['post'], detail=True)
    def addtocart(self, request, pk):
        """Add Product To Cart"""
        # Get the Customer instance using the customerId from the request data
        order = Order.objects.get(pk=request.data["orderId"])
        # Get the Book instance using the primary key (pk) parameter
        product = Product.objects.get(pk=pk)
            
        # Create a CustomerBook instance linking the customer and book
        Cart.objects.create(
            order_id=order,
            product_id=product
        )
        return Response({'message': 'Added to Cart'}, status=status.HTTP_201_CREATED)
    
    # Defines a custom action named addtocustomer within a viewset. The action is triggered by a POST request and adds a specific book to a specific customer. It first retrieves the customer and book instances based on the provided data, then creates a CustomerBook relationship between them.
    
    # Custom action that removes a book from a customer
    # @action(methods=['delete'], detail=True)
    # def removefromcart(self, request, pk):
    #     """Remove Book From Customer"""
    #     # Get the Customer instance using the customerId from the request data
    #     order_id = Order.objects.get(pk=request.data["orderId"])
    #     # Get the Book instance using the primary key (pk) parameter
    #     product_id = Product.objects.get(pk=pk)
            
    #     # Get the specific CustomerBook instance connecting the customer and book
    #     cart = Cart.objects.get(
    #         product_id=product_id.id,
    #         order_id=order_id.id
    #     )
        
    #     # Delete the CustomerBook instance            
    #     cart.delete()
        
        # Return a success response
        return Response({'message': 'Product removed from Cart'}, status=status.HTTP_204_NO_CONTENT)
  
    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for events
    """
    class Meta:
        model = Product
        fields = ('id' ,'name', 'image', 'description','seller_id', 'condition', 'price','brand','color')
        depth = 1
