from myauth.models import *
from django.contrib.auth import get_user_model
import bcrypt
from rest_framework import serializers
from django.contrib.auth import authenticate
from myauth.utils.validators import *
from rest_framework.exceptions import ValidationError


User = get_user_model()
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ('id','email','branch','password','password2','last_name','first_name','phone_number','job','team','customer_access_by_ids')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def validate(self, attrs):
        data = super().validate(attrs)
        if data['password']!= data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data



    def update(self, instance, validated_data):
        print('UPDATE')
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance



    def save(self):
        print(dict(self.validated_data),'VALIDATE DATAA')
        new_data = dict(self.validated_data)

        password = self.validated_data['password']
        
        # new_data.pop("password")
        new_data.pop("password2")
        print(new_data,'ALL')
        user = User.objects.create_user(**new_data)
        return user

class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    # recaptcha = ReCaptchaField(required=not settings.ON_PREMISE)

    def validate_email(self, attr):
        return attr.lower()

    @staticmethod
    def check_old_password(data):
        email, password = data.get("email"), data.get("password")
        if email and password:
            u = User.objects.filter(email__icontains=str(email).lower(), password__startswith="$2a$10$",
                                    is_active=False).last()
            if u and bcrypt.checkpw(str(password).encode('utf8'), str(u.password).encode('utf-8')):
                u.set_password(password)
                u.is_active = True
                u.save(update_fields=["password", "is_active"])
                return True
        return False

    def validate(self, data):
        self.check_old_password(dict(data))
        user = authenticate(request=self.context['request'], **data)
        if not user:
            raise serializers.ValidationError({'message': _("Unable to log in with provided credentials.")})
        return user





class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    is_staff = serializers.BooleanField(required=False)
    date_joined = serializers.CharField(required=True)
    job = serializers.CharField(required=False)
    team = serializers.CharField(required=False)


class PasswordUpdateSerializer(serializers.Serializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
    id = serializers.IntegerField()

    class Meta:
        fields = ('id','password','password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def validate(self, attrs):
        data = super().validate(attrs)
        if data['password']!= data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    # recaptcha = ReCaptchaField(required=not settings.ON_PREMISE, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'confirm_password', "first_name", 'last_name', 'phone_number',
                'time_zone', 'job_title')#'recaptcha'
        read_only_fields = ('id',)
        extra_kwargs = {'phone_number': {'required': True}, 'email': {'required': True}}

    def validate_email(self,attr):
        return attr.lower()

    def validate_password(self, attr):
        if not my_check_password(attr):
            raise ValidationError(_("""At least 8 characters, Must be restricted to, though does not specifically require any of: 
            uppercase letters: A-Z, lowercase letters: a-z, numbers: 0-9, any of the special characters: @#$%^&+=."""))
        return attr

    def validate_confirm_password(self, attr):
        if attr != self.initial_data.get('password'):
            raise ValidationError(_("Mistyped! `Password` and `confirm password` did not match. Try again please"))
        return attr

    def validate_phone_number(self, attr):
        if not my_check_phone_number(attr):
            raise ValidationError(_('Phone number is invalid. This must contain only digits. Allowed range is 9 - 15'))
        return attr

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        if validated_data.get("recaptcha"):
            validated_data.pop("recaptcha")
        
        validated_data.update({'is_master': True})
        validated_data.update({'is_active': False})
        user = User.objects.create_user(**validated_data)
        return user
