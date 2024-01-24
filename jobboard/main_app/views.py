from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse

from .serializers import Job_categorySerializer, JobSerializer, CompanySerializer, SkillSerializer, ProfileSerializer, ApplicationSerializer, UserSerializer, UpdateProfileSerializer

from .models import Skill, Profile, Company, Job_category, Job, Application, User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny, AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework import permissions
from rest_framework import status
from rest_framework import generics
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist 

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.decorators import permission_required
from .decorator import allowed_users
# Create your views here.
from django.utils.decorators import method_decorator

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

# Job-Category views:

class JobCategoryList(LoginRequiredMixin,generics.ListAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer


class JobCategoryDetail(LoginRequiredMixin,generics.RetrieveAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "message": "job category details retrieved successfully",
            "job_category": serializer.data
        }
        return JsonResponse(response_data)

 

# class JobCategoryDetail(LoginRequiredMixin,generics.RetrieveAPIView):
#     queryset = Job_category.objects.all()
#     serializer_class = Job_categorySerializer
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         response_data = {
#             "message": "job category details retrieved successfully",
#             "job_category": serializer.data
#         }
#         return JsonResponse(response_data)

    # def get(self, request, *args, **kwargs):
    #     job_category = Job_categorySerializer(self.get_queryset()).data
    #     return Response(job_category)


@method_decorator(allowed_users(['A,CA']), name='dispatch')
class JobCategoryCreate(LoginRequiredMixin,generics.CreateAPIView):
    # model = Job_category
    serializer_class = Job_categorySerializer
    permission_class = [IsAuthenticated]
    
    # fields = ['category_name']
    def form_valid(self, form):
        instance = form.save(commit=False)
        job_category = self.serializer_class(instance)
        return Response(job_category)



@method_decorator(allowed_users(['A,CA']), name='dispatch')
class JobCategoryUpdate(LoginRequiredMixin,generics.UpdateAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer
    



@method_decorator(allowed_users(['A,CA']), name='dispatch')
class JobCategoryDelete(LoginRequiredMixin,generics.DestroyAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categorySerializer


# Job Views:

class JobList(LoginRequiredMixin,generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer




class JobDetail(LoginRequiredMixin,generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "message": "job details retrieved successfully",
            "job": serializer.data
        }
        return JsonResponse(response_data)



# @parser_classes([JSONParser])

@allowed_users(['A,CA'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def job_create(request):
    try:
        user_id = request.user.id
        print('user_id ' , user_id)
        job_category = request.GET.get('category_id')
        company_id = request.GET.get('company_id')
        job_title = request.data['job_title']
        job_description = request.data['job_description']
        job_salary = request.data['job_salary']
        skills= request.data.get('skills')
        
        job = Job.objects.create(
            user_id = user_id,
            job_title = job_title,
            job_description = job_description,
            job_salary = job_salary,
            job_category_id = job_category,
            company_id = company_id
        )
        # skills has a many to many relation with the job so the skills will be added to the job
        job.skills.set(skills)
        
        serilaized_job_data = JobSerializer(job) 
        return JsonResponse(serilaized_job_data.data)
    except Exception as e:
        return JsonResponse({'message': str(e)})

       
@allowed_users(['A,CA'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def job_update(request):
    job_id = request.GET.get('job_id')
    job_category = request.GET.get('category_id')
    job_info = Job.objects.get(id=job_id)
    if 'job_title' in request.data:
        job_info.job_title = request.data.get('job_title')
    if 'job_description' in request.data:
        job_info.job_description = request.data.get('job_description')
    if 'job_salary' in request.data:
        job_info.job_salary = request.data.get('job_salary')
    if 'skills' in request.data:
        skills = request.data.get('skills')   
        job_info.skills.set(skills)  
    job_info.job_category_id = job_category
    serialized_data = JobSerializer(instance=job_info, data=request.data , partial=True , context={'instance':job_info})
    # if the serlized version of the updated job has valid inputs
    if serialized_data.is_valid():
        # store it in the database
        serialized_data.save()
        
        updated_serialized_job = JobSerializer(job_info).data
        
        return JsonResponse({
             "message": "Job updated successfully",
                "job":updated_serialized_job
        })
    else:
        return JsonResponse({"error": updated_serialized_job.errors})
   
        
@method_decorator(allowed_users(['A','CA']), name='dispatch')
class JobDelete(LoginRequiredMixin,generics.DestroyAPIView):
    serializer_class = JobSerializer
    queryset = Job.objects.all()


@allowed_users(['A','J'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def application_list(request):
    applications = Application.objects.filter(user_id=request.user.id)
    # serialized_applications = [ApplicationSerializer(instance=app).data for app in applications]
    application_serializer = ApplicationSerializer(applications, many=True)
    # return JsonResponse(application_serializer.data , safe=False)
    serialized_data = application_serializer.data
    return JsonResponse({'applications': serialized_data})


@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
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

@allowed_users(['A','J'])
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
 
@allowed_users(['A','J']) 
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

    
    application_serializer = ApplicationSerializer(instance=application_info, data=request.data , partial=True, context={'instance':application_info})
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


@allowed_users(['A','J'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
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

@allowed_users(['A','CA'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])  
@api_view(['POST'])  
def assoc_job(request):
    job_id = request.GET.get('job_id')
    print('job_id', job_id)
    skill_id=request.GET.get('skill_id')
    print('skill_id', skill_id)
    try:
        job = Job.objects.get(id=job_id)
        skill = Skill.objects.get(id=skill_id)
        print('skill', skill )

            # Add the skill to the job's skills
        job.skills.add(skill)
        print('job', job)
        print('added job to skill' , job.skills.add(skill))
        job_serializer = JobSerializer(job)
        return JsonResponse({
            'message': "The skill has been added successfully from the job",
            'job': job_serializer.data
        })    
    except Job.DoesNotExist:
        return JsonResponse({'message': 'Job not found'})

    except Skill.DoesNotExist:
        return JsonResponse({'message': 'Skill not found'})

    except Exception as e:
        return JsonResponse({'message': str(e)})
 
 
@allowed_users(['A','CA'])   
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])  
@api_view(['POST'])  
def unassoc_job(request):
    job_id = request.GET.get('job_id')
    print('job_id', job_id)
    skill_id=request.GET.get('skill_id')
    print('skill_id', skill_id)
    try:
        job = Job.objects.get(id=job_id)
        skill = Skill.objects.get(id=skill_id)
        print('skill', skill )

            # Add the skill to the job's skills
        job.skills.remove(skill)
        print('job', job)
        job_serializer = JobSerializer(job)
        return JsonResponse({
            'message': "The skill has been removed successfully from the job ",
            'job': job_serializer.data
        })  
    except Job.DoesNotExist:
        return JsonResponse({'message': 'Job not found'})

    except Skill.DoesNotExist:
        return JsonResponse({'message': 'Skill not found'})

    except Exception as e:
        return JsonResponse({'message': str(e)})


@allowed_users(['A','CA'])
@csrf_exempt
@api_view(['POST'])    
@permission_classes([permissions.IsAuthenticated])  
def assoc_profile(request):
    user_id = request.user.id
    print('user_id', user_id)
    skill_id = request.GET.get('skill_id')
    print('skill_id', skill_id)
    try:
        profile = Profile.objects.get(user_id=user_id)
        print('profile_info', profile)
        # skill = Skill.objects.get(id=skill_id)
        profile.skills.add(skill_id)
        profile_serializer = ProfileSerializer(profile)
        return JsonResponse({
            'message': "The skill has been removed successfully from the User Profile",
            'profile': profile_serializer.data
        })      
    except Profile.DoesNotExist:
        return JsonResponse({'message' : "profile does not exist"})
    except Skill.DoesNotExist:
        return JsonResponse({'message' : "skill does not exist"})
    except Exception as e:
        return JsonResponse({'message': str(e)})


@allowed_users(['A','CA'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])  
@api_view(['POST']) 
def unassoc_profile(request):
    user_id = request.user.id
    print('user_id', user_id)
    skill_id = request.GET.get('skill_id')
    print('skill_id', skill_id)
    try:
        profile = Profile.objects.get(user_id=user_id)
        print('profile_info', profile)
        # skill = Skill.objects.get(id=skill_id)
        profile.skills.remove(skill_id)
        profile_serializer = ProfileSerializer(profile)
        return JsonResponse({
            'message': "The skill has been removed successfully from the User Profile",
            'profile': profile_serializer.data
        }) 
    except Profile.DoesNotExist:
        return JsonResponse({'message' : "profile does not exist"})
    except Skill.DoesNotExist:
        return JsonResponse({'message' : "skill does not exist"})
    except Exception as e:
        return JsonResponse({'message': str(e)})
        


class CompanyList(LoginRequiredMixin,generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # def get(self, request, *args, **kwargs):
    #     company_list = CompanySerializer(self.get_queryset(), many=True).data
    #     return Response(company_list)

# class CompanyDetail(DetailView):
#     model = Company

#     def get(self, request, *args, **kwargs):
#         company = CompanySerializer(self.get_queryset()).data
#         return Response(company)
    
class CompanyDetail(LoginRequiredMixin,generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "message": "Company details retrieved successfully",
            "company": serializer.data
        }
        return JsonResponse(response_data)

@allowed_users(['A','CA'])
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def company_create(request):
    try:
        user_id = request.user.id
        company_name = request.data['company_name']
        location = request.data['location']
        logo = request.FILES['logo']
        email = request.data['email']
        
        company = Company.objects.create(
            user_id=user_id,
            company_name=company_name,
            location=location,
            logo=logo,
            email=email
        )    
        serialized_company_data = CompanySerializer(company)
        return JsonResponse(serialized_company_data.data)
    except  Exception as e:
        return JsonResponse({'message': str(e)})
 
@allowed_users(['A','CA'])   
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def company_update(request):
        company_id = request.GET.get('company_id')
        company_info = Company.objects.get(id = company_id)
        if 'company_name' in request.data:
            company_info.company_name = request.data.get('company_name')
        if 'location' in request.data:
            company_info.location = request.data.get('location')
        if 'logo' in request.FILES:
            company_info.logo = request.FILES.get('logo')
        if 'email' in request.data:
            company_info.email = request.data.get('email')
        
        serialized_data = CompanySerializer(instance=company_info , data=request.data, 
                                            partial=True, context={'instance':company_info})
        
        if serialized_data.is_valid():
            serialized_data.save()
        
            updated_serialized_company = CompanySerializer(company_info).data
            
            return JsonResponse({
                "message": "Company updated successfully",
                "company": updated_serialized_company
            })
        else:
            return JsonResponse({"error": updated_serialized_company.errors})
       
     

@method_decorator(allowed_users(['A,CA']), name='dispatch')
class CompanyDelete(LoginRequiredMixin,generics.DestroyAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()

# class ProfileList(LoginRequiredMixin,generics.ListAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer


class ProfileCreate(LoginRequiredMixin,generics.CreateAPIView):
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
    # permission_classes = [AllowAny]

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
    
class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer



class ProfileUpdate(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateProfileSerializer


# class UserProfileView(APIView):
#     def put(self, request, *args, **kwargs):
#         user = request.user
#         user_serializer = UserUpdateSerializer(user, data=request.data)
#         print('serialized')

#         print(user_serializer)
#         if user_serializer.is_valid():
#             print('valid')
#             # Update the user fields
#             user_serializer.save()
#             print('saved')
#             # Update the user profile fields
#             profile_data = user_serializer.validated_data.pop('profile', {})
#             profile_serializer = UpdateProfileSerializer(user.profile, data=profile_data, partial=True)
#             print("Profile serializer")
#             if profile_serializer.is_valid():
#                 print("Profile serializer valid")
#                 profile_serializer.save()
#                 print("profile serializer saved")
#                 return Response(user_serializer.data, status=status.HTTP_200_OK)
#             else:
#                 return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProfileUserUpdate(generics.UpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileUpdateSerializer

# class UserProfileUpdateView(APIView):
#     serializer_class = UserUpdateSerializer

#     def put(self, request, *args, **kwargs):
#         user = self.request.user
#         serializer = self.serializer_class(data=request.data)

#         if serializer.is_valid():
#             # old_password = serializer.validated_data.get('old_password')
#             new_username = serializer.validated_data.get('new_username')
#             # new_password = serializer.validated_data.get('new_password')
#             # confirm_password = serializer.validated_data.get('confirm_password')

#             # # Validate old password
#             # if old_password and not user.check_password(old_password):
#             #     return Response({'error': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)

#             # # Check if new password and confirm password match
#             # if new_password and new_password != confirm_password:
#             #     return Response({'error': 'New password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)

#             # Set the new username
#             if new_username:
#                 user.username = new_username

#             # Set the new password
#             # if new_password:
#             #     user.set_password(new_password)

#             # Update other profile fields
#             user.profile.email = serializer.validated_data.get('email', user.profile.email)
#             user.profile.profile.phone_number = serializer.validated_data.get('phone_number', user.profile.profile.phone_number)
#             user.profile.first_name = serializer.validated_data.get('first_name', user.profile.first_name)
#             user.profile.last_name = serializer.validated_data.get('last_name', user.profile.last_name)
#             user.profile.image = serializer.validated_data.get('image', user.profile.image)

#             user.save()

#             return Response({'success': 'User profile updated successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDelete(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class SkillList(LoginRequiredMixin,generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

 
@method_decorator(allowed_users(['A,CA']), name='dispatch')
class SkillDetail(LoginRequiredMixin,generics.RetrieveAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "message": "skill details retrieved successfully",
            "skill": serializer.data
        }
        return JsonResponse(response_data)
    
@method_decorator(allowed_users(['A,CA']), name='dispatch')
class SkillCreate(LoginRequiredMixin,generics.CreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    # model = Skill
    # fields = ['skill_name']
    
@method_decorator(allowed_users(['A,CA']), name='dispatch')
class SkillUpdate(LoginRequiredMixin,generics.UpdateAPIView):
    # model = Skill
    # fields = ['skill_name']
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

@method_decorator(allowed_users(['A,CA']), name='dispatch')
class SkillDelete(LoginRequiredMixin,generics.DestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def get_jobs_by_category(request):
    category_id = request.GET.get('category_id')
    print('category_id' , category_id)
    try:
        jobs = Job.objects.filter(job_category_id = category_id)
        job_serializer = JobSerializer(jobs, many=True)
        return JsonResponse(job_serializer.data, safe=False)
    except Exception as e:
        return JsonResponse({'message': str(e)})
    
@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def get_user_role(request):
    user_id = request.user.id
    print("user_id", user_id)
    try:
        user_role = Profile.objects.filter(user_id = user_id).values_list('role')[0]
        # user_role = Profile.objects.filter
        # user_role = Profile.objects.values_list('role', flat=True)[0]
        print('user_role ' , user_role)
        # profile_serializer = ProfileSerializer(user_role)
        return JsonResponse(user_role[0], safe=False)
    except Exception as e:
        return JsonResponse({'message': str(e)})

@csrf_exempt
@permission_classes([permissions.IsAuthenticated])
@api_view(['GET'])
def get_jobs_by_company(request):
    company_id = request.GET.get('id')
    try:
        company_jobs = Job.objects.filter(company_id = company_id)
        company_job_serializer = JobSerializer(company_jobs , many=True)
        job_company_response = {
            'jobs': company_job_serializer.data
        }
        return JsonResponse(job_company_response)
    except Exception as e:
        return JsonResponse({'message': str(e)})