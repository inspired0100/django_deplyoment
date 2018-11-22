from django import forms
#to check validation both builtin and custom neeed to call a package
from django.core import validators
#to crete exact like a model importing models
from main_app.models import Users,UserProfileInfo
#to use the django's buitin model class User
from django.contrib.auth.models import User


#the following fucntion is a example of custom validation
def is_first_letter_is_capital_and_alphabet(value):
    #WE Know the achi integer valuse of capital alphabets is from 65 to 90
    #converting the first letter of the input to ascii integer
    #fucntion ord('Letter') returns the ascii integer value
    asci_integer_of_first = ord(value[0])
    print(asci_integer_of_first)
    if asci_integer_of_first < 65 or asci_integer_of_first > 90:
        raise forms.ValidationError("Nmae should be start with capital and alphabet!")



class Demo_form(forms.Form):
    # here we are giving attrs fields for styling in html with bootstrapcss
    name = forms.CharField(max_length=64, label='Full Name', validators = [is_first_letter_is_capital_and_alphabet], #using the custom validation method
                                                    widget = forms.TextInput(attrs={
                                                    'placeholder' : 'Your full Name!',
                                                    }))
    email = forms.EmailField(max_length=128, widget = forms.EmailInput(attrs={
                                                        'placeholder' : 'Enter your email address here',
                                                        }))

    verify_email = forms.EmailField(max_length=128, label = 'Verify Email', widget = forms.EmailInput(attrs={
                                                        'placeholder' : 'Enter your email address again!',
                                                        }))

    phone = forms.CharField(max_length=32, required = False, widget = forms.TextInput(attrs={
                                                                        'placeholder' : 'Your Phone Number',
                                                                        }))
    bot_catcher = forms.CharField(required = False, widget = forms.HiddenInput, validators = [validators.MaxLengthValidator(0)]) #calling django's builtin validators

    def clean(self):
        all_cleaned_data = super().clean()
        name = all_cleaned_data.get('name')
        print(name)
        email = all_cleaned_data['email']
        print(email)
        vmail = all_cleaned_data['verify_email']
        print(vmail)

        if email != vmail:
            # two ways to make validation error
            #following one is field specific
            self.add_error('verify_email', "Make sure the emails are same!")

            # raise forms.ValidationError("Make sure the emails are same")
            #
            #
            #as we are using crispy forms and bootstrap so skipping this one
            #this still works but wont be displayed in page.
        else:
            print("emails matched")

        return None


class User_Form(forms.ModelForm):

    class Meta():
        # very important note in this Meta class we must assign Users(model) in side of model variable, other wise it won't work
        model = Users
        fields = '__all__'


    #here creatint new attributes of this form and overriding the model's attribute
    first_name = forms.CharField(max_length=32, validators = [is_first_letter_is_capital_and_alphabet], widget = forms.TextInput(attrs = {'placeholder':"Enter your first name"}))
    last_name = forms.CharField(max_length=32, validators = [is_first_letter_is_capital_and_alphabet], widget = forms.TextInput(attrs = {'placeholder':"Enter your last name"}))
    bot_catcher = forms.CharField(widget=forms.HiddenInput, required = False, validators = [validators.MaxLengthValidator(0)])
    email = forms.EmailField(max_length=64, widget=forms.EmailInput(attrs={'placeholder':'Enter mail address here'}))
    verify_email = forms.EmailField(max_length=64, label = 'Verify Email', widget=forms.EmailInput(attrs={'placeholder':'Enter your email address again!!'}))
    url = forms.URLField(max_length=128, required = False, widget = forms.URLInput(attrs = {"placeholder":"Website(optional)"}))

    def clean(self):
        all_cleaned_data = super().clean()
        email = all_cleaned_data['email']
        vmail = all_cleaned_data['verify_email']

        if email != vmail:
            self.add_error('verify_email', "Make sure the emails are same!")

        else:
            print("emails matched")

        return None

#here we will manipulate the django's builtin user form
#so that we need to import the model class User from django.auth.contrib.models
class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    #modifying the field of password attribute
    password = forms.CharField(widget=forms.PasswordInput())

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
