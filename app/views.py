from random import randrange
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
import os
from app import urls
from app.models import Morsel, Question, Answer, Response
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from django.views.generic import ListView, DetailView

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
    message = twilio_client.messages.create('+16467084542',body=body, from_=twilio_number)
    
    return HttpResponse("Message %s sent" % message.sid, content_type='text/plain', status=200)

def check_answer(request_text, question_id):
    answer_text = Answer.objects.filter(question_id=question_id).first().answer_text
    if request_text.strip().lower() == answer_text.strip().lower():
        return response.strip().lower()
    else:
        return None
