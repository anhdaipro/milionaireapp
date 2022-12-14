from django.shortcuts import render
from accounts.models import *
from questions.models import *
import re
from django.conf import settings
import random
from twilio.rest import Client
from django.template.loader import get_template
from django.db.models import F
from django.core.paginator import Paginator
from django.db.models import Max, Min, Count, Avg,Sum
from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView,
    UpdateAPIView, DestroyAPIView,GenericAPIView,
)
from twilio.rest import Client
from django.template.loader import render_to_string
from rest_framework.views import APIView

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.core.mail import EmailMessage
from django.db.models import Q
import datetime,jwt
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate,login,logout
from .serializers import (RegisterSerializer,UserinfoSerializer,VerifyEmailSerializer,QuestionSerializer)
from social_django.utils import load_strategy, load_backend
from django.core.mail import EmailMessage
import paypalrestsdk
from paypalrestsdk import Sale
from rest_framework import generics, permissions, status, views
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# Create your views here.,
paypalrestsdk.configure({
  'mode': 'sandbox', #sandbox or live
  'client_id': 'AY2deOMPkfo32qrQ_fKeXYeJkJlAGPh5N-9pdDFXISyUydAwgRKRPRGhiQF6aBnG68V6czG5JsulM2mX',
  'client_secret': 'EJBIHj3VRi77Xq3DXsQCxyo0qPN7UFB2RHQZ3DOXLmvgNf1fXWC5YkKTmUrIjH-jaKMSYBrH4-9RjiHA' })

account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = Client(account_sid, auth_token)

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializers_class=RegisterSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SocialLoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        provider = request.data.get('provider')
        social_id = request.data.get('social_id')
        name=request.data.get('name')
        username=request.data.get('username')
        email=request.data.get('email')
        password=request.data.get('password')
        avatar=request.data.get('avatar')
        users=CustomUser.objects.filter(social_id=social_id,auth_provider=provider)
        if users.exists():
            user=users.first()
        else:
            user=CustomUser.objects.create(
                name=name,username=username,social_id=social_id,
                email=email,auth_provider=provider
            )
            user.set_password(password)
            user.save()
        try:
            
            refresh = RefreshToken.for_user(user)
            data = {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
         
            }
            return Response(data)
        except Exception:
            return Response({
            "error": {"access_token": "Please provider valid"}}, status=status.HTTP_400_BAD_REQUEST)

