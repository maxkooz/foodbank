from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Volunteer

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return redirect(reverse('foodbank:main_page'))
    else:
        return render(request, 'home.html', {"error_msg": "Login Failed"})
    
def logout_view(request):
    logout(request)
    return redirect(reverse('foodbank:main_page'))

def sign_up_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]

    user = User.objects.create_user(username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    return redirect(reverse('foodbank:main_page'))

def main_page_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('foodbank:home'))

    return render(request, 'main_page.html')

def volunteer_view(request):
    volunteers = Volunteer.objects.all()

    query = request.GET.get('q')
    if query:
        volunteers = volunteers.filter(first_name__icontains=query)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Check that at least one field is not empty
        if any([first_name, last_name, street_address, city, home_state, zip_code, phone_number, email]):
            Volunteer.objects.create(
                first_name=first_name,
                last_name=last_name,
                street_address=street_address,
                city=city,
                home_state=home_state,
                zip_code=zip_code,
                phone_number=phone_number,
                email=email
            )
        elif 'edit' in request.POST:
            volunteer_id = request.POST.get('volunteer_id')
            volunteer = Volunteer.objects.get(id=volunteer_id)
            volunteer.first_name = request.POST.get('first_name')
            # Update other fields for editing
            volunteer.save()
        elif 'delete' in request.POST:
            volunteer_id = request.POST.get('volunteer_id')
            Volunteer.objects.get(id=volunteer_id).delete()

        return redirect('volunteer')

    context = {
        'volunteers': volunteers,
        'query': query,
    }
    return render(request, 'volunteer.html', context)
