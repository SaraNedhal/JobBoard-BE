from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .serializers import Job_categorySerializer , JobSerializer , CompanySerializer , SkillSerializer , ProfileSerializer , ApplicationSerializer , UserSerializer

from .models import Skill, Profile, Company, Job_category, Job, Application, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny, AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist 

# Create your views here.

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(generics.ListAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer

    # def get(self, request, *args, **kwargs):
    #     job_categories = Job_categorySerializer(self.get_queryset(), many=True).data
    #     return Response(job_categories)
 

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
    serializer_class = JobSerializer

    # def get(self, request, *args, **kwargs):
    #     job_list = JobSerializer(self.get_queryset(), many=True).data
    #     return Response(job_list)


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

# @api_view(['GET'])
# def application_index(request):
# #   applications = Application.objects.filter(user=request.user)
# # just 4 tesing 
#   applications = Application.objects.all()  
#   return Response({'applications' : applications})

@csrf_exempt
@api_view(['GET'])
def application_list(request):
    applications = Application.objects.filter(user_id=request.user.id)
    # serialized_applications = [ApplicationSerializer(instance=app).data for app in applications]
    application_serializer = ApplicationSerializer(applications, many=True)
    # return JsonResponse(application_serializer.data , safe=False)
    serialized_data = application_serializer.data
    return JsonResponse({'applications': serialized_data})
@csrf_exempt
@api_view(['GET'])
def get_user_info(request,user_id):
    user_info = User.objects.get(id=user_id)
    user_serializer = UserSerializer(user_info)
    profile_info = Profile.objects.get(user = user_info)
    # profile_info = get_object_or_404(Profile, user=user_info)
    profile_serializer = ProfileSerializer(profile_info)
    response_data = {
        "user_info": user_serializer.data,
        "profile_info": profile_serializer.data
    }
    return JsonResponse(response_data)

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def application_create(request , user_id , job_id):
    user_id = request.user.id
    print("user_id",request.user.id)
    if 'resume' in request.FILES:
        resume_file = request.FILES['resume']
    if not resume_file.name.endswith('.pdf'):
        return JsonResponse({"error": "Only PDF format is accepted"})   
    
    application_data = {
            'user': user_id,
            'job': job_id,
            'resume': resume_file
        }
    
    application_serializer = ApplicationSerializer(data=application_data)
    if application_serializer.is_valid():
            # Save the application to the database
            application_serializer.save()

            # Retrieve the serialized data of the created application
            serialized_application = ApplicationSerializer(application_serializer.instance).data

            return JsonResponse({
                "message": "Application created successfully",
                "application": serialized_application
            })
    else:
            return JsonResponse({"error": application_serializer.errors})
  
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def application_update(request):
    application_id = request.GET.get('application_id')
    application_info = Application.objects.get(id=application_id)
    # making sure that the user who created the application is the one who's updating the application
    if  request.user.id != application_info.user_id:
        JsonResponse({"error" : "You are not authorized to update this application"})
    if 'resume' in request.FILES:
        resume_file = request.FILES['resume']
    if not resume_file.name.endswith('.pdf'):
        return JsonResponse({"error": "Only PDF format is accepted"})  
        
    print("Before assigning user:", application_info.user)
    print("Before assigning job:", application_info.job)
    application_info.resume = resume_file
    application_info.user = request.user
    print('user id in update application' , request.user)
    application_info.job= application_info.job
    print('job id in update application' ,  application_info.job)

    
    application_serializer = ApplicationSerializer(instance=application_info, data=request.data , context={'instance':application_info})
    if application_serializer.is_valid():
        application_serializer.save()

        # Retrieve the serialized data of the updated application
        serialized_application = ApplicationSerializer(application_info).data

        return JsonResponse({
            "message": "Application updated successfully",
            "application": serialized_application
        })
    else:
        return JsonResponse({"error": application_serializer.errors})

@csrf_exempt
@api_view(['GET'])  
def application_delete(request):
    application_id = request.GET.get('application_id')
    print('application_id =' , application_id )
    try:
        application_info = Application.objects.get(id=application_id)
        print('applicatoin_info' , application_info)
        application_info.delete()
        response_data = {'success': True, 'message': ' Your application deleted successfully'}
    except ObjectDoesNotExist as e:
        print(f'Application.DoesNotExist: {str(e)}')
        response_data = {'success': False, 'message': 'Application not found'}
    return JsonResponse(response_data)


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

    # def get(self, request, *args, **kwargs):
    #     company_list = CompanySerializer(self.get_queryset(), many=True).data
    #     return Response(company_list)

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
    
    # def form_valid(self, form):
    #   form.instance.user = self.request.user
    #   # super() is calling the parent class
    #   return super().form_valid(form)

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

class ProfileUpdate(UpdateView):
    models = Profile
    fields = ['user.username', 'first_name', 'last_name', 'role', 'image', 'phone_number', 'skills']

class ProfileDelete(DeleteView):
    models = Profile
    
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


        if not username or not password or not email or not first_name or not last_name or not phone_number:
            return Response({'error': 'username, password, email, frist name, last name, and phone number are required'}, status=status.HTTP_400_BAD_REQUEST)
        if role not in ('J', 'C'):
            role = 'J'
        # Create user
        user = User.objects.create_user(username=username, password=password,)
        Profile.objects.create(email=email, user=user, role=role, first_name=first_name, last_name=last_name, phone_number=phone_number, image=image)

        login(request, user)

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({'access_token': access_token, 'refresh_token': str(refresh) }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user
            login(request, user)

            # Generate new tokens
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token, 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Log out the user
        logout(request)

        return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)

class SkillList(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    # def get(self, request, *args, **kwargs):
    #     skills = SkillSerializer(self.get_queryset(), many=True).data
    #     return Response(skills)

class SkillDetail(DetailView):
    model = Skill

class SkillCreate(generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    # model = Skill
    # fields = ['skill_name']
    

class SkillUpdate(generics.UpdateAPIView):
    # model = Skill
    # fields = ['skill_name']
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class SkillDelete(generics.DestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
class CompanyDelete(DeleteView):
    model = Company
    success_url = '/company/'
    
