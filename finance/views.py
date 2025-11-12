from django.shortcuts import render, redirect
from finance.forms import RegisterForm
from django.contrib.auth import login
from django.views import View


# class RegisterView(View):
#     def get(self, request, *args, **kwargs):
#         form = RegisterForm()
#         return render(request, 'finance/register.html', {'form': form})
#     def get(self, request, *args, **kwargs):
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             redirect('')

# class DashboardView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'finance/dashboard.html')



from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegisterForm 
from django.contrib.auth.decorators import login_required

def RegisterView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard') 
    else:
        form = RegisterForm()
    return render(request, 'finance/register.html', {'form': form})
@login_required
def DashboardView(request):
    return render(request, 'finance/dashboard.html')

