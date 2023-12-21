from django.shortcuts import redirect
from django.urls import reverse, resolve

class RedirectToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(reverse('login')):
            return redirect('login')

        return self.get_response(request)

class RedirectAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            allowed_patterns = ['patient_list', 'add_patient', 'edit_patient', 'logout']
            if resolve(request.path_info).url_name not in allowed_patterns:
                return redirect('patient_list')

        return self.get_response(request)
