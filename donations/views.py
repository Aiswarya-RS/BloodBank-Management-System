from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        messages.success(request, 'User registered successfully!')
        return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  # If authentication fails, redirect back to login
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def request_blood(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        units = request.POST['units']
        # You can save this request to DB (we’ll set that up later)
        messages.success(request, f'Requested {units} units of {blood_group} blood')
        return redirect('home')
    return render(request, 'request_blood.html')

from django.shortcuts import render
from .models import BloodRequest

def view_requests(request):
    # Get all blood requests from the database
    requests = BloodRequest.objects.all()
    return render(request, 'view_requests.html', {'requests': requests})

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def request_blood(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        units = request.POST['units']
        messages.success(request, f'Requested {units} units of {blood_group} blood')
        return redirect('home')
    return render(request, 'request_blood.html')



from .models import BloodRequest  # add this at the top

@login_required(login_url='login')
def request_blood(request):
    if request.method == 'POST':
        blood_group = request.POST['blood_group']
        units = request.POST['units']

        BloodRequest.objects.create(
            user=request.user,
            blood_group=blood_group,
            units=units
        )

        messages.success(request, f'Requested {units} units of {blood_group} blood')
        return redirect('home')

    return render(request, 'request_blood.html')


@login_required(login_url='login')
def view_requests(request):
    requests = BloodRequest.objects.all().order_by('-requested_at')
    return render(request, 'view_requests.html', {'requests': requests})


from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def mark_fulfilled(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)
    blood_request.status = 'Fulfilled'
    blood_request.save()
    messages.success(request, 'Request marked as fulfilled.')
    return redirect('view_requests')

