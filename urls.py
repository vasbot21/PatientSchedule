from django.urls import path
from . import views

urlpatterns = [
    path('', views.patients, name='patients'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('patient_<int:patient_id>/', views.patient, name='patient'),
    path('delete_patient_<int:patient_id>/', views.delete_patient, name='delete_patient')
]
