from rest_framework import serializers
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our API view"""
    #Function very similar to django form - define serializer and specify fields
    name = serializers.CharField(max_length=20) #accepts character input


class UserProfileSerializer(serializers.ModelSerializer):
    """WORK WITH EXISTING DJANGO DB MODEL - serialize a user profile object"""
    class Meta: 
        model = models.UserProfile
        #Connects to User Profile model
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {'write_only': True,
                        'style':{'input_type':'password'}}
        }

    def create(self,validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes Profile feed item"""

    class Meta:
        model = models.ProfileFeedItem

        fields = ( 'id','user_profile', 'status_text', 'created_on')#id created by default and is read only
        extra_kwargs = {
            'user_profile': {'read_only': True}
        }