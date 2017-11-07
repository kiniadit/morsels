from django.contrib import admin
from django.contrib.auth.models import User
from app.models  import Morsel, Question, Answer, Profile
# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = []
    fields = ('answers',)

class ProfileInline(admin.TabularInline):
    model = Profile
    fields = ('bio',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'profile_bio','email', 'first_name', 'last_name')
    def profile_bio(self, instance):
        return instance.profile.bio
    inlines = (ProfileInline,)
    list_filter = ('is_staff', 'is_superuser')

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Morsel)
admin.site.register(Question)
admin.site.register(Answer)

