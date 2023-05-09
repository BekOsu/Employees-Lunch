from django.urls import path
from .views import (
    RestaurantOwnerList,
    RestaurantOwnerDetail,
    RestaurantAPIView,
    RestaurantDetailView,
)

urlpatterns = [
    # restaurant-owners/
    path('owners/', RestaurantOwnerList.as_view(), name='owner_List'),
    path('owners/<int:pk>/', RestaurantOwnerDetail.as_view(), name='owner_detail'),
    # Restaurant
    path('ListCreate/', RestaurantAPIView.as_view(), name='restaurant_create'),
    path('detail/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant_detail'),
]
