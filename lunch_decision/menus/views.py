from rest_framework.permissions import IsAuthenticated
from .filters import MenuFilter
from .models import Menu, MenuItem
from .serializers import MenuSerializer, MenuItemSerializer
from datetime import date
from rest_framework import generics, viewsets
from UserAuth.permissions import IsRestaurantOwner
from UserAuth.permissions import IsEmployee


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsRestaurantOwner]
    filterset_class = MenuFilter


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsRestaurantOwner]


class CurrentDayMenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    permission_classes = [IsEmployee]

    def get_queryset(self):
        if IsEmployee().has_permission(self.request, self):
            today_menus = Menu.objects.filter(date=date.today())
            return today_menus
        return Menu.objects.none()
