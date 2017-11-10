from django import forms
from django.forms import formset_factory

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput()
    )

class MorselCreationForm(forms.Form):
    start_time = forms.DateTimeField(
        required = False,
        label = 'Start Time and Date',
        widget = forms.DateTimeInput(attrs={'placeholder': 'MM//DD/YY HH:MM'})
    )
    end_time = forms.DateTimeField(
        required = False,
        label = 'End Time and Date', 
        widget = forms.DateTimeInput(attrs={'placeholder': 'MM//DD/YY HH:MM'})
    )
    name = forms.CharField(
        required = False,
        label = 'Morsel Name',
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'Name your hunt...'})
    )
    welcome_text = forms.CharField(
        required = False,
        label = 'Welcome Message',
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'Greetings, instructions and dragons!'})
    )
    completed_text = forms.CharField(
        required = False,
        label = 'Goodbye Message', 
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'Be nice, say thank you to your players!'})
    )


class QuestionCreationForm(forms.Form):
    question_text = forms.CharField(
        required = False,
        label = 'Q: ', 
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'Ask something fun!'}) 
    )