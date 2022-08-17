from django.core.exceptions import ValidationError
from .models import ProgressModel,StudentDetailModel
from rest_framework import serializers
from django.contrib.auth.models import User

# class ProgressSerializer(serializers.ModelSerializer):
#     result=serializers.SerializerMethodField('get_result')
#     # details=serializers.SerializerMethodField('get_details')
#     class Meta:
#         model=ProgressModel
#         fields=['name','student_class','marks','result']

#     def get_result(self,obj):
#         if obj.marks >= 35:
#             return {
#                 'result':"Pass"
#             }
#         else:
#             return {
#                 'result':"Fail"
#                 }

    # def get_details(self,obj):
    #     return{
    #         'Father name':obj.father_name
    #     }

# class StudentDetailSerializer(serializers.ModelSerializer):
#     details=ProgressSerializer(read_only=True,many=True)
#     class Meta:
#         model=StudentDetailModel
#         fields=['father_name','occupation','address']

class StudentDetailSerializer(serializers.ModelSerializer):
    details=serializers.SerializerMethodField('get_details')
    # results=serializers.SerializerMethodField('get_results')
    class Meta:
        model=ProgressModel
        fields=['id','name','father_name', 'details','student_class','marks']

    # def get_results(self,obj):
    #     if obj.marks >=35:
    #         return{
    #         'Results': 'Pass'
    #         }
    #     else:
    #         return{
    #             'Results': 'Fail'
    #         }

    def get_details(self,obj):
        father_name=StudentDetailModel.objects.filter(father_name=obj.father_name).values()
        return father_name

    def validate_name(self,value):
        name2=value
        user_qs=ProgressModel.objects.filter(name=name2)
        if user_qs.exists():
            raise ValidationError('Student name already exists')
        return value

# for crud
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProgressModel
        fields=['id','name','student_class','marks', 'father_name']

    def validate_name(self,value):
        name2=value
        user_qs=ProgressModel.objects.filter(name=name2)
        if user_qs.exists():
            raise ValidationError('Student name already exists')
        return value

class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentDetailModel
        fields=['id', 'father_name','occupation','address']

# ----User login
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email','password')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

    