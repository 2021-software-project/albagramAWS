import random

import pandas as pd
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_auth.app_settings import create_token
from rest_framework.decorators import APIView, api_view, renderer_classes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import GenericAPIView

from .models import UserRating, UserPostingClick, UserPostingLike, ResultSatisfy
from .serializers import UserRatingSerializer, UserPostingClickSerializer, UserPostingLikeSerializer, \
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, CustomRegisterSerializer, \
    CustomUserDetailsSerializer, ResultSatisfySerializer
from rest_framework.response import Response
from rest_framework import generics, status
from .models import CustomUser

from django.core import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import  urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from rest_framework.authtoken.models import Token
from pandas import DataFrame
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .job_code import job_code, large_job_code
from .modules.code_to_korean import codeToKorean
# from ipware.ip import get_ip
from django.db import IntegrityError


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    @csrf_exempt
    def post(self, request):
        try:
            user = authenticate(username=request.data['email'], password=request.data['password'])
            if user is not None:
                try:
                    token = Token.objects.create(user=user)
                except IntegrityError as e:
                    token = Token.objects.get(user=user)
                return Response({"token": token.key})
            else:
                return Response(status=401)
        except:
            return Response(status=400)


class SignupView(APIView):
    serializer_class = CustomRegisterSerializer
    authentication_classes =[]
    permission_classes = []

    def post(self, request):
        try:
            serializer = self.serializer_class(request.data)

            email = request.data['email']
            username = request.data['username']
            password1 = request.data['password1']
            password2 = request.data['password2']
            mbti = request.data['mbti']
            # customuser = CustomRegisterSerializer.save(self, request=request.data)
            # print("customuser ",customuser)
            if CustomUser.objects.filter(email=email).exists():
                return Response({'email' : '?????? ???????????? ??????????????????.'}, status=status.HTTP_400_BAD_REQUEST)
            elif password1 != password2:
                return Response({'password' : '??????????????? ???????????? ????????????.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = CustomUser.objects.create_user(email=email, username = username,
                                                  password=password1,
                                                  mbti=mbti)
                user.save()
                # token = Token.objects.create(user=user)
                return Response({"success": "??????????????? ???????????????! ???????????????!"})
        except :
            return Response({"msg":"???????????? ??????"},status=status.HTTP_400_BAD_REQUEST)

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    # ?????? ??????
    authentication_classes =[]
    permission_classes = []
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            print(current_site)
            # ip = get_client_ip(request)
            # if ip is not None:
            #     print("?????????", ip)
            # else:
            #     print("????????????")
            relativeLink = reverse('password-reset-confirm',
                                   kwargs={'uidb64':uidb64,'token':token})
            print(request.get_host()) #?????? url??? ??????????????? ...
            absurl = 'http://127.0.0.1:8000'+relativeLink    #http://www.albagram.kro.kr
            email_body = "<div style='text-align : center'>" \
                         "<h3>???????????????. " +user.username+'???, Albagram ?????????. </h3> ' \
                        '<p>????????? ????????? ?????? ???, ???????????? ???????????? ???????????????. </p><br/>' \
                        '<a '\
                        "style='padding: 14px 20px;color: #ffffff;font-size: 15px;"\
                        "font-weight: bold; background-color: rgba(114, 96, 144, 0.75); border: 0;"\
    	                "border-radius: 8px; text-decoration: none; margin-bottom:10px;'"\
                        'href='+absurl+'>???????????? ?????????</a>'\
                        '</div>'
            data = {'email_body' : email_body,'to_email':user.email,
                    'email_subject' : '[Albagram] ???????????? ???????????? ?????? ???????????????.'}

            Util.send_email(data)
        #     success ??????
        else:
            return Response({'result' : 'fail'},status=status.HTTP_400_BAD_REQUEST)

        return Response({'result' : 'success'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    # ?????? ??????
    authentication_classes = []
    permission_classes = []
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'Token is not valid, please request a new one'},status=status.HTTP_401_UNAUTHORIZED)
            return HttpResponseRedirect("/password-reset/{}/{}".format(uidb64,token))

        except DjangoUnicodeDecodeError as identifier:
            return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    # ?????? ??????
    authentication_classes = []
    permission_classes = []
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        # serializer.is_valid(raise_exception=True)
        uid = request.data['uid']
        password = request.data['password']

        id = force_str(urlsafe_base64_decode(uid))
        user = CustomUser.objects.get(id=id)

        user.set_password(password)
        user.save()

        return Response({'success':True, 'message':'Password reset Success'},status=status.HTTP_200_OK)



class UserRatingVIEW(generics.ListAPIView): #???????????? db??? ?????? ????????????(Create, Read)
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        print(search)
        if search:
            qs = qs.filter(email=search)
            for rating in qs:
                largejobcode = rating.jobfamily
                subcode = rating.job
                rating.jobfamily = dict(map(reversed,large_job_code.items()))[largejobcode]
                rating.job = dict(map(reversed,job_code[largejobcode].items()))[subcode]
        return qs

    def post(self, request): #CreateModelMixin??? ???????????? ????????? drf api??? ????????? ??????
        copyData = request.data.copy() #queryDict??? ??????. ??????????????? ???????????? ???????????????
        largejobcode = large_job_code[request.data['jobfamily']]
        smalljobcode = job_code[largejobcode][request.data['job']]
        copyData['jobfamily'] = largejobcode
        copyData['job'] = smalljobcode

        serializer = UserRatingSerializer(data=copyData)  # JSON -> Serialize

        if serializer.is_valid():  # ????????? ?????? ??? ??????
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ratingDetails(APIView):  #???????????? Update, Delete
    def get_object(self, ratingId):
        try:  # ???????????? ????????? Article ????????? ?????????
            return UserRating.objects.get(id=ratingId)

        except UserRating.DoesNotExist:  # ????????? ????????? ????????? 404??????
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, ratingId):
        rating = self.get_object(ratingId)
        serializer = UserRatingSerializer(rating)
        return Response(serializer.data)

    def put(self, request, ratingId):
        rating = self.get_object(ratingId)
        serializer = UserRatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ratingId):
        article = self.get_object(ratingId)
        article.delete()
        return Response(status=201)
        #return Response(status=status.HTTP_204_NO_CONTENT)  # ????????? ??????



