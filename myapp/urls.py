from django.urls import path
from myapp import views
from knox import views as knox_views
from knox.views import LoginView

urlpatterns = [
    # path('', views.add_student_field.as_view()),
    path('student_details/',views.add_details_field.as_view()),
    path('person/',views.add_person.as_view()),
    path('person_details/',views.add_person_details.as_view()),
    # path('users/',views.ListUsers.as_view()),
    path('login/', views.CustomAuthToken.as_view()),
    path('register/', views.RegisterAPI.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
]
