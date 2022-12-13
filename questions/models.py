from django.db import models
from accounts.models import *

level_choice=(
    ('1',"Easy"),
    ('2',"Normal"),
    ('3',"difficult")
)
# Create your models here.
class Question(models.Model):
    question=models.CharField(max_length=1000)
    choice=models.JSONField()
    answer=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level=models.CharField(default='1',max_length=100)

class QuestionUser(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    correct=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class AnswerUser(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    questions=models.JSONField()
    answers=models.ManyToManyField(QuestionUser,related_name='answers')
    complete=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coins=models.FloatField(default=0)

