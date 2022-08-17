from django.shortcuts import render
from .serializer import StudentDetailSerializer,PersonSerializer,PersonDetailSerializer,UserSerializer,RegisterSerializer
from .models import ProgressModel,StudentDetailModel
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import authentication_classes,permission_classes

from rest_framework.views import APIView
from rest_framework import authentication, permissions
from django.contrib.auth.models import User

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from knox.models import AuthToken
from django.contrib.auth import login,logout
from rest_framework import permissions,status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.signals import user_logged_out


# Create your views here.
# class add_student_field(generics.ListCreateAPIView):
#     queryset=ProgressModel.objects.all()
#     serializer_class=ProgressSerializer
#     pagination_class=PageNumberPagination

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
class add_details_field(generics.ListCreateAPIView):
    queryset=ProgressModel.objects.all()
    serializer_class=StudentDetailSerializer
    
# for crud
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
# @permission_classes([AllowAny])
class add_person(generics.ListCreateAPIView):
    queryset=ProgressModel.objects.all()
    serializer_class=PersonSerializer

@permission_classes([AllowAny])
class add_person_details(generics.ListCreateAPIView):
    queryset=StudentDetailModel.objects.all()
    serializer_class=PersonDetailSerializer

# ---------APIView

# class ListUsers(APIView):
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request, format=None):
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)

# -----------ObtainAuthToken

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
        })


# Create user login
@permission_classes([AllowAny])
class RegisterAPI(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class = RegisterSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors)
        
        
        # Response({
        # "user": UserSerializer(user, context=self.get_serializer_context()).data,
        # "token": AuthToken.objects.create(user)[1]
        # })



class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        request._auth.delete()
        user_logged_out.send(sender=request.user.__class__,
                             request=request, user=request.user)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

