from django.shortcuts import render
from rest_framework.views import APIView #import APIView class from rest framework
from rest_framework.response import Response #used to return response object from the APIView
from rest_framework import status #HTTP status codes used to return responses from API
from profiles_api import serializers, models, permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication #Authenticate user for the API
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
#Unauthenticated users can read only
#from rest_framework.permissions import IsAuthenticated
#above is to restrict all access to unauthenticated users

# Create your views here.

class HelloApiView(APIView):
    """TEST API VIEW"""
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
        """RETURNS LIST OF API VIEW FEATURES"""
        #it expects a function for different http request and get request to retreive list of objects or 
        # 1 object. Whenever http.get requests made to url assigned to this view it will call get function
        # and execute the logic in the get function
        an_apiview = [
            'Uses HTTP methods as functions - get, post, patch, delete, put',
            'Is similar to traditonal django view but intended for APIs',
            'gives you the most control over app logic',
            'mapped manually to urls'
        ]

        return Response({'message':'Hello','an_apiview': an_apiview}) #List or dictionary to be returned
        #it will convert to json - Whenever the url receives a get request, the response will be given


    def post(self, request):
        """CREATE HELLO MESSAGE WITH OUR NAME"""
        serializer = self.serializer_class(data=request.data)#data is passed as request.data in POST request

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors, 
                status = status.HTTP_400_BAD_REQUEST
                )
    
    def put(self,request,pk=None):
        """ HANDLE UPDATING AN OBJECT - PUT UPDATES ALL FIELDS BY REPLACING WITH VALUES PROVIDED"""
        #pk is to take id of the object we are updating with put request
        return Response({'method': 'PUT'})

    def patch(self,request,pk=None):
        """ HANDLE PARTIAL UPDATE AN OBJECT - ONLY UPDATE FIELDS PROVIDED IN REQUEST """
        return Response({'method':'PATCH'})

    def delete(self,request,pk=None):
        """ DELETE AN OBJECT """
        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """TEST API VIEWSETS"""
    
    serializer_class = serializers.HelloSerializer
    def list(self,request):
        """return hello message and it is a get request"""
        a_viewset = [
            'Uses actions - create, retreive,list, update, partial update, delete',
            'Automatically maps to urls using routers',
            'provides more functionality with less code',
            
        ]        

        return Response({'message':'Hello','a_viewset':a_viewset})

    def create(self,request):
        """CREATE A NEW HELLO MESSAGE"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message':message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retreive(self,request,pk=None):
        """RETREIVE A PARTICULAR OBJECT"""
        return Response({'http_method':'GET'})
    
    def update(self,request,pk=None):
        """UPDATING AN OBJECT"""
        return Response({'http_method':'PUT'})

    def partial_update(self,request,pk=None):
        """UPDATING AN OBJECT PARTIALLY"""
        return Response({'http_method':'PATCH'})    
    
    def destroy(self,request,pk=None):
        """REMOVING AN OBJECT"""
        return Response({'http_method':'DELETE'})        


class UserProfileViewSet(viewsets.ModelViewSet):
    """HANDLE CREATING AND UPDATING PROFILES"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all() #get all user profile objects in DB

    authentication_classes = (TokenAuthentication,)#Token authentication
    permission_classes = (permissions.UpdateOwnProfile,) #only those users who are authenticated get to update
    filter_backends = (filters.SearchFilter,) #Filtering the objects
    search_fields = ('name','email') #fields for searching

class UserLoginApiView(ObtainAuthToken):
    """HANDLE CREATING USER AUTHENTICATION TOKEN"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    
class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """HANDLES CRUD OF PROFILE FEED ITEMS"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all() #manage all profile feed items
    permission_classes = (
        permissions.UpdateOwnStatus, 
        IsAuthenticatedOrReadOnly
    )
    def perform_create(self, serializer):
        """Sets user profile to logged in user"""
        serializer.save(user_profile=self.request.user)
        #when new obj created, django accesses perform create
        #serializer is a model serializer and has save function to save contents to DB
        #here user_profile is validated with the user who is making the request
        #since we use token authentication, the request will have the authenticated user associated with 