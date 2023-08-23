from solehubapi.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def check_user(request):
    '''Checks to see if User has an Account

    Method arguments:
      request -- The full HTTP request object
    '''
    uid = request.data['uid']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    user = User.objects.filter(uid=uid).first()

    # If authentication was successful, respond with their token
    if user is not None:
        data = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'email':user.email,
            'shoes_size': user.shoe_size,
            'uid': user.uid
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)
      
@api_view(['POST'])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    user = User.objects.create(
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        address=request.data['address'],
        email=request.data['email'],
        shoe_size=request.data['shoe_size'],
        uid=request.data['uid']
    )

    data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'address': user.address,
        'email':user.email,
        'shoe_size':user.shoe_size,
        'uid': user.uid,
    }
    return Response(data)
