from .views import (LoginView,UserView,
RegisterView,
SocialLoginView,Addquestion,
AnswerAPI,SupportQuestion
)
from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views
from django.conf.urls import include
urlpatterns = [
    path('oauth/login', SocialLoginView.as_view()),
    path("signup", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("user/info", UserView.as_view()),
    path("addquestion", Addquestion.as_view()),
    path("answer/<int:id>", AnswerAPI.as_view()),
    path("suport/<int:id>", SupportQuestion.as_view()),
    path("refresh", jwt_views.TokenRefreshView.as_view()),
]