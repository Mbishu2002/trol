from django.shortcuts import render
from .serializers import *
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from django.contrib.auth.tokens import default_token_generator
from django.template import loader
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, force_text, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from rest_framework import status
import jwt, datetime
from  django.core.mail import *
from django.contrib.auth.decorators import login_required
from rest_framework.parsers import MultiPartParser
from django.views.decorators.csrf import csrf_exempt
import binascii

@api_view(['POST'])
def register(request) :
    if request.method == 'POST':
        email = request.data.get('email')
        username = request.data.get('username')
        is_business = request.data.get('is_business')
        serializer = UserSerializer(data=request.data)
        if User.objects.filter(email=email).exists():
            return Response({"message":"email already registered"})
        elif  User.objects.filter(username = username).exists():
            return Response({"message":"username already taken"})
        else:
            if serializer.is_valid():
                user = serializer.save()
                payload ={
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator(user),
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                    'iat': datetime.datetime.utcnow()
                }
                # current_site = get_current_site(request)
                subject = 'Activate Your Account'
                token = jwt.encode(payload, key='secret', algorithm="HS256")
                message = render_to_string('verification_email.html', {
                    'user': user,
                    'domain': 'Trol',
                    'token' : token
                })
                to_email = email
                email = EmailMultiAlternatives(
                    subject, message, to=[to_email]
                )
                email.attach_alternative(message, "text/html")
                email.send()
                messages.success(request, 'Please confirm your email address to complete the registration.')
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
     if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        password = request.data.get('password')
        email = request.data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
                raise AuthenticationFailed('User with this email does not exist')
        if not user.check_password(password):
            raise AuthenticationFailed('wrong password')
        payload = {
            'id' : user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=180),
            'iat': datetime.datetime.utcnow()
        } 
        token = jwt.encode(payload,key='secret',algorithm="HS256")
        response = Response()
        response.set_cookie(key='jwt', value=token,httponly=True )
        return Response( "ok", status= status.HTTP_200_OK)
@api_view(['GET'])
@csrf_exempt
def verify_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        return Response({"message": "User verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired verification token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@parser_classes([MultiPartParser])
def update_user(request, user_id):
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_password_reset_email(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        if not validated_data:
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "This email address is not registered with us."}, status=status.HTTP_400_BAD_REQUEST)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        otp = default_token_generator.make_token(user)
        context = {
            'uid': uid,
            'token': otp,
            'protocol': 'https' if request.is_secure() else 'http',
        }
        subject = loader.render_to_string('reset_password_subject.txt', context)
        message = loader.render_to_string('reset_password_email.html', context)
        send_mail(subject, message, 'fmbishu@gmail.com', [email], fail_silently=False)
        return Response({"message": "Password reset email sent successfully"})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def set_new_password(request):
    serializer = SetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        password = request.data.get('password')
        token = request.data.get('token')
        uidb64 = request.data.get('uidb64')

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            users = User.objects.filter(pk=uid)

            if users.exists() and default_token_generator.check_token(users[0], token):
                user = users[0]
                user.set_password(password)
                user.save()
                return Response({"message": "Password set successfully"})

        except (TypeError, ValueError, OverflowError, DjangoUnicodeDecodeError, binascii.Error, User.DoesNotExist):
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Invalid/Expired token"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@login_required
def logout(request):
    response = Response()
    response.delete_cookie('jwt')
    return Response(status= status.HTTP_200_OK)


@api_view(['GET'])
@login_required
def get_user(request):
    user = request.user
    serializer = UserDetailSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@login_required
def follow_user(request):
    serializer = FollowersSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@login_required
def get_followers(request, user_id):
    followers = Followers.objects.filter(business__user_id=user_id)
    serializer = FollowersSerializer(followers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)