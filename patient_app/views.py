from django.urls import reverse
from django.shortcuts import render, redirect
from .models import Patient
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_POST

def get_patient_data(page=1):
    url = f'https://hapi.fhir.org/baseR5/Patient?_sort=-_lastUpdated&_count=500&_getpagesoffset={page - 1}'
    response = requests.get(url)
    data = response.json()
    patients = []
    for entry in data.get('entry', []):
        patient_data = entry.get('resource', {})
        patient = Patient(
            patient_id=patient_data.get('id'),
            family_name=patient_data.get('name', [{}])[0].get('family', ''),
            given_name=patient_data.get('name', [{}])[0].get('given', [''])[0],
            gender=patient_data.get('gender'),
            birth_date=patient_data.get('birthDate'),
            address_line=patient_data.get('address', [{}])[0].get('line', [''])[0],
            address_city=patient_data.get('address', [{}])[0].get('city', ''),
            address_state=patient_data.get('address', [{}])[0].get('state', ''),
            address_postal_code=patient_data.get('address', [{}])[0].get('postalCode', ''),
            address_country=patient_data.get('address', [{}])[0].get('country', ''),
            telecom_value=patient_data.get('telecom', [{}])[0].get('value', ''),
        )
        patients.append(patient)
    return patients

def patient_list(request, page=1):
    page = int(page)

    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        delete_patient(request, patient_id)

    patients = get_patient_data(page)
    context = {
        'patients': patients,
    }
    return render(request, 'patient_list.html', context)

def add_patient(request):
    if request.method == 'POST':
        patient_data = {
            "resourceType": "Patient",
            "name": [
                {
                    "use": "official",
                    "family": request.POST.get('family_name', ''),
                    "given": [request.POST.get('given_name', '')]
                }
            ],
            "gender": request.POST.get('gender', ''),
            "birthDate": request.POST.get('birth_date', ''),
            "address": [
                {
                    "use": "home",
                    "line": [request.POST.get('address_line', '')],
                    "city": request.POST.get('address_city', ''),
                    "state": request.POST.get('address_state', ''),
                    "postalCode": request.POST.get('postal_code', ''),
                    "country": request.POST.get('address_country', ''),
                }
            ],
            "telecom": [
                {
                    "system": "phone",
                    "value": request.POST.get('phone_number', ''),
                    "use": "home"
                }
            ]
        }

        response = requests.post('https://hapi.fhir.org/baseR5/Patient', json=patient_data)

        if response.status_code == 201:
            return redirect(reverse('patient_list'))

    return render(request, 'add_patient.html')

from django.shortcuts import redirect
from django.http import JsonResponse
import requests

@require_POST
def delete_patient(request, patient_id):
    base_url = "https://hapi.fhir.org/baseR5/Patient"
    delete_url = f"{base_url}/{patient_id}"

    headers = {
        "Content-Type": "application/fhir+json",
        "Accept": "application/fhir+json",
    }

    params = {
        "_cascade": "delete"
    }

    try:
        response = requests.delete(delete_url, headers=headers, params=params)

        if response.status_code == 200:
            print(f"Patient with ID {patient_id} successfully deleted.")
        else:
            print(f"Failed to delete patient. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'An error occurred during patient deletion.'}, status=500)

    return redirect('patient_list')




def edit_patient(request, patient_id):
    url = f'https://hapi.fhir.org/baseR5/Patient/{patient_id}'
    response = requests.get(url)
    
    if response.status_code == 200:
        patient_data = response.json()
    else:
        return JsonResponse({'error': 'Failed to retrieve patient data.'}, status=response.status_code)

    if request.method == 'POST':
        family_name = request.POST.get('family_name', '')
        given_name = request.POST.get('given_name', '')
        gender = request.POST.get('gender', '')
        birth_date = request.POST.get('birth_date', '')
        address_line = request.POST.get('address_line', '')
        address_city = request.POST.get('address_city', '')
        address_state = request.POST.get('address_state', '')
        postal_code = request.POST.get('postal_code', '')
        address_country = request.POST.get('address_country', '')
        telecom_value = request.POST.get('telecom_value', '')

        patient_data['name'] = [{'family': family_name, 'given': [given_name]}]
        patient_data['gender'] = gender
        patient_data['birthDate'] = birth_date
        patient_data['address'] = [{'use': 'home', 'line': [address_line],
                                   'city': address_city, 'state': address_state,
                                   'postalCode': postal_code, 'country': address_country}]
        patient_data['telecom'] = [{'system': 'phone', 'value': telecom_value, 'use': 'home'}]

        update_url = f'https://hapi.fhir.org/baseR5/Patient/{patient_id}'
        response = requests.put(update_url, json=patient_data, headers={'Content-Type': 'application/fhir+json'})

        if response.status_code == 200:
            return redirect(reverse('patient_list'))
        else:
            return JsonResponse({'error': 'Failed to update patient.'}, status=response.status_code)

    patient_name = patient_data.get('name', [{}])[0]
    patient_address = patient_data.get('address', [{}])[0]
    patient_telecom = patient_data.get('telecom', [{}])[0]
    if patient_name:
        family_name = patient_name.get('family', '')
        given_name = patient_name.get('given', [''])[0]
        patient_data['family_name'] = family_name
        patient_data['given_name'] = given_name
    if patient_address:
        address_line = patient_address.get('line', [''])[0]
        address_city = patient_address.get('city', '')
        address_state = patient_address.get('state', '')
        postal_code = patient_address.get('postalCode', '')
        address_country = patient_address.get('country', '')
        patient_data['address_line'] = address_line
        patient_data['address_city'] = address_city
        patient_data['address_state'] = address_state
        patient_data['postal_code'] = postal_code
        patient_data['address_country'] = address_country
    if patient_telecom:
        phone_number = patient_telecom.get('value', '')
        patient_data['telecom_value'] = phone_number
    birth_date = patient_data.get('birthDate', '')
    patient_data['birth_date'] = birth_date

    return render(request, 'edit_patient.html', {'patient': patient_data})
