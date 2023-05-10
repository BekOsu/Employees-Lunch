from rest_framework import generics
from .models import RestaurantOwner, Restaurant
from .serializers import RestaurantSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RestaurantOwnerSerializer
from UserAuth.permissions import IsRestaurantOwner


class RestaurantOwnerList(generics.ListCreateAPIView):
    serializer_class = RestaurantOwnerSerializer
    queryset = RestaurantOwner.objects.all()


class RestaurantOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer


class RestaurantAPIView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]
    # permission_classes = [IsAuthenticated, IsRestaurantOwner] # if we want to use jwt

    def get_queryset(self):
        if self.request.user.is_authenticated:
            owner = self.request.user.restaurantowner
            return Restaurant.objects.filter(owner=self.request.user.restaurantowner)
        else:
            return Restaurant.objects.none()

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            owner = self.request.user.restaurantowner
            serializer.save(owner=self.request.user.restaurantowner)
        else:
            return Restaurant.objects.none()


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]
    # permission_classes = [IsAuthenticated, IsRestaurantOwner]  # if we want to use jwt
    queryset = Restaurant.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            owner = self.request.user.restaurantowner
            return Restaurant.objects.filter(owner=owner)
        else:
            return Restaurant.objects.none()
