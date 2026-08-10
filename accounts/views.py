from django.shortcuts import render
from .models import Patient
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

#####Logins now handled by django built-in login views
# def login_view(request):
#     # Django looks inside the 'templates' folder automatically based on Step 1
#     return render(request, 'accounts/login.html')

@staff_member_required
def search_api(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = list(
            Patient.objects.filter(date_of_birth=query)[:10].values('patient_id', 'first_name', 'last_name')
        )
    return JsonResponse({'results': results})