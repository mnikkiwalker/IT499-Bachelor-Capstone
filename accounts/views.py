from django.shortcuts import render

# Create your views here.
def login_view(request):
    # Django looks inside the 'templates' folder automatically based on Step 1
    return render(request, 'accounts/login.html')