class Registeremail(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        username=request.data.get('username')
        email=request.data.get('email')
        verify=request.data.get('verify')
        check_user=User.objects.filter(Q(username=username) | Q(email=email))
        if check_user.exists():
            return Response({'error':True})
        else:
            usr_otp = random.randint(100000, 999999)
            Verifyemail.objects.create(email = email, otp = usr_otp)
            email_body = f"Chào mừng bạn đến với anhdai.com,\n Mã xác nhận email của bạn là: {usr_otp}"
            data = {'email_body': email_body, 'to_email':email,
                    'email_subject': "Welcome to AnhDai's Shop - Verify Your Email!"}
            email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
            email.send()
            return Response({'error':False})
        
class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        otp = int(request.data.get("otp"))
        email=request.data.get('email')
        reset=request.data.get('reset')
        verifyemail=Verifyemail.objects.filter(email=email).last()
        if verifyemail.otp==otp:    
            return Response({'verify':True})
        else:
            return Response({'verify':False})

class Sendotp(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        phone=request.data.get('phone')
        login=request.data.get('login')
        reset=request.data.get('reset')
        usr_otp = random.randint(100000, 999999)
        otp=SMSVerification.objects.create(pin=usr_otp,phone=phone)
        if login: 
            message = client.messages.create(
                body=f"DE DANG NHAP TAI KHOAN VUI LONG NHAP MA XAC THUC {otp.pin}. Co hieu luc trong 15 phut. Khong chia se ma nay voi nguoi khac",
                from_=settings.TWILIO_FROM_NUMBER,
                to=str(phone)
            )
        elif reset:
            message = client.messages.create(
                body=f"DE CAP NHAT MAT KHAU VUI LONG NHAP MA XAC THUC {otp.pin}. Co hieu luc trong 15 phut. Khong chia se ma nay voi nguoi khac",
                from_=settings.TWILIO_FROM_NUMBER,
                to=str(phone)
            )
        else:
            message = client.messages.create(
                body=f"DE DANG KY TAI KHOAN VUI LONG NHAP MA XAC THUC {otp.pin}. Co hieu luc trong 15 phut. Khong chia se ma nay voi nguoi khac",
                from_=settings.TWILIO_FROM_NUMBER,
                to=str(phone)
            )
        data={'id':otp.id}
        return Response(data)

class VerifySMSView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        id=request.data.get('id')
        pin = int(request.data.get("pin"))
        phone=request.data.get('phone')
        reset=request.data.get('reset')
        otp=SMSVerification.objects.get(id=id)
        profile=Profile.objects.filter(phone=phone)
        if otp.pin==pin:
            otp.verified=True
            otp.save()
            if profile.exists():
                if reset:
                    user=profile.first().user
                    uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                    token = default_token_generator.make_token(user)
                    return Response({'verify':True,'token':token,'uidb64':uidb64})
                return Response({'verify':True,'avatar':profile.first().avatar.url,'username':profile.first().user.username,'user_id':profile.first().user.id})
            else:
                return Response({'verify':True})
        else:
            return Response({'verify':False})

class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request,*args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        if username:
            user = authenticate(request, username=username, password=password)
        if email:
            user = authenticate(request, email=username, password=password)  
        try:
            refresh = RefreshToken.for_user(user)
            
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
      
            }
            return Response(data)
        except Exception:
            raise AuthenticationFailed('Unauthenticated!')

class UserView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            user=request.user
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user=request.user
        serializer = UserinfoSerializer(user)
        return Response(serializer.data)
class Addquestion(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        user=CustomUser.objects.get(id=1)
        easy=Question.objects.filter(level="1").values('id')
        normal=Question.objects.filter(level="2").values('id')
        difficult=Question.objects.filter(level="3").values('id')
        easy_list=random.sample(list(easy),k=5)
        normal_list=random.sample(list(normal),k=5)
        difficult_list=random.sample(list(difficult),k=5)
        questions=easy_list+normal_list+difficult_list
        anwsers=AnswerUser.objects.create(user=user,questions=questions)
        questionuser=QuestionUser.objects.create(user=user,question_id=easy_list[0]['id'])
        first_question=Question.objects.get(id=easy_list[0]['id'])
        data={'question':QuestionSerializer(first_question).data,'id':anwsers.id,'questionuserid':questionuser.id}
        return Response(data)
def now():
    return timezone.now()
class SupportQuestion(APIView):
    def post(self,request,id):
        support_type=request.data.get('support_type')
        question_id=request.data.get('question_id')
        question=Question.objects.get(id=question_id)
        answeruser=AnswerUser.objects.get(id=id)
        
        data={}
        if support_type=='1':
            choice=[item for item in question.choice if item!=question.answer]
            choice_hiden=random.sample(list(choice),k=2)
            data.update({'choice_hiden':choice_hiden})
        else:
            user=CustomUser.objects.get(id=1)
            questions=Question.objects.filter(Q(level=question.level) & ~Q(id=question_id)).values('id')
            id_change=random.choice(list(questions))
            questions_update=[item if item['id']!=question_id else id_change for item in answeruser.questions]
            question_change=Question.objects.get(id=id_change['id'])
            answeruser.questions=questions_update
            answeruser.save()
            questionuser_change=QuestionUser.objects.create(user=user,question_id=id_change['id'])
            data.update({'question':QuestionSerializer(question_change).data,'questionuserid':questionuser_change.id})
        return Response(data)
class AnswerAPI(APIView):
    permission_classes = (AllowAny,)
    def post(self,request,id):
        answer=request.data.get('answer')
        support=request.data.get('support')
        questionuserid=request.data.get('questionuserid')
        questionuser=QuestionUser.objects.get(id=questionuserid)
        question_id=request.data.get('question_id')
        answeruser=AnswerUser.objects.get(id=id)
        question=Question.objects.get(id=question_id)
        user=CustomUser.objects.get(id=1)
        time_experi=timezone.now()-questionuser.created_at
        time=time_experi.total_seconds()
        data={}
        if answer==question.answer:
            if time<=60 or support: 
                questionuser.correct=True
                questionuser.save()
                answeruser.answers.add(questionuser)
                listquestions=[item['id'] for item in answeruser.questions]
                index=listquestions.index(question_id)
                user.coins=user.coins+100
                user.save()
                if index==len(listquestions)-1:
                    data.update({'success':True,'correct':True})
                    answeruser.complete=True
                    answeruser.save()
                else:
                    nextid=answeruser.questions[index+1]['id']
                    question_next=Question.objects.get(id=nextid)
                    questionuser_next=QuestionUser.objects.create(user=user,question_id=nextid)
                    data.update({'questionNumber':index+1+1,'correct':True,'question':QuestionSerializer(question_next).data,'questionuserid':questionuser_next.id})
            else:
                data.update({'correct':False,'message':"expiried"})
                answeruser.complete=True
                answeruser.save()
        else:
            data.update({'correct':False,'message':"notcorrect"})
            answeruser.complete=True
            answeruser.save()
        
        return Response(data)