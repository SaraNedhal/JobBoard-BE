from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from .serializers import Job_categorySerializer , JobSerializer , CompanySerializer , SkillSerializer , ProfileSerializer , ApplicationSerializer
from .models import Skill, Profile, Company, Job_category, Job, Application
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import Job_categorySerializer, JobSerializer, CompanySerializer
# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(generics.ListAPIView):
    queryset = Job_category.objects.all()

    def get(self, request, *args, **kwargs):
        job_categories = Job_categorySerializer(self.get_queryset(), many=True).data
        return Response(job_categories)
 

class JobCategoryDetail(DetailView):
    model = Job_category

    def get(self, request, *args, **kwargs):
        job_category = Job_categorySerializer(self.get_queryset()).data
        return Response(job_category)


class JobCategoryCreate(generics.CreateAPIView):
    # model = Job_category
    serializer_class = Job_categorySerializer
    permission_class = [IsAuthenticated]
    
    # fields = ['category_name']
    def form_valid(self, form):
        instance = form.save(commit=False)
        job_category = self.serializer_class(instance)
        return Response(job_category)



class JobCategoryUpdate(UpdateView):
    # model = Job_category
    # fields = ['category_name']

    serializer_class = Job_categorySerializer
    permission_class = [IsAuthenticated]
    
    # fields = ['category_name']
    def form_valid(self, form):
        instance = form.save(commit=False)
        job_category = self.serializer_class(instance)
        return Response(job_category)



class JobCategoryDelete(DeleteView):
    model = Job_category
    permission_class = [AllowAny]

    # success_url = '/job_categories'
    def delete(self, request, *args, **kwargs):
        # self.check_object_permissions(self.request, self.get_object())
        response = super().delete(request, *args, **kwargs)
        return Response({'message': 'Job deleted successfully'})


# Job Views:

class JobList(generics.ListAPIView):
    queryset = Job.objects.all()

    def get(self, request, *args, **kwargs):
        job_list = JobSerializer(self.get_queryset(), many=True).data
        return Response(job_list)


class JobDetail(DetailView):
    model = Job

    def get(self, request, *args, **kwargs):
        job= JobSerializer(self.get_queryset()).data
        return Response(job)

class JobCreate(CreateView):
    serializer_class = JobSerializer
    permission_class = [IsAuthenticated]
    
    # fields = ['job_title', 'job_description', 'job_salary']

    def form_valid(self, form):
        instance = form.save(commit=False)
        job = self.serializer_class(instance)
        return Response(job)


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

    def get(self, request, *args, **kwargs):
        company_list = CompanySerializer(self.get_queryset(), many=True).data
        return Response(company_list)

class CompanyDetail(DetailView):
    model = Company

    def get(self, request, *args, **kwargs):
        company = CompanySerializer(self.get_queryset()).data
        return Response(company)

class CompanyCreate(CreateView):
    serializer_class = JobSerializer
    permission_class = [IsAuthenticated]
    
    # fields = ['company_name', 'location', 'logo', 'email']

    def form_valid(self, form):
        instance = form.save(commit=False)
        job = self.serializer_class(instance)
        return Response(job)

class CompanyUpdate(UpdateView):
    model = Company
    fields = ['company_name', 'location', 'logo', 'email']

class CompanyDelete(DeleteView):
    model = Company
    success_url = '/company/'
    
@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return Response({'success': True, 'message': 'Signup successful'})
        else:
            return Response({'success': False, 'message': 'Invalid sign up - try again'}, status=400)

    return Response({'success': False, 'message': 'Bad request'}, status=400)

