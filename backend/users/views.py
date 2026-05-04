import urllib.parse
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import SessionAuthentication
from .models import User, AccessTokenRecord
from .serializers import UserRegisterSerializer, UserSerializer
from .authentication import CookieJWTAuthentication, BlacklistJWTAuthentication


def blacklist_user_access_tokens(user):
    AccessTokenRecord.objects.filter(user=user, is_blacklisted=False).update(is_blacklisted=True)

    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
    outstanding_tokens = OutstandingToken.objects.filter(user=user)
    for token in outstanding_tokens:
        BlacklistedToken.objects.get_or_create(token=token)


def register_access_token(user, access_token_obj):
    access_jti = access_token_obj['jti']
    AccessTokenRecord.objects.get_or_create(
        jti=access_jti,
        defaults={'user': user}
    )


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'success': 'CSRF cookie set'})


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': '注册成功，请登录',
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class SessionLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            blacklist_user_access_tokens(user)

            response = Response({
                'message': 'Session登录成功',
                'auth_type': 'Session',
                'user': UserSerializer(user).data,
                'session_data': {
                    'session_key': request.session.session_key,
                    'session_expiry_age': 604800,
                    'session_cookie_name': 'studyhub_sessionid',
                },
            })

            response.set_cookie(
                key='studyhub_sessionid',
                value=request.session.session_key,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=604800,
            )

            response.delete_cookie('access_token', path='/', samesite='Lax')
            response.delete_cookie('refresh_token', path='/', samesite='Lax')
            response.delete_cookie('username', path='/', samesite='Lax')

            return response
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)


class SessionLogoutView(APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request):
        logout(request)
        response = Response({'message': 'Session登出成功，服务端Session已销毁'})
        response.delete_cookie('access_token', path='/', samesite='Lax')
        response.delete_cookie('refresh_token', path='/', samesite='Lax')
        response.delete_cookie('username', path='/', samesite='Lax')
        response.delete_cookie('studyhub_sessionid', path='/', samesite='Lax')
        response.delete_cookie('sessionid', path='/', samesite='Lax')
        return response


class SessionProfileView(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'auth_type': 'Session',
            'user': UserSerializer(request.user).data,
            'session_info': {
                'session_key': request.session.session_key,
            },
        })


@method_decorator(csrf_exempt, name='dispatch')
class TokenLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session.flush()
            request.session.modified = False

            blacklist_user_access_tokens(user)

            refresh = RefreshToken.for_user(user)
            access_token_obj = refresh.access_token
            register_access_token(user, access_token_obj)

            response = Response({
                'message': 'Token登录成功',
                'auth_type': 'JWT Token',
                'user': UserSerializer(user).data,
                'access': str(access_token_obj),
                'refresh': str(refresh),
                'token_info': {
                    'access_token_lifetime': '60分钟',
                    'refresh_token_lifetime': '7天',
                    '使用方式': 'Authorization: Bearer <access_token>',
                },
            })

            response.delete_cookie('studyhub_sessionid', path='/', samesite='Lax')
            response.delete_cookie('sessionid', path='/', samesite='Lax')
            response.delete_cookie('access_token', path='/', samesite='Lax')
            response.delete_cookie('refresh_token', path='/', samesite='Lax')
            response.delete_cookie('username', path='/', samesite='Lax')

            return response
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)


class TokenLogoutView(APIView):
    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token_str = request.data.get('refresh')
        if refresh_token_str:
            try:
                token = RefreshToken(refresh_token_str)
                token.blacklist()
            except Exception:
                pass

        blacklist_user_access_tokens(request.user)

        return Response({'message': 'Token登出成功，请客户端清除本地Token'})


class TokenProfileView(APIView):
    authentication_classes = [BlacklistJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        return Response({
            'auth_type': 'JWT Token',
            'user': UserSerializer(request.user).data,
            'token_info': {
                'auth_header': auth_header[:50] + '...' if auth_header else '无',
            },
        })


@method_decorator(csrf_exempt, name='dispatch')
class CookieLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session.flush()
            request.session.modified = False

            blacklist_user_access_tokens(user)

            refresh = RefreshToken.for_user(user)
            access_token_obj = refresh.access_token
            register_access_token(user, access_token_obj)
            access_token = str(access_token_obj)
            refresh_token = str(refresh)

            response = Response({
                'message': 'Cookie登录成功',
                'auth_type': 'Cookie',
                'user': UserSerializer(user).data,
            })

            response.delete_cookie('studyhub_sessionid', path='/', samesite='Lax')
            response.delete_cookie('sessionid', path='/', samesite='Lax')
            response.delete_cookie('access_token', path='/', samesite='Lax')
            response.delete_cookie('refresh_token', path='/', samesite='Lax')
            response.delete_cookie('username', path='/', samesite='Lax')

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=3600,
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=7 * 24 * 3600,
            )
            username_encoded = urllib.parse.quote(user.username, safe='')
            response.set_cookie(
                key='username',
                value=username_encoded,
                httponly=False,
                samesite='Lax',
                max_age=7 * 24 * 3600,
            )
            return response
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)


