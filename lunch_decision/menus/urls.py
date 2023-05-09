from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CurrentDayMenuView

router = DefaultRouter()
router.register(r'upload', views.MenuViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('current_day/', CurrentDayMenuView.as_view(), name='current_day_menu'),

]
