# TODO здесь производится настройка пермишенов для нашего проекта
from rest_framework.permissions import BasePermission

class IsAuthorOrSuper(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.author == request.user