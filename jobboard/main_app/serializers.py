
from rest_framework import serializers
from .models import User, Profile, Company , Application , Job, Job_category , Skill 
  
class ApplicationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Application
    fields = '__all__'
    
  def __init__(self, *args, **kwargs):
        super(ApplicationSerializer, self).__init__(*args, **kwargs)
        if 'instance' in self.context:
          for field_name in ['user', 'job']:
            self.fields[field_name].required = False
    
class SkillSerializer(serializers.ModelSerializer):
  class Meta:
    model = Skill
    fields = '__all__'
  
class JobSerializer(serializers.ModelSerializer):
    # applications = ApplicationSerializer(many=True)
    skills = SkillSerializer(many=True, read_only=True)
    
    class Meta:
      model = Job
      fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(JobSerializer, self).__init__(*args, **kwargs)
        if 'instance' in self.context:
          for field_name in ['user']:
            self.fields[field_name].required = False
      
     
    

    # def to_representation(self, instance):
    #     # Customize the representation for 'skills' to be an array
    #     representation = super(JobSerializer, self).to_representation(instance)
    #     representation['skills'] = SkillSerializer(instance.skills.all(), many=True).data
    #     return representation

    
    
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('pk','username', 'password')


# class UserUpdateSerializer(serializers.ModelSerializer):
#    class Meta:
#     model = User
#     fields = ('username', 'password')

class ProfileSerializer(serializers.ModelSerializer):
  skills = SkillSerializer(many=True, read_only=True)
  user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
  class Meta:
    model = Profile
    fields = '__all__'
  
    
# class UserSerializer(serializers.ModelSerializer):
#   # jobs = JobSerializer(many=True)
#   # profile = ProfileSerializer()
#   # applications = ApplicationSerializer(many=True)
#   class Meta:
#     model = User
#     fields = ('pk','username', 'first_name', 'last_name')

class CompanySerializer(serializers.ModelSerializer):
      # user = UserSerializer(required = True)
    class Meta:
        model = Company
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(CompanySerializer, self).__init__(*args, **kwargs)
        if 'instance' in self.context:
          for field_name in ['user']:
            self.fields[field_name].required = False
      

class UpdateProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'image', 'role', 'phone_number', 'skills')

    def update(self, instance, validated_data):
        # Update the role only if it's not in ('J', 'C')
        role = validated_data.get('role', instance.role)
        if role not in ('J', 'C'):
            role = 'J'
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.image = validated_data.get('image', instance.image)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.role = role  # Updated role
        instance.save()

        return instance
#    def update(self, instance, validated_data):
#         # Update the Profile instance with the validated data
#         instance.email = validated_data.get('email', instance.email)
#         instance.first_name = validated_data.get('first_name', instance.first_name)
#         instance.last_name = validated_data.get('last_name', instance.last_name)
#         instance.image = validated_data.get('image', instance.image)
#         instance.role = validated_data.get('role', instance.role)
#         instance.phone_number = validated_data.get('phone_number', instance.phone_number)

#         # Save the changes
#         instance.save()

#         return instance

# class ProfileUpdateSerializer(serializers.ModelSerializer):
#    skills = SkillSerializer(many=True, read_only=True)
#    user = UserSerializer(many=True, read_only=True)
#    class Meta:
#       model = Profile
#       fields = '__all__'

# class UserUpdateSerializer(serializers.Serializer):
#     # old_password = serializers.CharField(write_only=True)
#     new_username = serializers.CharField(write_only=True, required=False)
#     # new_password = serializers.CharField(write_only=True, required=False)
#     # confirm_password = serializers.CharField(write_only=True, required=False)
#     email = serializers.EmailField(write_only=True, required=False)
#     phone_number = serializers.CharField(write_only=True, required=False)
#     first_name = serializers.CharField(write_only=True, required=False)
#     last_name = serializers.CharField(write_only=True, required=False)
#     image = serializers.ImageField(required=False)

class Job_categorySerializer(serializers.ModelSerializer):
  jobs = JobSerializer(many=True, read_only=True)
  class Meta:
      model = Job_category
      fields = '__all__'