class UserPostingClickVIEW(generics.ListAPIView): #???????????? ????????? ?????? ??? ????????? ??????
    queryset = UserPostingClick.objects.all()
    serializer_class = UserPostingClickSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request): #CreateModelMixin??? ???????????? ????????? drf api??? ????????? ??????
        serializer = UserPostingClickSerializer(data = request.data)  # JSON -> Serialize

        if serializer.is_valid():  # ????????? ?????? ??? ??????
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserPostingLikeVIEW(generics.ListAPIView): #?????? ???/??? Create, Read
    queryset = UserPostingLike.objects.all()
    serializer_class = UserPostingLikeSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(email=search)
        return qs

    def post(self, request):  # CreateModelMixin??? ???????????? ????????? drf api??? ????????? ??????
        serializer = UserPostingLikeSerializer(data=request.data)  # JSON -> Serialize

        if serializer.is_valid():  # ????????? ?????? ??? ??????
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UserPostingLikeDetails(APIView):  #?????? ???/??? Update, Delete
    def get_object(self, email, post_id):
        try:  # ?????????(email+??????id??? ?????????)??? ????????? ????????? ?????????
            return UserPostingLike.objects.get(email=email, post_id=post_id)
        except UserPostingLike.DoesNotExist:  # ????????? ????????? ????????? 404??????
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, email, post_id):
        if UserPostingLike.objects.filter(email=email, post_id=post_id).exists(): #???????????? ?????????
            userpostinglike = self.get_object(email, post_id)
            serializer = UserPostingLikeSerializer(userpostinglike)
            return Response(serializer.data)
        else:
            return Response(0)

    def put(self, request, email, post_id):
        userpostinglike = self.get_object(email, post_id)
        serializer = UserPostingLikeSerializer(userpostinglike, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, email, post_id):
        userpostinglike = self.get_object(email, post_id)
        userpostinglike.delete()
        return Response(status=201)
        #return Response(status=status.HTTP_204_NO_CONTENT)  # ????????? ??????


class UserPostingLikeWithPosting(APIView):
    model = UserPostingLike
    def get(self, request, email):
        userpostinglike = UserPostingLike.objects.select_related().filter(email=email)
        serializer = UserPostingLikeSerializer(userpostinglike, many=True)

        num=-1
        for like in userpostinglike:
            num+=1
            JobPosting = {
                'id': like.post_id.id,
                'city':like.post_id.city,
                'county':like.post_id.county,
                'company':like.post_id.company,
                'subtitle': like.post_id.subtitle,
                'url':like.post_id.url,
                'pay_type':like.post_id.pay_type,
                'pay': like.post_id.pay,
                'sub_code': like.post_id.sub_code,
                'enrol_date': like.post_id.enrol_date,
            }
            serializer.data[num]['post_id'] = JobPosting
        return Response(serializer.data)


