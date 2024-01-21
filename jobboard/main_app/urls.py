from django.urls import path
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    path('hello-world/', views.hello_world, name='hello_world'),

    # Paths for all the CRUD Operations for job_category - CBVs
    path('job_categories/', views.JobCategoryList.as_view(), name='job_category_list'),
    path('job_categories/<int:pk>', views.JobCategoryDetail.as_view(), name="job_category_detail"),
    path('job_categories/create/', views.JobCategoryCreate.as_view(), name='job_category_create'),
    path('job_categories/<int:pk>/update/', views.JobCategoryUpdate.as_view(), name='job_category_update'),
    path('job_categories/<int:pk>/delete/', views.JobCategoryDelete.as_view(), name='job_category_delete'),

    # Paths for all the CRUD Operations for jobs - CBVs
    path('jobs/', views.JobList.as_view(), name='jobs_index'),
    path('jobs/<int:pk>', views.JobDetail.as_view(), name="jobs_detail"),
    path('jobs/create/', views.JobCreate.as_view(), name='jobs_create'),
    path('jobs/<int:pk>/update/', views.JobUpdate.as_view(), name='jobs_update'),
    path('jobs/<int:pk>/delete/', views.JobDelete.as_view(), name='jobs_delete'),

     # Paths for all the CRUD Operations for Company Model - CBVs
    path('company/', views.CompanyList.as_view(), name='company_index'),
    path('company/<int:pk>', views.CompanyDetail.as_view(), name="company_detail"),
    path('company/create/', views.CompanyCreate.as_view(), name='company_create'),
    path('company/<int:pk>/update/', views.CompanyUpdate.as_view(), name='company_update'),
    path('company/<int:pk>/delete/', views.CompanyDelete.as_view(), name='company_delete'),

    path('application/' , views.application_list , name="application_list"),
    path('application/<int:user_id>/create/' , views.application_create, name="applications_create" ),
  
    path('accounts/signup/', views.signup, name='signup'),
]