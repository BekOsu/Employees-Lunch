from .views import (
    EmployeeList,
    EmployeeDetail,
    VoteList,
    TodayTopMenus,
)
from django.urls import path

urlpatterns = [
    # employees
    path('account', EmployeeList.as_view(), name='employee_List'),
    path('account/<int:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
    # voting
    path('votes/', VoteList.as_view(), name='employees_votes'),
    path('api/today-top-menus/', TodayTopMenus.as_view(), name='today_top_menus'),

]
