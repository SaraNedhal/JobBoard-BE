from rest_framework import serializers
from .models import User, Profile, Company , Application , Job, Job_category , Skill 
  
class ApplicationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Application
    fields = '__all__'
    
class SkillSerializer(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = '__all__'
  
class JobSerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True)
    skills = SkillSerializer(many=True)
    
    class Meta:
      model = Job
      fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
  companies = JobSerializer(many=True)
  class Meta:
    model = Company
    fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True)
  class Meta:
    model = Profile
    fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
  jobs = JobSerializer(many=True)
  profile = ProfileSerializer()
  applications = ApplicationSerializer(many=True)
  class Meta:
    model = User
    fields = '__all__'
    
      
class Job_categorySerializer(serializers.ModelSerializer):
  jobs = JobSerializer(many=True)
  class Meta:
      model = Job_category
      fields = '__all__'


