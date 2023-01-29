from django.contrib import admin
from .models import *
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id','question','answer','level']

admin.site.register(Question,QuestionAdmin)
admin.site.register(QuestionUser)
admin.site.register(AnswerUser)
