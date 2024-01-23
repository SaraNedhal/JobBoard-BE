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

STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )

REQUEST_DESCRIPTION_CHOICES = (
  ('1', 'Premession to be a company admin'),
  ('2', 'demote the user to a job seeker')
)
class Skill(models.Model):
  skill_name = models.CharField(max_length=100)

  def __str__(self):
    return self.skill_name
  

class Profile(models.Model):
  email = models.EmailField(max_length = 254)
  role =  models.CharField(max_length=1, choices=ROLES,default=ROLES[1][0])
  phone_number = models.CharField(max_length=20)
  image = models.ImageField(upload_to='main_app/static/uploads', default="")
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  skills = models.ManyToManyField(Skill)
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)

class Company(models.Model):
  company_name = models.CharField(max_length=200)
  location = models.CharField(max_length=200)
  logo = models.ImageField(upload_to='main_app/static/uploads', default="")
  email = models.EmailField(max_length = 254)

  def __str__(self):
    return self.company_name
  
class Job_category(models.Model):
  category_name = models.CharField(max_length=100)

  def __str__(self):
    return self.category_name

  
class Job(models.Model):
  job_title = models.CharField(max_length=100)
  job_description = models.TextField(max_length=2500)
  job_salary = models.DecimalField(decimal_places=2,max_digits=12)
  job_created_at = models.DateTimeField(auto_now_add=True)
  job_updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
  company = models.ForeignKey(Company, on_delete=models.CASCADE)
  job_category = models.ForeignKey(Job_category, on_delete=models.CASCADE)
  skills = models.ManyToManyField(Skill)
  
  def __str__(self):
    return self.job_title
  

class Application(models.Model):
  application_date = models.DateTimeField(auto_now_add=True)
  application_updated_at = models.DateTimeField(auto_now=True)
  application_status = models.CharField(max_length=1, choices=STATUS,default=STATUS[2][0])
  resume = models.FileField(upload_to='main_app/static/uploads_resumes/', default="")
  job = models.ForeignKey(Job, on_delete = models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

class Admin_Requests(models.Model):
  user= models.ForeignKey(User, on_delete=models.CASCADE)
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
  request_description = models.CharField(max_length=2, choices=REQUEST_DESCRIPTION_CHOICES)
  date=models.DateTimeField(auto_now_add=True)




  

  
  
