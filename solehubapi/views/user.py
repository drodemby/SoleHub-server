"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from solehubapi.models import User

class UserView(ViewSet):
    """SoleHub Users view"""
    
    def list(self, request):
        """Handle GET requests to get all users
        Returns:
            Response -- JSON serialized list of users
        """
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
      
    def retrieve(self, request, pk):
      try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
      except User.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
          
    def update(self, request, pk):
        user = User.objects.get(pk=pk)
        user.first_name = request.data["first_name"]
        user.last_name = request.data["last_name"]
        user.address = request.data["address"]
        user.email = request.data["email"]
        user.shoe_size = request.data["shoe_size"]
        user.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for users
    """
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'address', 'email', 'shoe_size', 'uid')
