from django.shortcuts import render,redirect
from django.core.paginator import Paginator
import requests
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import logout
import json
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    print('------------Refresh-------')
    url="http://127.0.0.1:8000/api/person_details/"
    response=requests.get(url).json()
    return render(request,'student.html',{'response':response})

def get_student(request):
    if request.method=='POST':
        print('------------Create branch-------')
        name=request.POST['txtFullname']
        father_name=request.POST['selectFatherName']
        student_class=request.POST['selectGrade']
        marks=request.POST['txtMarks']
        data={
            'name':name,
            'father_name':father_name,
            'student_class':student_class,
            'marks':marks,
        }
        print(data)
        url="http://127.0.0.1:8000/api/person/"
        response=requests.post(url,data=data)
        print(response.text)
        if response.status_code==400:
            messages.error(request,('Student name already exists'))
            url="http://127.0.0.1:8000/api/person_details/"
            response=requests.get(url).json()
            return render(request,'student.html',{'response':response})
        else:
            messages.success(request,("Student entered successfully"))
            return redirect('list_details')
    print('------------Student Refresh-------')
    url="http://127.0.0.1:8000/api/person_details/"
    response=requests.get(url).json()
    return render(request,'student.html',{'response':response})

def get_student_details(request):
    if request.method=='POST':
        print('------------Create branch-------')
        father_name=request.POST['txtFatherName']
        occupation=request.POST['txtOccupation']
        address=request.POST['txtAddress']
        data={
            'father_name':father_name,
            'occupation':occupation,
            'address':address,
        }
        url="http://127.0.0.1:8000/api/person_details/"
        response=requests.post(url,data=data)
        messages.success(request,("Student entered successfully"))
        return redirect('get_student')
    print('------------Details Refresh-------')
    url="http://127.0.0.1:8000/api/person_details/"
    response=requests.get(url).json()
    return render(request,'student_details.html',{'response':response})
    # url="http://127.0.0.1:8000/api/person/"
    # response=requests.get(url).json()
    # print("------------Branch Refresh-----------")
    # return render(request,'list_details.html',{'response':response})

@login_required(login_url='/blog/signin/')
def list_details(request):
    print('------------List details-------')
    get_token = request.session.get('get_token')
    # creating header format to access api link with token
    headers={"content-type": "application/json;", 'Authorization': 'Token {token_get}'.format(token_get=get_token)}
    print(headers)
    url="http://127.0.0.1:8000/api/student_details/"
    response=requests.get(url,headers=headers).json()
    p=Paginator(response,3)
    page=request.GET.get('page')
    venues=p.get_page(page)
    return render(request,'list_details.html',{'venues':venues})

# login and register
def signin(request):
    if request.method=='POST':
        print('------------Signin branch-------')
        name=request.POST['txtName']
        password=request.POST['pwdPassword']
        data={
            'username':name,
            'password':password,
        }
        print(data)
        url="http://127.0.0.1:8000/api/login/"
        response=requests.post(url,data=data)
        print(response)
        print(response.text)
        if response.status_code==200:
            messages.success(request,('Logged in successful'))
            print(response.text)
            dict=json.loads(response.text)
            Token=(dict["token"])
            print(Token)
            # for getting session variable:
            request.session['get_token'] = Token
            # for setting session variable:
            # get_token = request.session.get('get_token')

            return redirect('get_student')
        else:
            messages.error(request,("Wrong credentials. Try Again"))
            return render(request,'signup/signin.html')
    else:
        return render(request,'signup/signin.html')

def register(request):
    if request.method=='POST':
        print('------------Create User-------')
        name=request.POST['txtName']
        email=request.POST['emailEmail']
        password=request.POST['pwdPassword']
        password2=request.POST['pwdPassword2']
        if password == password2:
            data={
                'username':name,
                'email':email,
                'password':password,
            }
            print(data)
            url="http://127.0.0.1:8000/api/register/"
            response=requests.post(url,data=data)
            print(response)
            # msg=response.json()
            # print(msg)
            if response.status_code==201:
                messages.success(request,('User successfully created'))
                return redirect('signin')
            else:
                messages.error(request,("Username already found. Try different name!!!"))
                return render(request,'signup/register.html')
        else:
            messages.error(request,'Password mismatches with confirm password')
    return render(request,'signup/register.html')

def user_logout(request):
    logout(request)
    return redirect('signin')



    
