from rest_framework import generics, status
from .models import Vote, Employee
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import EmployeeSerializer, VoteSerializer
from rest_framework.response import Response
from datetime import date
from UserAuth.permissions import IsEmployee
from menus.models import Menu
from django.db.models import Sum
from drf_yasg.utils import swagger_auto_schema
from menus.serializers import MenuSerializer
from drf_yasg import openapi


class EmployeeList(generics.ListCreateAPIView):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()


class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class VoteList(generics.CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsEmployee]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='X-API-Version',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description="API version, e.g., 'v1' or 'v2'",
        )
    ])
    def post(self, request, *args, **kwargs):
        version = request.META.get('HTTP_X_API_VERSION', "v1")

        if version == "v1":
            return self.create_vote_v1(request)
        elif version == "v2":
            return self.create_vote_v2(request)
        else:
            return Response("Invalid API version", status=status.HTTP_400_BAD_REQUEST)

    def create_vote_v1(self, request):
        data = request.data
        if isinstance(data, list):
            return Response("Multiple menu selections are not allowed in API v1", status=status.HTTP_400_BAD_REQUEST)
        menu_id = request.data.get('menu')

        if menu_id is None:
            return Response("Please select one restaurant", status=status.HTTP_400_BAD_REQUEST)

        menu = Menu.objects.filter(id=menu_id).first()

        if not menu:
            return Response("Invalid menu selection", status=status.HTTP_400_BAD_REQUEST)

        employee = request.user.employee
        today = date.today()
        vote = Vote.objects.filter(employee=employee, created_at__date=today, menu=menu).first()
        if vote:
            return Response("You have already voted for this menu today", status=status.HTTP_400_BAD_REQUEST)

        vote, created = Vote.objects.update_or_create(
            employee=employee, created_at__date=date.today(), points=3,
            defaults={'menu': menu}
        )
        queryset = Vote.objects.filter(employee=employee, created_at__date=date.today())
        serializer = self.get_serializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_vote_v2(self, request):
        selected_menus = request.data

        # Validate request data format
        if not isinstance(selected_menus, list) or len(selected_menus) != 3:
            return Response("Request data must be a list of three dictionaries, each with a 'menu' key",
                            status=status.HTTP_400_BAD_REQUEST)

        employee = request.user.employee
        points = [3, 2, 1]

        for index, selection in enumerate(selected_menus):
            menu_id = selection.get('menu')
            menu = Menu.objects.filter(id=menu_id).first()

            if not menu:
                return Response(f"Invalid selection for restaurant {index + 1}", status=status.HTTP_400_BAD_REQUEST)
            vote, created = Vote.objects.update_or_create(
                employee=employee, created_at__date=date.today(), menu=menu,
                defaults={'points': points[index]}
            )

        queryset = Vote.objects.filter(employee=employee, created_at__date=date.today())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TodayTopMenus(generics.ListAPIView):
    permission_classes = [IsEmployee]
    serializer_class = MenuSerializer

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='X-API-Version',
            in_=openapi.IN_HEADER,
            type=openapi.TYPE_STRING,
            required=True,
            description="API version, e.g., 'v1' or 'v2'",
        )
    ])
    def get(self, request, *args, **kwargs):
        version = request.META.get('HTTP_X_API_VERSION', "v1")

        if version == "v1":
            return self.get_top_menu_v1(request)
        elif version == "v2":
            return self.get_top_menus_v2(request)
        else:
            return Response("Invalid API version", status=status.HTTP_400_BAD_REQUEST)

    def get_top_menu_v1(self, request):
        today_votes = Vote.objects.filter(created_at__date=date.today())
        top_menu = today_votes.annotate(total_points=Sum('points')).order_by('-total_points').first()
        if top_menu:
            serializer = self.get_serializer(top_menu.menu)
            return Response(serializer.data)
        else:
            return Response("No votes for the day yet", status=status.HTTP_404_NOT_FOUND)

    def get_top_menus_v2(self, request):
        today_votes = Vote.objects.filter(created_at__date=date.today())
        top_menus = today_votes.values('menu').annotate(total_points=Sum('points')).order_by('-total_points')[:3]
        top_menu_ids = [menu['menu'] for menu in top_menus]
        queryset = Menu.objects.filter(id__in=top_menu_ids)
        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("No votes for the day yet", status=status.HTTP_404_NOT_FOUND)
