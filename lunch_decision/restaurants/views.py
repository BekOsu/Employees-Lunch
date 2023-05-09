from rest_framework import generics
from .models import RestaurantOwner, Restaurant
from .serializers import RestaurantSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RestaurantOwnerSerializer
from UserAuth.permissions import IsRestaurantOwner


class RestaurantOwnerList(generics.ListCreateAPIView):
    serializer_class = RestaurantOwnerSerializer
    queryset = RestaurantOwner.objects.all()
    permission_classes = [AllowAny]


class RestaurantOwnerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer


class RestaurantAPIView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsRestaurantOwner]

    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user.restaurantowner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.restaurantowner)


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [IsAuthenticated, IsRestaurantOwner]
    queryset = Restaurant.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            owner = self.request.user.restaurantowner
            return Restaurant.objects.filter(owner=owner)
        else:
            return Restaurant.objects.none()