class CookieProfileView(APIView):
    authentication_classes = [CookieJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cookie_info = {}
        for key in ['access_token', 'refresh_token', 'username', 'studyhub_sessionid']:
            if key in request.COOKIES:
                cookie_info[key] = {
                    'value': request.COOKIES[key][:20] + '...' if len(request.COOKIES[key]) > 20 else request.COOKIES[key],
                    '存在': True,
                }

        return Response({
            'auth_type': 'Cookie',
            'user': UserSerializer(request.user).data,
            'cookie_info': cookie_info,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CookieLogoutView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication, BlacklistJWTAuthentication, CookieJWTAuthentication]

    def post(self, request):
        if request.user.is_authenticated:
            blacklist_user_access_tokens(request.user)
        response = Response({'message': 'Cookie登出成功，所有认证Cookie已清除'})
        response.delete_cookie('access_token', path='/', samesite='Lax')
        response.delete_cookie('refresh_token', path='/', samesite='Lax')
        response.delete_cookie('username', path='/', samesite='Lax')
        response.delete_cookie('studyhub_sessionid', path='/', samesite='Lax')
        response.delete_cookie('sessionid', path='/', samesite='Lax')
        logout(request)
        return response


class AuthCompareView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        session_authenticated = False
        session_user = None
        session_key = request.COOKIES.get('studyhub_sessionid') or request.COOKIES.get('sessionid')
        if session_key:
            from django.contrib.sessions.models import Session as SessionModel
            try:
                session_obj = SessionModel.objects.get(session_key=session_key)
                data = session_obj.get_decoded()
                user_id = data.get('_auth_user_id')
                if user_id:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    try:
                        user = User.objects.get(id=user_id)
                        session_authenticated = True
                        session_user = UserSerializer(user).data
                    except User.DoesNotExist:
                        pass
            except SessionModel.DoesNotExist:
                pass

        token_authenticated = False
        token_user = None
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            try:
                jwt_auth = BlacklistJWTAuthentication()
                validated_token = jwt_auth.get_validated_token(auth_header.split(' ')[1])
                jti = validated_token.get('jti')
                if jti and AccessTokenRecord.objects.filter(jti=jti, is_blacklisted=True).exists():
                    token_authenticated = False
                    token_user = None
                else:
                    user = jwt_auth.get_user(validated_token)
                    token_authenticated = True
                    token_user = UserSerializer(user).data
            except Exception:
                pass

        cookie_authenticated = False
        cookie_user = None
        cookie_access_token = request.COOKIES.get('access_token')
        cookie_has_token = bool(cookie_access_token)
        if cookie_access_token:
            try:
                jwt_auth = CookieJWTAuthentication()
                validated_token = jwt_auth.get_validated_token(cookie_access_token)
                jti = validated_token.get('jti')
                if jti and AccessTokenRecord.objects.filter(jti=jti, is_blacklisted=True).exists():
                    cookie_authenticated = False
                    cookie_user = None
                else:
                    user = jwt_auth.get_user(validated_token)
                    cookie_authenticated = True
                    cookie_user = UserSerializer(user).data
            except Exception:
                pass

        result = {
            'session': {
                'auth_method': 'Session认证',
                '当前状态': '已认证' if session_authenticated else '未认证',
                'sessionid': session_key or '无',
                'user': session_user,
            },
            'token': {
                'auth_method': 'Token(JWT)认证',
                '当前状态': '已认证' if token_authenticated else '未认证',
                'auth_header': auth_header[:50] + '...' if len(auth_header) > 50 else (auth_header or '无'),
                'user': token_user,
            },
            'cookie': {
                'auth_method': 'Cookie认证',
                '当前状态': '已认证' if cookie_authenticated else '未认证',
                'has_token': cookie_has_token,
                'cookies': list(request.COOKIES.keys()),
                'user': cookie_user,
            },
        }
        return Response(result)
