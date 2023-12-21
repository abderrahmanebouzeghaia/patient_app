from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=100)
    family_name = models.CharField(max_length=255, default='')
    given_name = models.CharField(max_length=255, default='')
    gender = models.CharField(max_length=10, default='unknown')
    birth_date = models.DateField(default='1900-01-01')
    address_line = models.CharField(max_length=255, default='')
    address_city = models.CharField(max_length=255, default='')
    address_state = models.CharField(max_length=255, default='')
    address_postal_code = models.CharField(max_length=10, default='')
    address_country = models.CharField(max_length=255, default='')
    telecom_value = models.CharField(max_length=20, default='')

    def get_edit_url(self):
        return f'/patients/{self.patient_id}/edit/'

    def __str__(self):
        return f'{self.family_name}, {self.given_name}'
