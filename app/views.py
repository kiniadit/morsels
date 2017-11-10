from random import randrange
import time
import os

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django import forms
from django.forms import formset_factory
from .forms import UserRegistrationForm, MorselCreationForm, QuestionCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from app import urls
from app.models import Morsel, Question, Answer, Response

from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

morsel_id_session = None
incorrect_replies = ["Sorry, you have the incorrect answer. Try again!", 
                     "Not quite, maybe a little more thought?",
                     "This isn't the right answer, resend the correct SMS"]

class MorselList(ListView):
    model = Morsel

class MorselDetailView(DetailView):
   model = Morsel

@csrf_exempt  
def send_morsel(request):
    global morsel_id_session
    twiml_response = MessagingResponse()
    current_morsel_id = morsel_id_session if morsel_id_session else request.session.get('morsel_id')
    current_question_id = request.session.get('current_question_id')
    request_text = request.POST.get('Body')

    if current_morsel_id:
        if current_question_id:
            question = get_object_or_404(Question, pk=int(current_question_id))
            if not check_answer(request_text, question.id):
                twiml_response.message(incorrect_replies[randrange(len(incorrect_replies))-1])
                return HttpResponse(twiml_response)
                
            next_question = question.next()

            if not next_question:
                twiml_response.message(morsel.completed_text)
                request.session['current_question_id'] = request.session['morsel_id'] = None
                morsel_id_session = 0
            else:
                request.session['current_question_id'] = next_question.id
                twiml_response.message(next_question.question_text)           

            return HttpResponse(twiml_response)
        else:
            request.session['current_question_id'] = Question.objects.filter(morsel_id=current_morsel_id).first().id
            twiml_response.message(Question.objects.get(pk=int(request.session['current_question_id'])).question_text)
            return HttpResponse(twiml_response)
   
    else:
        raise Http404("SMS not setup")

def start_hunt(request, morsel_id):
    global morsel_id_session
    morsel = get_object_or_404(Morsel,pk=int(morsel_id))
    
    twilio_account_sid = settings.TWILIO_ACCOUNT_SID
    twilio_auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_number = settings.TWILIO_NUMBER

    twilio_client = Client(twilio_account_sid,twilio_auth_token)
    morsel_id_session = int(morsel_id)
    body = morsel.welcome_text + " Respond with 'yes' to start"
    outgoing_message = twilio_client.messages.create('+16467084542',body=body, from_=twilio_number)
    time.sleep(2)
    status_message = twilio_client.messages(outgoing_message.sid).fetch().status
    messages.success(request, "Message sent succesfully") if status_message == 'delivered' else  messages.success(request, "Message not sent succesfully")
    return HttpResponseRedirect('/app/morsels/')

def check_answer(request_text, question_id):
    answer_text = Answer.objects.filter(question_id=question_id).first().answer_text
    if request_text.strip().lower() == answer_text.strip().lower():
        return response.strip().lower()
    else:
        return None

def create_morsel(request):
    if request.method == 'POST':
        if request.POST['action'] == "+":
            extra = int(request.session['extra']) + 1
            form = MorselCreationForm(initial=request.POST)
            formset = formset_factory(QuestionCreationForm, extra=extra)()
        else:
            extra = int(request.session['extra'])
            form = MorselCreationForm(request.POST)
            formset = formset_factory(QuestionCreationForm, extra=extra)(request.POST)

            if form.is_valid() and formet.is_valid():
                name = form.cleaned_data["name"]
                start_time = form.cleaned_data["start_time"]
                end_time = form.cleaned_data["end_time"]
                welcome_text = form.cleaned_data["welcome_text"]
                completed_text = form.cleaned_data["completed_text"]
                m = Morsel(
                    name=name, 
                    start_time = start_time, 
                    end_time = end_time, 
                    welcome_text = welcome_text, 
                    completed_text = completed_text
                )
                m.save()
                # this order is important to be able to access the relations
                for form in formset:
                    question_text = form.cleaned_data["question_text"]
                    q = Question(
                        question_text=question_text,
                        model = m
                    )
                    q.save()
                return HttpResponseRedirect('/app/morsels/')
        request.session["extra"] = extra           
    else:
        form = MorselCreationForm()
        formset = formset_factory(QuestionCreationForm, extra=1)()
        request.session["extra"] = 1
    return render(request, 'app/create_morsel.html', {'form' : form, 'formset' : formset })

#user registration
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            username =user['username']
            email = user['email']
            password = user['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'app/register.html', {'form' : form})