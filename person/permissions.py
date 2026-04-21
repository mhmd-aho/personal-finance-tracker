from rest_framework import permissions
class IsOwnerProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
class IsProfileOwnerForObject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user