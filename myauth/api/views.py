from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.signals import user_logged_in
from knox.auth import *
from knox.models import AuthToken
from knox.settings import knox_settings
from knox.views import LoginView, LogoutView
from myauth.api.serializer import *
from myauth.utils.utils import *
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.serializers import DateTimeField
from rest_framework.views import APIView

USER_MODEL = settings.AUTH_USER_MODEL


class UserData(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = User.objects.all().values(
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
            "job",
            "job__name",
            "team",
            "team__name",
            "role",
            "role__name",
            "branch",
            "branch__name",
            "customer_access_by_ids",
        )
        return Response(data)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data, "DAATA")
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            return Response(
                {
                    "user": RegistrationSerializer(user).data,
                    # "token": token
                }
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenAuthentication(TokenAuthentication):
    def validate_user(self, auth_token):
        return auth_token.user, auth_token


class LogoutApiView(LogoutView):
    authentication_classes = (CustomTokenAuthentication,)


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            _, token = AuthToken.objects.create(user)
            return Response(
                {
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": f"Token {token}",
                }
            )
        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SetNewPass(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = request.data.get("password")
            id = request.data.get("id")
            usr = User.objects.filter(id=id)
            if usr:
                usr[0].set_password(password)
                usr[0].save()
                return Response(["Password update"])
            return Response(["User not found"])


class UpdateUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            update_data = request.data
            update_data.pop("id")
            print(serializer.data, "THIS ID")
            usr = User.objects.filter(id=serializer.data.get("id"))
            print("User: ", usr)
            if usr:
                usr.update(**update_data)
            else:
                return Response(["User not found"])
            print("User update olub bitmelidi")
            return Response(request.data)

        return Response([""])


class UserMeApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        response_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class DeleteUser(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        print("id", self.kwargs["id"])

        user = User.objects.filter(id=self.kwargs["id"])
        if not user:
            return Response(["User not found"])

        user.delete()

        return Response({"result": "user delete"})


class UserRegistration(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    @staticmethod
    def get_token(user, request):
        instance, token = AuthToken.objects.create(user, knox_settings.TOKEN_TTL)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        datetime_format = knox_settings.EXPIRY_DATETIME_FORMAT
        data = {
            "expiry": DateTimeField(format=datetime_format).to_representation(
                instance.expiry
            ),
            "token": f"Token {token}",
        }
        return data

    @staticmethod
    def user_data(user):
        response_data = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "is_master": user.is_master,
            "picture": user.get_picture(),
            "is_active": user.is_active,
            "is_first_login": user.is_staff,
        }

        response_data.update({"roles": user_groups(user)})
        return response_data

    def create(self, request, *args, **kwargs):
        front_url = request.query_params.get("url", None)
        if front_url:
            user_data = super().create(request, *args, **kwargs).data
            user = User.objects.get(pk=user_data["id"])
            link = front_url + "?uid={}&token={}"

            # _body = 'Hi {}, Please the link below to activate your account \n {}'
            # link = link.format(urlsafe_base64_encode(force_bytes(user.pk)),
            #                         account_activation_token.make_token(user))
            # _body = welcome_mail({'user': user, 'link': link})
            # data = {
            #     'to': user.email,
            #     'link': link,
            #     'content': _body,
            #     'subject': 'Activate your account'
            # }
            # status_code = send_qmeter_mail(data)
            # from ticketing.tasks import send_new_user_data
            # send_new_user_data.delay(user.id, request.META.get('REMOTE_ADDR'), request.META.get('HTTP_HOST'), 'registration')
            # if status_code:
            #     return Response(data={"message": "Email sent successfully!", **self.get_token(user, request),
            #                           **self.user_data(user)}, status=status.HTTP_200_OK)
        return Response(
            data={"message": "url params is important!"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=200)
        return Response(status=401)
