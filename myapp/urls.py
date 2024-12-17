from django.urls import path
from .import views

app_name ='myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name = 'contact' ),
    path('service/', views.service, name='service'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('about/', views.about , name = 'about'),
    path('team/', views.team, name='team'),
    path('show_contact/', views.retrieve_contact,name = 'show_contact'),
    path('delete/<int:id>/', views.delete_contact, name ='delete_contact'),
    path('edit/<int:contact_id>/', views.update_contact, name = 'update_contact'),
    path('upload/', views.upload_image, name='upload_image'),

]