from django.urls import path
from ..api.views import *

urlpatterns = [
    path('usermanagement/', UserData.as_view()),
    # path('logout/', LogoutApiView.as_view(), name="logout"),

]
