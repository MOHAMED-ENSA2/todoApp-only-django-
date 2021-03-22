from django.urls import path 

from .views import TaskList,Detail, Create, Update, Delete,Register, Login
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path("" , TaskList.as_view() , name = 'tasks'),
    path("<int:pk>/" , Detail.as_view() , name = 'task'),
    path("create-task/" , Create.as_view() , name = 'create' ),
    path("updte-task/<int:pk>/" , Update.as_view() , name = 'update' ),
    path("delete-task/<int:pk>/" , Delete.as_view() , name = 'delete' ),
    path("login/" , Login.as_view() , name = "login"),
    path("register/" , Register.as_view() , name = "register"),
    path("logout/" , LogoutView.as_view(next_page = "tasks") , name = "logout"),


]

