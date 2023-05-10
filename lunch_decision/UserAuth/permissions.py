from rest_framework import permissions
from restaurants.models import RestaurantOwner
from employee.models import Employee


class IsRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        print("user rest : ", request.user)

        if request.user.is_authenticated and RestaurantOwner.objects.filter(user=request.user).exists():
            return True
        return False


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        # print("user : ", request.user)

        if request.user.is_authenticated and Employee.objects.filter(user=request.user).exists():
            # print("user : ", request.user)
            return True
        return False
