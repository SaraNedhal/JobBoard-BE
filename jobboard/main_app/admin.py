from django.contrib import admin
from .models import Skill, Profile, Company, Job_category, Job, Application


# Register your models here.
admin.site.register(Job_category)
admin.site.register(Job)
admin.site.register(Skill)
