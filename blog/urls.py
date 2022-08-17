from django.urls import path
from blog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_student/',views.get_student,name='get_student'),
    path('get_student_details/',views.get_student_details,name='student_details'),
    path('list_details/',views.list_details,name='list_details'),
    path('signin/',views.signin,name='signin'),
    path('register/',views.register,name='register'),
    path('user_logout/',views.user_logout,name='user_logout'),
    
]
