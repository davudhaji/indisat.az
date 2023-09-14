# import psycopg2
import json
import logging
from datetime import datetime, timedelta
from http import server

from core.models import *
from django.contrib.auth import authenticate, get_user_model
from django.db.models import (
    Avg,
    BooleanField,
    Case,
    CharField,
    Count,
    DateTimeField,
    ExpressionWrapper,
    F,
    Func,
    Max,
    Q,
    Sum,
    Value,
    When,
)
from knox.auth import *
from knox.models import AuthToken
from knox.views import LogoutView
from pytz import timezone
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView


class UserData(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response([""])
