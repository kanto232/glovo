from rest_framework.permissions import BasePermission


class CheckRole(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        return False

class CourierRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'courier'


