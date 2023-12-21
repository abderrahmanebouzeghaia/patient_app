from django.urls import path
from .views import patient_list, add_patient, edit_patient

urlpatterns = [
    path('', patient_list, name='patient_list'),
    path('add/', add_patient, name='add_patient'),
    path('<str:patient_id>/', edit_patient, name='edit_patient'),
]
