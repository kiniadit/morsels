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
    newsletter_signup = forms.BooleanField(
        required = False,
        label = 'Would you like to receive occasional emails?',
        widget = forms.CheckboxInput()
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
    public_enabled = forms.BooleanField(
        required = False,
        label = 'Do you want to make this Crumble public? (Anyone will be able to join)',
        widget = forms.CheckboxInput()
    )


class QuestionAnswerCreationForm(forms.Form):
    question_text = forms.CharField(
        required = False,
        label = 'Question', 
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'Ask something fun!'}) 
    )
    answer_text = forms.CharField(
        required = False,
        label = 'Answer', 
        max_length = 200,
        widget = forms.TextInput(attrs={'placeholder' : 'and the answer is...'}) 
    )
    
class NewsletterSignupForm(forms.Form):
    email = forms.CharField(
        required = False
    )