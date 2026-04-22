from rest_framework import permissions
class IsOwnerProfile(permissions.BasePermission):
    message  = 'You do not have permission to access this profile.'
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
class IsProfileOwnerForObject(permissions.BasePermission):
    message  = 'You are not the owner of this data.'
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user
