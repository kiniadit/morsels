from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
# Create your modles here.
class DateTime(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True

class Morsel(DateTime):
    start_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True, default=timezone.now)
    name = models.CharField(max_length = 200)
    welcome_text = models.CharField(max_length = 200)
    completed_text = models.CharField(max_length = 200)
    status = models.CharField(max_length = 80)

    def __str__(self):
        return self.name

class Question(DateTime):
    question_text = models.CharField(max_length = 400)
    morsel = models.ForeignKey(Morsel, on_delete = models.CASCADE, related_name = "questions")
    
    def __str__(self):
        return self.question_text

    def next(self):
        morsel = Morsel.objects.get(pk=self.morsel_id)
        next_q = morsel.questions.order_by('id').filter(id__gt=self.id)

        return next_q.first() if next_q.first() else None
    
class Answer(DateTime):
    answer_text = models.CharField(max_length = 100)
    question = models.OneToOneField(Question, on_delete=models.CASCADE, related_name = "answer")

    def __str__(self):
        return self.answer_text

class Response(DateTime):
    response_text = models.CharField(max_length = 100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    #include a session foreign key?
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.response_text

class AnonymousUser(models.Model):
    phonenumber = models.CharField(max_length=40, blank=True)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=40, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()