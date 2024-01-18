from django.urls import path
from . import views

urlpatterns = [
   path('application/' , views.application_index , name="application_index"),
  path('application/<int:user_id>/create/' , views.application_create, name="applications_create" ),
 
]