from rest_framework import permissions

class IsAnonCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated:
            return True
        elif request.method == "PATCH" and request.user.is_authenticated:
            return True
        elif request.method == "DELETE" and request.user.is_authenticated:
            return True
        elif request.method != "POST" and not request.user.is_authenticated:
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.email == request.user.email or request.user.is_admin

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user or request.user.is_admin

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_admin
