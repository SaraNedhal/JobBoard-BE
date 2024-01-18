from django.shortcuts import render, redirect
from django.http import HttpResponse

from .serializers import Job_categorySerializer , JobSerializer , CompanySerializer , SkillSerializer , ProfileSerializer , ApplicationSerializer
from .models import Skill, Profile, Company, Job_category, Job, Application
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(generics.ListAPIView):
  queryset = Job_category.objects.all()
  serializer_class = Job_categorySerializer


class JobCategoryDetail(DetailView):
    model = Job_category


class JobCategoryCreate(generics.CreateAPIView):
    # model = Job_category
  serializer_class = Job_categorySerializer
  permission_class = [IsAuthenticated]
    
    # fields = ['category_name']


class JobCategoryUpdate(UpdateView):
    model = Job_category
    fields = ['category_name']


class JobCategoryDelete(DeleteView):
    model = Job_category
    success_url = '/job_categories'


# Job Views:

class JobList(generics.ListAPIView):
   queryset = Job.objects.all()
   serializer_class = JobSerializer
   model = Job


class JobDetail(DetailView):
    model = Job


class JobCreate(CreateView):
    model = Job
    fields = ['job_title', 'job_description', 'job_salary']


class JobUpdate(UpdateView):
    model = Job
    fields = ['job_title', 'job_description', 'job_salary']


class JobDelete(DeleteView):
    model = Job
    success_url = '/jobs'


def application_index(request):
  pass

def application_create(request):
  pass

class CompanyList(generics.ListAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  model = Company

class CompanyDetail(DetailView):
    model = Company

class CompanyCreate(CreateView):
    model = Company
    fields = ['company_name', 'location', 'logo', 'email']

class CompanyUpdate(UpdateView):
    model = Company
    fields = ['company_name', 'location', 'logo', 'email']

class CompanyDelete(DeleteView):
    model = Company
    success_url = '/company/'

class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@login_required
class ProfileCreate(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    
# @csrf_exempt
# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return Response({'success': True, 'message': 'Signup successful'})
#         else:
#             return Response({'success': False, 'message': 'Invalid sign up - try again'}, status=400)

#     return Response({'success': False, 'message': 'Bad request'}, status=400)


class RegistrationView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        role = request.data.get('role', 'J')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('phone_number')
        image = request.data.get('image')


        if not username or not password or not email or not role or not first_name or not last_name or not phone_number:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ('J', 'C'):
            role = 'J'
        # Create user
        user = User.objects.create_user(username=username, password=password,)
        Profile.objects.create(email=email, user=user, role=role, first_name=first_name, last_name=last_name, phone_number=phone_number, image=image)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, 'refresh_token': str(refresh) }, status=status.HTTP_201_CREATED)
