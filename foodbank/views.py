from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import generic

from .models import Volunteer

import re

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

class VolunteerView(generic.ListView):
    model = Volunteer
    template_name='volunteer.html'
    context_object_name='volunteers'
    # phoneNumberRegex = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
    # emailRegex = re.compile("[^@]+@[^@]+\.[^@]+")

    def get_queryset(self):
        return Volunteer.objects.all()
    
    def get(self, req):
        error_msg = req.GET['error_msg'] if 'error_msg' in req.GET else None
        context = {
            self.context_object_name: self.get_queryset(),
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Check that at least one field is not empty
        if self.validate_fields(first_name, last_name, street_address, city, home_state, zip_code, phone_number, email):            
            if 'add' in request.POST:
            
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
        else:
            error_msg = "All fields are required to create volunteer object"
            return redirect(reverse("foodbank:volunteer")+'?error_msg='+error_msg)



        return redirect(reverse("foodbank:volunteer"))
    
    def validate_fields(self, first_name, last_name, street_address, city, home_state, zip_code, phone_number, email):
        fname_valid = first_name != ""
        lname_valid = last_name != ""
        street_address_valid = street_address != ""
        city_valid = city != ""
        home_state_valid = home_state != ""
        zip_code_valid = zip_code != ""
        # phone_number_valid = self.phoneNumberRegex.match(phone_number)
        # email_valid = self.emailRegex.match(email)
        phone_number_valid = phone_number != ""
        email_valid = email != ""

        if fname_valid and lname_valid and street_address_valid and city_valid and home_state_valid and zip_code_valid and phone_number_valid and email_valid:
            return True
        else:
            return False


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

        return redirect(reverse("foodbank:volunteer"))

    context = {
        'volunteers': volunteers,
        'query': query,
    }
    return render(request, 'volunteer.html', context)
