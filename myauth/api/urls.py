from django.urls import path
from myauth.api.views import *

urlpatterns = [
    path('usermanagement/', UserData.as_view()),
    path('login/',LoginAPI.as_view()),
    path('updateuser/',UpdateUser.as_view()),
    path('deleteuser/<int:id>/',DeleteUser.as_view()),
    path('me/', UserMeApi.as_view()),
    path('updatepass/',SetNewPass.as_view()),
    path('logout/', LogoutApiView.as_view(), name="logout"),

]
