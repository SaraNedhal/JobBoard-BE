from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Skill, Profile, Company, Job_category, Job, Application
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(ListView):
    model = Job_category


class JobCategoryDetail(DetailView):
    model = Job_category


class JobCategoryCreate(CreateView):
    model = Job_category
    fields = ['category_name']


class JobCategoryUpdate(UpdateView):
    model = Job_category
    fields = ['category_name']


class JobCategoryDelete(DeleteView):
    model = Job_category
    success_url = '/job_categories'


# Job Views:

class JobList(ListView):
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

class CompanyList(ListView):
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
