from django.shortcuts import render
# to using the forms we have to import them in the views.py file
from main_app import forms
from main_app.models import Users
from main_app.forms import User_Form, UserForm, UserProfileInfoForm

#additional imports for the login and logout capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.

def demo_from(request):
    form = forms.Demo_form()

    if request.method == 'POST':
        form = forms.Demo_form(request.POST)

        if form.is_valid():
            print("Validation success")
            print(form.cleaned_data['name'])



    return render(request, 'main_app/demo_form.html', {'form':form})
    #we are passing here the context (last argument) so that we can use template tagging in the html file

def welcome(request):

    return render(request, 'main_app/welcome.html', {'for_custom':'Custom Filters checking!!'})

def sign_up(request):
    form = forms.User_Form()

    if request.method == "POST":
        form = forms.User_Form(request.POST)

        if form.is_valid():
            print("validation success of user form success")
            form.save(commit=True)
            print('Saved to databse!!')
            return current_users(request)
        else:
            print("validation error")

    return render(request, 'main_app/sign_up.html', {'form':form})

def current_users(request):
    user_list = Users.objects.order_by('first_name')

    return render(request, 'main_app/current_users.html', {"user": user_list})



def registration_form(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            #any csv,pdf,pic,are in returned with request.Files
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'main_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def login_form(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('welcome'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'main_app/login.html', {})


@login_required
def logout_page(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('welcome'))
