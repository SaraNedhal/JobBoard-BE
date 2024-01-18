from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
STATUS= (
  ('R' , 'Reject'),
  ('A' , 'Accept'),
  ('S' , 'Submitted')
)
ROLES = (
  ('A' , 'Admin'),
  ('J' , 'Job seeker'),
  ('C' , 'Company admin')
)

  
class Skill(models.Model):
  skill_name = models.CharField(max_length=100)

class Profile(models.Model):
  email = models.EmailField(max_length = 254)
  role =  models.CharField(max_length=1, choices=ROLES,default=ROLES[1][0])
  phone_number = models.CharField(max_length=20)
  image = models.ImageField(upload_to='main_app/static/uploads', default="")
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  skills = models.ManyToManyField(Skill)


class Company(models.Model):
  company_name = models.CharField(max_length=200)
  location = models.CharField(max_length=200)
  logo = models.ImageField(upload_to='main_app/static/uploads', default="")
  email = models.EmailField(max_length = 254)
  
class Job_category(models.Model):
  category_name = models.CharField(max_length=100)

  
class Job(models.Model):
  job_title = models.CharField(max_length=100)
  job_description = models.TextField(max_length=2500)
  job_salary = models.DecimalField(decimal_places=2,max_digits=12)
  job_created_at = models.DateTimeField(auto_now_add=True)
  job_updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  job_category = models.ForeignKey(Job_category, on_delete=models.CASCADE)
  skills = models.ManyToManyField(Skill)
  
  

class Application(models.Model):
  application_date = models.DateTimeField(auto_now_add=True)
  application_updated_at = models.DateTimeField(auto_now=True)
  application_status = models.CharField(max_length=1, choices=STATUS,default=STATUS[2][0])
  resume = models.FileField(upload_to='main_app/static/uploads_resumes/', default="")
  job = models.ForeignKey(Job, on_delete = models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)





  

  
  
