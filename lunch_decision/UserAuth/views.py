from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer


# class UserListCreateView(ListCreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
