from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import AuthenticationFailed

from .models import CustomUser, UserRating, UserPostingClick, UserPostingLike, ResultSatisfy


@csrf_exempt
class UserSerializer(serializers.ModelSerializer):
    # authentication_classes =[]
    # permission_classes = []

    class Meta:
        model = CustomUser
        fields = ('email','username','first_name', 'last_name','last_login','date_joined','is_staff','sns', 'mbti')

@csrf_exempt
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('pk', 'username', 'email', 'mbti')
        read_only_fields = ('email', )

@csrf_exempt
class CustomRegisterSerializer(serializers.ModelSerializer):
    # authentication_classes =[]
    # permission_classes = []

    password1 = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2','first_name','last_name','sns','mbti']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    # def get_cleaned_data(self):
    #     data = super(CustomRegisterSerializer, self).get_cleaned_data()
    #     return data

    def save(self,request, *args, **kwargs):
        print("save")
        user = CustomUser.objects.create_user(
            username = self.validated_data.get('username',' '),
            email= self.validated_data.get('email', ' '),
            sns = self.validated_data.get('sns',' '),
            mbti=self.validated_data.get('mbti', ' '),
        )
        password1 = self.validated_data.get('password1', ' ')
        password2 = self.validated_data.get('password2', ' ')

        if CustomUser.objects.filter(email=user.email).exists():
            raise serializers.ValidationError({'email':'이미 사용중인 이메일입니다.'})
        elif CustomUser.objects.filter(username=user.username).exists():
            raise serializers.ValidationError({'username': '이미 사용중인 닉네임입니다.'})
        elif password1 != password2:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})

        user.set_password(password1)
        user.save()
        return user


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6,max_length=68,write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields=['password','token','uidb64']


class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = '__all__'  #모델에서 설정한 모든 필드를 여기서도 설정해줌

class UserPostingClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostingClick
        fields = '__all__'


class UserPostingLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostingLike
        fields = '__all__'

class ResultSatisfySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultSatisfy
        fields = '__all__'