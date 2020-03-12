from rest_framework import permissions #permissions module


class UpdateOwnProfile(permissions.BasePermission):
    """ALLOW USERS TO EDIT THEIR OWN PROFILE"""
    def has_object_permission(self,request, view, obj):
        """check user trying to edit their own profile and responds a boolean"""
        if request.method in permissions.SAFE_METHODS:#get is a safe method since it is only reading
            return True

        return obj.id == request.user.id #compare ID of the profile(obj) with user id


class UpdateOwnStatus(permissions.BasePermission):
    """ALLOW USERS TO UPDATE THEIR OWN STATUS"""
    def has_object_permission(self,request,view,obj):
        """check the user trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user_profile.id == request.user.id