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
from .serializers import Job_categorySerializer, JobSerializer, CompanySerializer
# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(generics.ListAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer

    def get(self, request, *args, **kwargs):
        job_categories = Job_categorySerializer(self.get_queryset(), many=True).data
        return Response(job_categories)


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

# @api_view(['GET'])
# def application_index(request):
# #   applications = Application.objects.filter(user=request.user)
# # just 4 tesing 
#   applications = Application.objects.all()  
#   return Response({'applications' : applications})

@csrf_exempt
@api_view(['GET'])
def application_list(request):
    applications = Application.objects.filter(user_id=request.user)
    serialized_applications = [ApplicationSerializer(instance=app).data for app in applications]
    return Response({'success': True, 'applications': serialized_applications})
    
@csrf_exempt
@api_view(['GET'])
def get_user_info(request,user_id):
    user_info = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user_info)
    return JsonResponse( user_serializer.data)

@csrf_exempt
@api_view(['POST'])
def application_create(request , user_id , job_id):
    pass
    
    
    
    # ApplicationForm(request.POST, request.FILES) 
    # if form.is_valid():
    #     new_application = form.save(commit=False) 
    #     # get the job and user id from the url and add it as fk
    #     # add fk manually
    #     new_application.user_id = user_id
    #     new_application.job_id = job_id
    #     uploaded_file = request.FILES.get('resume')
    #     if uploaded_file:
    #         new_application.resume = uploaded_file
        
    #     new_application.save()
    #     serialized_application = ApplicationForm(instance=new_application).data
    #     # return JsonResponse()
    #     # return Response({'success': True, 'application': serialized_application})
    # else:
    #     return Response({'success': False, 'errors': form.errors})


class CompanyList(generics.ListAPIView):
  queryset = Company.objects.all()
  serializer_class = CompanySerializer
  model = Company

class CompanyDetail(DetailView):
    model = Company

class CompanyCreate(CreateView):
    model = Company
    fields = ['company_name', 'location', 'logo', 'email']
    
    def form_valid(self, form):
      form.instance.user = self.request.user
      # super() is calling the parent class
      return super().form_valid(form)

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

class SkillList(generics.ListAPIView):
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer
  model = Skill

class SkillDetail(DetailView):
    model = Skill

class SkillCreate(CreateView):
    model = Skill
    fields = ['skill_name']
    

class SkillUpdate(UpdateView):
    model = Skill
    fields = ['skill_name']

class SkillDelete(DeleteView):
    model = Skill
    
class CompanyDelete(DeleteView):
    model = Company
    success_url = '/company/'
    