class UserDetailVIEW(generics.ListAPIView):

   def get(self, request, email):
       if CustomUser.objects.filter(email=email).exists():
           user = CustomUser.objects.get(email=email)
       return Response({"mbti":user.mbti, "username":user.username}, status=status.HTTP_200_OK)

   def post(self,request):
       email = request.data["email"]
       mbti = request.data["mbti"]
       if CustomUser.objects.filter(email=email).exists():
          user = CustomUser.objects.get(email=email)
          user.mbti = mbti
          user.save()

         #if UserPostingLike.objects.filter(email=email).exists():
         #    print("email",email)
         #    user_postings = UserPostingLike.objects.get(email=email)
         #    user_postings.mbti = mbti
         #    user_postings.save()

         #    return Response({'success': True, 'message': 'MBTI??? ?????????????????????.'}, status=status.HTTP_200_OK)

          return Response({'success': True, 'message': 'MBTI??? ?????????????????????.'}, status=status.HTTP_200_OK)
       else:
           return Response({'error': '????????? ??? ?????? ????????????.'}, status=status.HTTP_401_UNAUTHORIZED)


class resultSatisfyView(generics.ListAPIView):
    queryset = ResultSatisfy.objects.all()
    serializer_class = ResultSatisfySerializer
    def post(self, request):
        serializer = ResultSatisfySerializer(data=request.data)  # JSON -> Serialize

        if serializer.is_valid():  # ????????? ?????? ??? ??????
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class resultSatisfyDetails(APIView):  # Update
    def get_object(self, id):
        try:
            return ResultSatisfy.objects.get(id=id)
        except ResultSatisfy.DoesNotExist:  # ????????? ????????? ????????? 404??????
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, id):
        if ResultSatisfy.objects.filter(id=id).exists(): #???????????? ?????????
            resultsatisfy = self.get_object(id)
            serializer = ResultSatisfySerializer(resultsatisfy)
            return Response(serializer.data)
        else:
            return Response(0)

    def put(self, request, id):
        resultsatisfy = self.get_object(id)
        serializer = ResultSatisfySerializer(resultsatisfy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from .models import JobPosting
from .modules.recommendation import Recommendation

@method_decorator(csrf_exempt,name='dispatch')
class mbtiRcm(View):

    def get(self, request):
        mbti = request.GET.get('mbti')
        email = request.GET.get('email')
        user_rating = UserRating.objects.filter(email=email)

        if not user_rating.exists():
            return HttpResponse('??????????????? ????????? ?????? ????????????!', status=status.HTTP_400_BAD_REQUEST)
        else:
            rec = Recommendation()

            job_list = rec.recommendation('cb', email, mbti, 5)
            job_code_list = codeToKorean(job_list)

            return JsonResponse({
                'job_list' : job_code_list
            }) # ?????? ?????? ??????????????? 16????????? ????????? ?????? : ????????? ??????????????? json_dumps_params = {'ensure_ascii': False} ??????


@method_decorator(csrf_exempt,name='dispatch')
class persRcm(View):
    def get(self, request):
        email = request.GET.get('email')
        user_rating = UserRating.objects.filter(email=email)

        if not user_rating.exists():
            return HttpResponse('??????????????? ????????? ?????? ????????????!', status=status.HTTP_400_BAD_REQUEST)

        rec = Recommendation()
        job_list = rec.recommendation('cf_u', email, 5)
        job_code_list = codeToKorean(job_list)

        return  JsonResponse({
            'job_list' : job_code_list,
        }) # ?????? ?????? ??????????????? 16????????? ????????? ?????? : ????????? ??????????????? json_dumps_params = {'ensure_ascii': False} ??????


@csrf_exempt
def postings(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        print("code ", code)
        selArea = request.POST.getlist('selectArea')
        print("[selArea] ", selArea)

        qs = JobPosting.objects.filter(sub_code=code, city=selArea[0], county=selArea[1])
        for i in range(3):
            if len(selArea) > i * 2:
                print(selArea[2*i], selArea[2*i+1])
                if selArea[2*i] == '??????':
                    qs = JobPosting.objects.filter(sub_code=code)
                else:
                    if selArea[2*i+1] == '??????':
                        qs2 = JobPosting.objects.filter(sub_code=code, city=selArea[2*i])
                    else:
                        qs2 = JobPosting.objects.filter(sub_code=code, city=selArea[2*i], county=selArea[2*i+1])
                    qs = qs.union(qs2)

        if len(qs) > 45:
            qs = random.sample(list(qs), 45)
        # print("????????????: ",len(qs))
        # print("----------------- qs\n",qs)

        post_list = serializers.serialize('json', qs)

        # print(post_list)
        return HttpResponse(post_list, content_type="text/json-comment-filtered")

